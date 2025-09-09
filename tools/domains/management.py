import os
from .models import Domain

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