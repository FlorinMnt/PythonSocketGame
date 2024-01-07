import socket
import random

rules = {'P': 'F', 'H': 'P', 'F': 'H'}

def get_winner(player_choice, server_choice):
    if player_choice == server_choice:
        return 'Egalitate'
    elif rules[player_choice] == server_choice:
        return 'Jucătorul'
    else:
        return 'Serverul'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print('Serverul este pregătit să primească conexiuni.')

while True:
    client_socket, client_address = server_socket.accept()
    print(f'[Server] Conexiune acceptată de la {client_address}')

    client_socket.send('Trimite READY pentru a începe jocul.'.encode())

    rounds = 0
    winner = None

    while True:
        message = client_socket.recv(1024).decode()

        if message == 'READY':
            client_socket.send('Serverul este pregătit. Alege P, H sau F.'.encode())
            break
        else:
            client_socket.send('Trimite READY pentru a începe jocul.'.encode())

    while True:
        # Așteaptă mesaj de la client
        message = client_socket.recv(1024).decode()

        if message in ['P', 'H', 'F']:

            rounds += 1

            server_choice = random.choice(['P', 'H', 'F'])

            result = get_winner(message, server_choice)

            client_socket.send(f'Serverul a ales {server_choice}. {result} câștigă runda {rounds}.'.encode())

            # Verificare dacă jocul este terminat
            if rounds == 3:
                if result == 'Egalitate':
                    client_socket.send('Jocul s-a încheiat cu rezultat egal.'.encode())
                else:
                    client_socket.send(f'Jocul s-a încheiat. {result} a câștigat în {rounds} runde.'.encode())
                break
            else:
                # Așteaptă comanda pentru a continua
                client_socket.send('Trimite READY pentru a continua sau altă comandă pentru a încheia jocul.'.encode())
        else:
             client_socket.send('Nu există o astfel de variantă. Verificați și introduceți din nou.'.encode())

    # Așteaptă comanda pentru un joc nou
    new_game_command = client_socket.recv(1024).decode()
    if new_game_command == 'READY':
        continue
    else:
        break
server_socket.close()
