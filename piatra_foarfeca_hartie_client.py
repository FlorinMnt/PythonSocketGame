import socket
import threading

def read_user_input():
    while True:
        user_input = input()
        client_socket.send(user_input.upper().encode())


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

server_message = client_socket.recv(1024).decode()
print(server_message)

# Creează un fir de execuție pentru a citi comenzile de la utilizator în fundal
user_input_thread = threading.Thread(target=read_user_input)
user_input_thread.start()

while True:
 
    server_message = client_socket.recv(1024).decode()
    print(server_message)

    # Dacă jocul este terminat, întreabă utilizatorul dacă dorește să înceapă un joc nou
    if 'Jocul s-a încheiat' in server_message:
        new_game_command = input('Pentru a începe un joc nou, tastati START. Altă comandă pentru a închide: ')
        client_socket.send(new_game_command.upper().encode())
        if new_game_command != 'START':
            break
 
client_socket.close()
