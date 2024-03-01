from socket import *
import threading;

#metodo temporario, futuramente tera canais

#mude somente se souber o que está fazendo!
server_port = 5757


def main_screen():
    print("--------------------------")
    print("Bem-vindo ao DioneChat V1")
    print("       dale 1TDSA!       ")
    print("Canal padrão: 1tdsa")
    print("--------------------------")
    print()
    response = input("Server/User: ")
    if(response == "Server"):
        run_server()
    else:
        run_client(False)

#if channel already exists, user only connects to server
def run_client(is_server):
    server_address = "localhost"

    if(not is_server):
        server_address = input("IP: ")
    
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    def recieve_messages():
        while True:
            recieved_message = client_socket.recv(4096)
            if(len(recieved_message) > 0):
               print(">> " + recieved_message.decode())
    
    def send_message():
        while True:
            sentence = input(">> ")
            client_socket.sendall(sentence.encode())
    
    recieve_thread = threading.Thread(target=recieve_messages)
    recieve_thread.start()

    send_thread = threading.Thread(target=send_message)
    send_thread.start()


#if channel is not created yet, user is the server
def run_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    run_client(True)

    
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

#store all clients
clients = []
def handle_client(client_socket, client_address):
        clients.append(client_socket)
        try:
            while True:
                message = client_socket.recv(4096)
                if(len(message) > 0):
                    for c in clients:
                        if(c != client_socket):
                           c.sendall(message)
        except Exception as e:
            print(f"Error handling client {client_address}")
        finally:
            client_socket.close()

    


    

main_screen()
