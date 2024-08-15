
import socket
import threading
import time


def start_client(server_host , server_port , client_Id, local_host , local_port) :
    #和服务器首先建立连接
    try:
        cur_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cur_client.connect((server_host, server_port))
        cur_client.send(client_Id.encode())
        print(f"{client_Id.encode()}")
    except Exception as e:
        print(f'connect server error!')

    while True:
        socket_loc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket_loc.connect((local_host, local_port))

        try:
            data = cur_client.recv(1024)

            if not data:
                break

            socket_loc.send(data)
            res = socket_loc.recv(1024)

            if not res:
                break
            cur_client.send(res)
        except Exception as e:
            print(f"Error in client: {e}")
        finally:
            socket_loc.close()




start_client("127.0.0.1", 5000, "test-client", "127.0.0.1", 8000)