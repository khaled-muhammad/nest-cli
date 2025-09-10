class Domain:
    name      = None
    sock_path = None

    def __init__(self, name, sock_path):
        self.name      = name
        self.sock_path = sock_path

class DomainSSLInfo:
    subject = None
    issuer  = None
    expiry  = None
    issued  = None

    def __init__(self, subject, issuer, expiry, issued):
        self.subject = subject
        self.issuer  = issuer
        self.expiry  = expiry
        self.issued  = issued