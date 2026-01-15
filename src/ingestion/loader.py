import requests

def fetch_github_repo(owner: str, repo: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
