from src.ingestion.loader import fetch_github_repo #type: ignore

def test_fetch_github_repo():
    data = fetch_github_repo("apache", "airflow")
    assert "full_name" in data
