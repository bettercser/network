
#服务端需要做的事情    处理外部的数据连接 并通过私有协议处理后 转发给客户端 客户端在发送数据给内网中的设备，并把响应写回传送给服务器， 处理客户端的连接
import socket
import threading

clients = {}


def handler_external_conncetion(socket_ext, client_id) :
    try:
        # 从clients 中 拿出客户端的连接
        socket_cli = clients[client_id]
        while True:
            # 外部连接 是外部 和服务器建立的
            data = socket_ext.recv(1024)
            if not data :
                break
            socket_cli.send(data)

            res = socket_cli.recv(1024)

            if not res :
                break
            socket_ext.send(res)
    except Exception as e:
        print(f"Error connection information : {e}")

def handler_client_connection(socket_cli) :
    try:
        print(f"first")
        cli_Id = socket_cli.recv(1024).decode()

        print(f"{cli_Id} connected")

        clients[cli_Id] = socket_cli

        while True:
            data = socket_cli.recv(1024)

            if not data:
                break

    except Exception as e:
        print(f"Error client connection information : {e}")
    finally:
        del clients[cli_Id]
        socket_cli.close()



def start_server(host, port) :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    server.listen(3)
    print(f"server listen in {host}:{port}")

    while True:

        socket_cli, _ = server.accept()
        threading.Thread(target=handler_client_connection, args=(socket_cli,)).start()


def start_listener_ext(ext_port, client_Id) :
    listener_ext = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_ext.bind(("0.0.0.0", ext_port))
    listener_ext.listen(3)

    print(f"external listener in {ext_port}")

    while True:
        socket_ext, _ = listener_ext.accept()
        threading.Thread(target=handler_external_conncetion, args=(socket_ext, client_Id)).start()


threading.Thread(target=start_server, args=("0.0.0.0", 5000)).start()

start_listener_ext(6000, "test-client")







