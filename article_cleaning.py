import re

def article_cleaning(string):
    # string에 cleaning 할 문장을 넣는다.
    # string의 특수문자 제거
    string = re.sub('[-=+#/\:^$@*\※~&ㆍ『』「」\\|\(\)\[\]\<\>\…》▶→]',' ', string)
    string = re.sub('↑','상승',string)
    string = re.sub('↓','하락',string)
    string = re.sub("\n", "", string)
    string = re.sub("\r", "", string)
    
    # 한글, 영어빼고 나머지는 다 삭제
    string = re.sub('[^a-zA-Z가-힣\s.0-9]','',string)
    # 클렌징이 되서 나온걸 결과값으로 가져온다.
    return string.lstrip().strip()
