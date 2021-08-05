## gRPC Overview

Unary RPC -- use-case : 클라이언트는 서버에 Single Request를 보내고 다시 Single Response를 받습니다.

```
message testRequest{
   string message = 1; //#1 정의된 Request Protocol Buffer
}
service testService{
   rpc getTest(testRequest) returns (testResponse); //#2 testRequest에 따라 testResponse 메시지를 보내줍니다.
}
```

Bidirectional streaming RPC -- use-case: read-write 스트림을 이용해 일련의 메시지를 서버, 클라이언트 양쪽으로 보내게 됩니다.
두 개의 스트림이 독립적으로 작동하기 때문에 클라이언트와 서버는 원하는 순서대로 읽고 쓸 수 있습니다.

```
message testRequest{
  string message = 1; //#1 정의된 Request Protocol Buffer
}

service testService{
  rpc ListTest(stream testRequest) returns (stream testResponse); //#2 request, response 타입이 stream으로 전달되고 받아오게 됩니다.
}
```

Server-side Stream RPC -- use-case : 클라이언트가 서버에 Request를 보내고 스트림을 가져와 일련의 메시지를 읽습니다. return 되는 스트림의 메시지가 없을 떄 까지 읽습니다. 개별적인 gRPC에 대한 메시지 순서를 보증합니다.

```
message testRequest{
   string message = 1; //#1 정의된 Request Protocol Buffer
}

service testService{
   rpc ListTest(testRequest) returns (stream testResponse); //#2 testRequest에 따라 stream 메시지를 보내줍니다.
}
```

Client-side Stream RPC --use-case : 클라이언트는 일련의 메시지를 작성하고 스트림으로 서버로 전송하게 됩니다. 클라이언트에서 메시지 작성을 끝내고 서버에 전송하게 되면 서버에서 읽고 응답을 반환할 때까지 기다립니다. Server streaming RPC와 마찬가지로 개별적인 RPC call에 대한 메시지 순서를 보증하게 됩니다.

```
message testRequest{
   string message = 1; //#1 정의된 Request Protocol Buffer
}
service testService {
   rpc ListTest(stream testRequest) returns (testResponse); //#2 stream testRequest에 따라 testResponse 메시지를 보내줍니다.
}
```
