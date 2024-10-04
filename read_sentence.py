import dateparser
from konlpy.tag import Kkma

from data_read import get_location_list

kkma = Kkma()


def extract_location(text):
    # KoNLPy로 명사 추출 (장소 정보는 일반적으로 명사로 표현)
    nouns = kkma.nouns(text)

    # 장소 관련 사전 (예: 실제 장소 이름이 들어간 키워드 리스트)
    location_keywords = get_location_list()

    # 명사 중에서 장소와 관련된 명사 필터링
    locations = [noun for noun in nouns if noun in location_keywords]

    return locations


def extract_time_from_sentence(text):
    nouns = kkma.nouns(text)

    print(nouns)
    date_list = []
    for n in nouns:
        res, dt = extract_time_from_noun(n)
        if res:
            print(n, dt)
            date_list.append(dt)

    return date_list


def extract_time_from_noun(n):
    # dateparser를 이용해 시간 추출
    date_time = dateparser.parse(n, languages=['ko'])
    if date_time:

        return True, date_time

    return False, None
