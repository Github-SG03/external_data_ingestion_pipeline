def test_sqlserver_source_config():
    source = {"type": "sqlserver", "table": "sales", "s3_prefix": "sqlserver/sales"}
    assert source["type"] == "sqlserver"
