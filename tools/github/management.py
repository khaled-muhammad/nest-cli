import json
import os, subprocess, sys

from .models import *

def check_if_github_logged_in():
    result = subprocess.run(
        ["gh", "auth", "status"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0

def github_auth():
    os.system("gh auth login")

    return check_if_github_logged_in()

def github_logout():
    os.system("gh auth logout")

    return check_if_github_logged_in()

if __name__ == '__main__':
    print(check_if_github_logged_in())


def list_repos(lim=30):
    res = subprocess.run(
        ["gh", "repo", "list", "--json", "name,sshUrl,url", f"--limit={lim}"],
        capture_output=True,
        text=True
    )

    try:
        repos = [Repo.from_json(repo) for repo in json.loads(res.stdout)]
    except:
        print(res.stderr)
        sys.exit()

    return repos

def clone_repo(repo:Repo, save_path):
    os.system(f"git clone {repo.sshUrl if isinstance(repo, Repo) else repo} {save_path}")


def create_repo(name, visibility='public', description=None, local_path=None):
    cmd = ["gh", "repo", "create", name, f"--{visibility}"]

    if description:
        cmd.append("--description", description)
    

    if local_path != None:
        cmd.append(f"--source={local_path}")
        cmd.append("--push")

    subprocess.run(cmd)