import socket
import struct


class KafkaBroker:
    def __init__(self, host: str = "localhost", port: int = 9092):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"KafkaBroker listening on {self.host}:{self.port}")

    def handle_client(self, client_socket: socket.socket):
        try:
            while True:
                # Read the request size
                request_size_data = client_socket.recv(4)
                if not request_size_data:
                    break
                request_size = struct.unpack(">I", request_size_data)[0]
                print(request_size)

                # Read the request data
                request_data = client_socket.recv(request_size)
                if not request_data:
                    break
                # Handle APIVersions request (API key 18)
                print(request_data)

                api_key, _, correlation_id, client_id_len = struct.unpack(
                    ">hhih", request_data[:10]
                )
                print(api_key, _, correlation_id, client_id_len)
                client_string = request_data[10 : 10 + client_id_len].decode("utf-8")
                print(client_string)

                if api_key == 18:
                    self.handle_api_versions(client_socket, correlation_id)
                else:
                    print(f"Unsupported API key: {api_key}")

        finally:
            client_socket.close()

    def handle_api_versions(self, client_socket: socket.socket, correlation_id: int):
        # APIVersions response
        error_code = 0
        api_keys = [
            # (0, 0, 2),  # (api_key, min_version, max_version)
            (1, 16, 0),
        ]
        throttle_time_ms = 0

        api_keys_data = b""
        for api_key, min_version, max_version in api_keys:
            api_keys_data += struct.pack(">hhh", api_key, min_version, max_version)

        api_versions_response = (
            struct.pack(">ihh", correlation_id, error_code, len(api_keys))
            + api_keys_data
            + struct.pack(">i", throttle_time_ms)
        )

        client_socket.sendall(
            struct.pack(">I", len(api_versions_response)) + api_versions_response
        )

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            self.handle_client(client_socket)


if __name__ == "__main__":
    broker = KafkaBroker()
    broker.start()
