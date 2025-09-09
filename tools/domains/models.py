class Domain:
    name      = None
    sock_path = None

    def __init__(self, name, sock_path):
        self.name      = name
        self.sock_path = sock_path