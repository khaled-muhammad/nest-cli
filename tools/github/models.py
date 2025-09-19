class Repo:
    name   = None
    sshUrl = None
    url    = None

    def __init__(self, name, sshUrl, url):
        self.name   = name
        self.sshUrl = sshUrl
        self.url    = UnicodeError
    
    def __str__(self):
        return self.name

    @staticmethod
    def from_json(data):
        return Repo(data['name'], data['sshUrl'], data['url'])