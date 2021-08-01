## TimeZone 수정하기

CREATE OR REPLACE TABLE aladin_demo.purchase_complete
(
  eventTime STRING not null,
  eventType STRING,
  userInfo struct<visitorId STRING not null> not null,
  productEventDetail struct<productDetails array<struct<id INTEGER not null, originalPrice FLOAT64, quantity INTEGER not null>>, 
  purchaseTransaction struct<currencyCode STRING, revenue FLOAT64>>
)
as 
SELECT
  REPLACE(replace(cast(InDate as STRING)," ", "T"),"+00", "Z") as eventTIme,
  'purchase-complete' as eventType,
  struct(CAST(_User_Id_ as STRING)) as userInfo,
  struct(array[struct(Item_Id, cast(item.Price as FLOAT64), 1)],struct('KRW',cast(PRICE as FLOAT64)))

FROM
  taekyun1.aladin_demo.interaction join aladin_demo.item on interaction.Item_Id = item._Item_Id_