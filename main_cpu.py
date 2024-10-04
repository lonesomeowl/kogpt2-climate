from read_sentence import extract_location, extract_time_from_sentence, extract_time_from_noun

# 테스트 예시
text = "3주 후 서울에서 날씨가 어떨까요"

# 장소 및 시간 추출
locations = extract_location(text)
time = extract_time_from_sentence(text)

print(f"명사(장소 후보): {locations}")
print(f"시간: {time}")

res, time = extract_time_from_noun('3주 후')
if res:
    print(f"시간: {time}")

# info = get_climate_info(locations, time)

