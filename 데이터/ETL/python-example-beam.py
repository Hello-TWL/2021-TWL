
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" data_enrichment.py demonstrates a Dataflow pipeline which reads a file and
 writes its contents to a BigQuery table.  Along the way, data from BigQuery
 is read in as a side input and joined in with the primary data from the file.
"""

import argparse
import csv
import logging
import os
import sys

import apache_beam as beam
from apache_beam.io.gcp import bigquery
from apache_beam.io.gcp.bigquery import parse_table_schema_from_json
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.pvalue import AsDict


class DataIngestion(object):
    """A helper class which contains the logic to translate the file into a
  format BigQuery will accept."""

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.schema_str = ''
        # This is the schema of the destination table in BigQuery.
        schema_file = os.path.join(dir_path, 'schema',
                                   'usa_names_with_full_state_name.json')
        with open(schema_file) \
                as f:
            data = f.read()
            # Wrapping the schema in fields is required for the BigQuery API.
            self.schema_str = '{"fields": ' + data + '}'

    def parse_method(self, string_input):

        featdict = {}
        header = "state_name,state_abbreviation".split(",")
        for name, value in zip(header, string_input):
            featdict[name] = value

        print(featdict)
        return featdict


def run(argv=None):
    """The main function which creates the pipeline and runs it."""
    parser = argparse.ArgumentParser()
    # Here we add some specific command line arguments we expect.   Specifically
    # we have the input file to load and the output table to write to.
    parser.add_argument(
        '--input',
        dest='input',
        required=False,
        help='Input file to read.  This can be a local file or '
        'a file in a Google Storage Bucket.',
        # This example file contains a total of only 10 lines.
        # Useful for quickly debugging on a small set of data
        default='gs://python-dataflow-example/data_files/username-password-recovery-code.csv')
    # The output defaults to the lake dataset in your BigQuery project.  You'll have
    # to create the lake dataset yourself using this command:
    # bq mk lake
    parser.add_argument('--output',
                        dest='output',
                        required=False,
                        help='Output BQ table to write results to.',
                        default='tkroh_test.dataflow_output')

    # Parse arguments from the command line.
    known_args, pipeline_args = parser.parse_known_args(argv)

    # DataIngestion is a class we built in this script to hold the logic for
    # transforming the file into a BigQuery table.
    data_ingestion = DataIngestion()

    # Initiate the pipeline using the pipeline arguments passed in from the
    # command line.  This includes information like where Dataflow should store
    #  temp files, and what the project id is
    p = beam.Pipeline(options=PipelineOptions(pipeline_args))
    schema = parse_table_schema_from_json(data_ingestion.schema_str)

    # This function adds in a full state name by looking up the
    # full name in the short_to_long_name_map.  The short_to_long_name_map
    # comes from a read from BigQuery in the next few lines
    def add_full_state_name(row, short_to_long_name_map):
        row['state_full_name'] = short_to_long_name_map[row['state']]
        return row

    # This is a second source of data.  The source is from BigQuery.
    # This will come into our pipeline a side input.

    read_query = """
    SELECT
    state_name,
    state_abbreviation
    FROM
    `jungang-poc.tkroh_test.state_abbreviations`"""

    state_abbreviations = (
        p | 'Read from BigQuery' >> beam.io.Read(
            beam.io.BigQuerySource(query=read_query, use_standard_sql=True))
        # We must create a python tuple of key to value pairs here in order to
        # use the data as a side input.  Dataflow will use the keys to distribute the
        # work to the correct worker.
        | 'Abbreviation to Full Name' >>
        beam.Map(lambda row: (row['state_abbreviation'], row['state_name']))
         # Translates from the raw string data in the CSV to a dictionary.
         # The dictionary is a keyed by column names with the values being the values
         # we want to store in BigQuery.
        | 'String to BigQuery Row' >>
         beam.Map(lambda s: data_ingestion.parse_method(s))
        | 'Write to BigQuery' >> beam.io.Write(
             beam.io.BigQuerySink(
                 # The table name is a required argument for the BigQuery sink.
                 # In this case we use the value passed in from the command line.
                 known_args.output,
                 # Here we use the JSON schema read in from a JSON file.
                 # Specifying the schema allows the API to create the table correctly if it does not yet exist.
                 schema=schema,
                 # Creates the table in BigQuery if it does not yet exist.
                 create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                 # Deletes all data in the BigQuery table before writing.
                 write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE))
    )

    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()