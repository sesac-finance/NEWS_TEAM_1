import pandas as pd
from pandas import DataFrame

# location 에 파일경로 설정
# df 로 해당 csv파일의 경로가 나온다.

def csv_dataframe(location):
    data = pd.read_csv(location)
    df = pd.DataFrame(data)
    return df


    