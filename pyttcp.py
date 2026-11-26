
import socket
import threading

class TCPServer:
    def __init__(self, host="0.0.0.0", port=22222):
        self.host = host
        self.port = port
        self.running = False
        self.sock = None

    def start(self):
        if self.running:
            return

        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.running = True

        print(f"TCP Server running on {self.host}:{self.port}")

        threading.Thread(
            target=self.accept_clients,
            daemon=True
        ).start()

    def accept_clients(self):
        while self.running:
            try:
                client, address = self.sock.accept()

                threading.Thread(
                    target=self.handle_client,
                    args=(client, address),
                    daemon=True
                ).start()

            except OSError:
                break

    def handle_client(self, client, address):
        print("Client connected:", address)

        with client:
            while self.running:
                try:
                    data = client.recv(2048)

                    if not data:
                        break

                    message = data.decode(
                        "utf-8", errors="replace"
                    )

                    print("Received:", message)

                    response = (
                        f"Hello {address}! "
                        f"I got this from you: '{message}'"
                    )

                    client.sendall(
                        response.encode("utf-8")
                    )

                except OSError:
                    break

        print("Client disconnected:", address)

    def stop(self):
        self.running = False

        if self.sock:
            self.sock.close()
            self.sock = None
