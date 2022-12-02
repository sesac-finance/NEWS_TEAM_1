import re

def article_cleaning(string):
    
    # 한글, 영어빼고 나머지는 다 삭제
    string = re.sub('[^a-zA-Z가-힣\s.,]','',string)
    # 클렌징이 되서 나온걸 결과값으로 가져온다.
    return string.lstrip().strip()
