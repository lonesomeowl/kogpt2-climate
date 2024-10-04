import datetime
from data_read import get_location_list


def get_diff_day_from_today(dt):
    t = datetime.datetime.now()
    today = datetime.datetime(t.year, t.month, t.day)

    time_delta = dt - today

    # print(f'{today}, {dt}, 차이: {time_delta.days}')
    return time_delta.days


def available_location(location):
    loc_list = get_location_list()
    return location in loc_list


def available_date_time(dt):
    days = get_diff_day_from_today(dt)
    if days > 1 or days < -60:  # 내일 날씨를 구할 수 없었음
        return False
    return True


def validate_each(location, dt):
    res = available_location(location)
    if not res:
        return False, f"{location}는 지원하지 않는 지역 입니다."

    res = available_date_time(dt)
    if not res:
        return False, f"{location}는 지원하지 않는 시간 입니다."

    return True, ''


def validate(info_dict):
    if info_dict:
        if "location" in info_dict and "date" in info_dict:
            return validate_each(info_dict['location'], info_dict['date'])

    return False, '정보가 정확하지 않습니다. 다시 입력하세요'


if __name__ == '__main__':
    t = datetime.datetime(2024, 10, 3)
    res = available_date_time(t)
    print(t, res)
