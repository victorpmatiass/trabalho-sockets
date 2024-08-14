import socket
import threading

clients = []
board = [' ' for _ in range(9)]
current_player = 1
lock = threading.Lock()
game_over = False 

def print_board():
    return (f"{board[0]}|{board[1]}|{board[2]}\n"
            f"-+-+-\n"
            f"{board[3]}|{board[4]}|{board[5]}\n"
            f"-+-+-\n"
            f"{board[6]}|{board[7]}|{board[8]}\n")

def check_winner():
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for (x, y, z) in win_conditions:
        if board[x] == board[y] == board[z] != ' ':
            return board[x]
    if ' ' not in board:
        return 'Tie'
    return None

def handle_client(client_socket, player_number):
    global current_player, game_over

    while not game_over:
        with lock:
            if current_player != player_number:
                continue

            client_socket.send(print_board().encode())
            possible_moves = ','.join(str(i) for i, spot in enumerate(board) if spot == ' ')
            client_socket.send(f"Possible moves: {possible_moves}".encode())

            move = int(client_socket.recv(1024).decode())
            if board[move] == ' ':
                board[move] = 'X' if player_number == 1 else 'O'
                winner = check_winner()
                if winner:
                    for client in clients:
                        client.send(print_board().encode())
                        if winner == 'Tie':
                            client.send("Game Over: It's a Tie!".encode())
                        else:
                            client.send(f"Game Over: Player {winner} wins!".encode())

                    game_over = True
                    break  

                current_player = 1 if current_player == 2 else 2
    client_socket.close()

def main():
    global game_over
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(2)

    print("Server started. Waiting for players to connect...")
    while not game_over and len(clients) < 2:
        server.settimeout(1)
        try:
            client_socket, addr = server.accept()
            clients.append(client_socket)
            print(f"Player {len(clients)} connected from {addr}")
            if len(clients) == 1:
                client_socket.send("Waiting for a second player...".encode())
            else:
                for client in clients:
                    client.send("Game start! Player 1 starts.".encode())
                threading.Thread(target=handle_client, args=(clients[0], 1)).start()
                threading.Thread(target=handle_client, args=(clients[1], 2)).start()
        except socket.timeout:
            continue
    print("Server shutting down.")
    server.close()

if __name__ == "__main__":
    main()
