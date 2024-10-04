import validator
from climate_info import get_climate_forecast_info
from info_from_sentence import InfoExtruder

if __name__ == "__main__":
    # 클래스 인스턴스 생성
    info_extruder = InfoExtruder()

    # 테스트 문장
    text_sample = '서울 어제 날씨는 어떨까요?'

    # 정보 추출 및 출력
    result = info_extruder.extract_info(text_sample)
    print(text_sample)
    print(f"추출된 정보: {result}")

    res, data = validator.validate(result)
    if res:
        result_str = get_climate_forecast_info(result)
        print(result_str)
    else:
        print(data)

