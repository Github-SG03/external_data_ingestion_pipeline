import pandas as pd

def test_empty_df_fails():
    df = pd.DataFrame()
    assert df.empty
