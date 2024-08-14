import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('server', 9999))

    while True:
        mensage = client.recv(1024).decode()
        print(mensage)

        if "Game Over" in mensage:
            break

        if 'Possible moves' in mensage:
            move = input("Enter your move (0-8): ")
            client.send(move.encode())

    client.close()

if __name__ == "__main__":
    main()
