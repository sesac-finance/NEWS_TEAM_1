import pymysql
import pandas as pd
# to_do: 불러올 길이, 연결할 데이터 로그인 인자 받아오기 등 : 클래스화하기

class DB_data():
    def __init__(self, host:str, user:str, password:str, db:str, data_limit:int ):    #(호스트명, 유저아이디, 비밀번호, db명, 불어올 데이터 양) 설정
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.data_limit = data_limit

        conn, cur = None, None
        data1, data2, data3, data4 = "", "", "", ""
        row=None

    #DB 연결
    def DB_connect(self):
        #conn = pymysql.connect(host='localhost', user='root', password='1111', db='shopDB', charset='utf8')
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8')
        cur = conn.cursor()

        DB_data.DB_dataload(cur, self.data_limit)
        #result = print(DB_data.DB_dataload(cur, self.data_limit)) #return 값으로 받아 변수에 df 저장하는 방식

        conn.close()



    #DB 데이터 가져오기 
    def DB_dataload(cur, data_limit):
        sql1 = "SELECT * FROM userTable"
        sql2 = "select id, email from userTable"  #sql부에 조건 변경해서 가져올 데이터 설정(데이터 컬럼명, where 등 변경해야함)
        cur.execute(sql2)

        data_list = []
        data_len = 0
        while (data_len < data_limit) :
            # 루프를 돌면서 tuple 하나씩 가져오기
            row = cur.fetchone()
            #print(row)
            if row== None :
                break
            data1 = row[0]
            data2 = row[1]
            # data3 = row[2]
            # data4 = row[3]
            temp = data1, data2
            data_list.append(temp)
            data_len += 1
        #print(data_list)

        #데이터 프레임화 추가 (데이터 프레임화 필요없으면 리스트화도 그냥 제거하기)
        df = pd.DataFrame(data_list)
        df.columns = ['ID', 'Email']
        print(df)
        return df

DB_exc = DB_data('localhost', 'root', '1111', 'shopDB', 2)
DB_exc.DB_connect()

