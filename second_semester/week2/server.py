import socket
import threading

# 접속한 사람 목록
clients = {}

# 전체 클라이언트에게 메시지 전송
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                remove_client(client)

# 클라이언트 퇴장 처리
def remove_client(client_socket):
    if client_socket in clients:
        name = clients[client_socket]
        del clients[client_socket]
        broadcast(f'[{name}] 님이 퇴장하셨습니다.')
        print(f'{name} 퇴장')

# 메시지 처리 (일반 / 귓속말)
def handle_message(sender_socket, message):
    sender_name = clients[sender_socket]

    if message.startswith('/w'):
        parts = message.split(' ', 2)
        if len(parts) < 3:
            sender_socket.send('귓속말 사용법: /w 사용자이름 메시지\n'.encode('utf-8'))
            return
        target_name, whisper_message = parts[1], parts[2]

        for client, name in clients.items():
            if name == target_name:
                client.send(f'(귓속말) {sender_name}> {whisper_message}'.encode('utf-8'))
                sender_socket.send(f'(귓속말 보냄) {sender_name}> {whisper_message}'.encode('utf-8'))
                return

        sender_socket.send(f'[{target_name}] 사용자를 찾을 수 없습니다.\n'.encode('utf-8'))
    else:
        broadcast(f'{sender_name}> {message}', sender_socket)

# 각 클라이언트 처리 스레드
def handle_client(client_socket):
    try:
        # 닉네임 받기
        client_socket.send('닉네임을 입력하세요: '.encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8').strip()
        clients[client_socket] = name
        print(f'{name} 입장')
        broadcast(f'[{name}] 님이 입장하셨습니다.', client_socket)

        # 채팅 받기
        while True:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                continue
            if message == '/종료':
                remove_client(client_socket)
                client_socket.close()
                break
            else:
                handle_message(client_socket, message)
    except:
        remove_client(client_socket)

# 서버 시작
def start_server(host='127.0.0.1', port=6000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f'서버 시작됨: {host}:{port}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'새 연결: {addr}')
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == '__main__':
    start_server()
