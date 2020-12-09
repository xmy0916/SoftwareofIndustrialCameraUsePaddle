## 文件结构
整体文件结构如下：
```
Traffic_Safety
	client.py   (客户端，数据发送)
	data_pb2.py   (消息类定义)
	data_pb2_grpc.py   (gRPC server类(FormatDataServicer)和client类(FormatDataStub)定义)
	server.py   (服务器，数据接收)
	test.py   (摄像头打开测试)
	README.md
```

