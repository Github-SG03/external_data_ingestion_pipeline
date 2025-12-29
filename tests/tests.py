def test_s3_path_generation():
    from github_pipeline.github_ingestion import build_s3_path
    assert "date=" in build_s3_path("2025-12-28")
