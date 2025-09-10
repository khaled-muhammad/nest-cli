import os
import subprocess
import ssl, socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from .models import Domain, DomainSSLInfo

def listDomains():
    domains = []
    output  = os.popen('nest caddy list').read().splitlines()

    for line in output:
        _, name, sock_path = line.replace("(", "").replace(")", "").split()

        domains.append(Domain(
            name=name,
            sock_path=sock_path
        ))

    return domains

def getSSLInfo(domain):
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
        s.settimeout(5)
        s.connect((domain, 443))
        der_cert = s.getpeercert(True)
        cert = x509.load_der_x509_certificate(der_cert, default_backend())
        return  DomainSSLInfo(
            subject=cert.subject.rfc4514_string(),
            issuer=cert.issuer.rfc4514_string(),
            expiry=cert.not_valid_after_utc,
            issued=cert.not_valid_before_utc,
        )

def addDomain(domain):
    result = subprocess.run(
        ["nest", "caddy", "add", domain],
        capture_output=True,
        text=True
    )
    output = result.stdout + result.stderr

    if "This domain already has already been taken" in output:
        return False, "Domain already exists."
    if "not verified" in output:
        return False, "Domain is not verified. Please make sure to verify your domain."

    return True, "Domain added successfully."

def removeDomain(domain):
    os.system(f'nest caddy rm {domain}')