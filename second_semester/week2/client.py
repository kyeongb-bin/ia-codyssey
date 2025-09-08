import socket
import threading

# 서버에서 오는 메시지 받기
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print('서버 연결이 종료되었습니다.')
            sock.close()
            break

# 클라이언트 시작
def start_client(host='127.0.0.1', port=6000):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.daemon = True
    thread.start()

    while True:
        message = input()
        if message:
            client_socket.send(message.encode('utf-8'))
            if message == '/종료':
                break

    client_socket.close()

if __name__ == '__main__':
    start_client()
