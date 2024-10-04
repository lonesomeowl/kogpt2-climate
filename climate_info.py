import datetime
import json
import os

import requests
from urllib.request import urlopen

from bs4 import BeautifulSoup

from data_read import get_grid_info, location_asos_dict
from make_sentence import make_sentence
from validator import get_diff_day_from_today

service_key = os.environ.get('DATA_GO_KR_KEY', '')

short_forecast_dict = {
    "POP":	{'name': "강수확률", "unit":	"%", "type": "int"},
    "RN1":	{'name': "1시간 강수량", "unit": "mm", "type": "int"},
    "PTY":	{'name': "강수형태", "unit": "코드값", "type": "string"},
    "PCP":	{'name': "1시간 강수량	범주", "unit":	"(1 mm)", "type": "int"},
    "REH":	{'name': "습도", "unit":	"%", "type": "int"},
    "SNO":	{'name': "1시간 신적설", "unit": "범주(1 cm)", "type": "int"},
    "SKY":	{'name': "하늘상태", "unit": "코드값", "type": "string"},
    "T1H":	{'name': "기온", "unit": "℃", "type": "float"},
    "TMP":	{'name': "1시간 기온", "unit": "℃", "type": "float"},
    "TMN":	{'name': "일 최저기온", "unit": "℃", "type": "float"},
    "TMX":	{'name': "일 최고기온", "unit": "℃", "type": "float"},
    "UUU":	{'name': "풍속(동서성분)", "unit":	"m/s", "type": "int"},
    "VVV":	{'name': "풍속(남북성분)", "unit":	"m/s", "type": "int"},
    "WAV":	{'name': "파고", "unit":	"M", "type": "int"},
    "VEC":	{'name': "풍향", "unit":	"deg", "type": "int"},
    "WSD":	{'name': "풍속", "unit":	"m/s", "type": "float"},
}


mid_climate_forecast_with_data_url = f'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList?serviceKey={service_key}'
mid_climate_forecast_url = f'http://apis.data.go.kr/1360000/MidFcstInfoService/getMidFcst?serviceKey={service_key}'
short_climate_forecast_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey={service_key}'


def get_mid_climate_forecast_with_data_info(station_id, date_time):
    before_day = date_time - datetime.timedelta(days=1)
    day_str = date_time.strftime('%Y-%m-%d')
    start_date_str = before_day.strftime('%Y%m%d')
    end_date_str = date_time.strftime('%Y%m%d')
    url = (f'{mid_climate_forecast_with_data_url}&pageNo=1&numOfRows=10&dataCd=ASOS&dateCd=DAY&dataType=XML'
           f'&startDt={start_date_str}&endDt={end_date_str}&stnIds={station_id}')

    result = urlopen(url)

    res = BeautifulSoup(result, 'xml')

    items = res.find_all("item")
    info_dict = dict()
    for item in items:
        tmp = dict()
        for el in item:
            if el.text:
                tmp[el.name] = el.text

        if 'tm' in tmp:
            info_dict[tmp['tm']] = tmp

    if day_str in info_dict:
        return True, info_dict[day_str]

    return False, None


def get_mid_climate_forecast_info(station_id, date_time):
    date_time_str = date_time.strftime('%Y%m%d0600')
    print(date_time_str)
    url = f'{mid_climate_forecast_url}&pageNo=1&numOfRows=10&dataType=XML&stnId={station_id}&tmFc={date_time_str}'

    print(url)
    result = urlopen(url)

    res = BeautifulSoup(result, 'xml')

    print(res)
    items = res.find_all("item")
    print(len(items))
    for item in items:
        print(item)


def get_short_climate_forecast_info(nx, ny, date_time):
    base_date = date_time.strftime('%Y%m%d')
    base_time = date_time.strftime('0600')
    print(base_date, base_time)

    url = (f'{short_climate_forecast_url}&pageNo=1&numOfRows=9999&dataType=json&stnId=108&base_date={base_date}'
           f'&base_time={base_time}&nx={nx}&ny={ny}')

    try:
        response = requests.get(url, verify=False)
        res = json.loads(response.text)

        result_code = res['response']['header']['resultCode']
        info_dict = dict()
        if int(result_code) != 0:
            return False, info_dict

        for items in res['response']['body']['items']['item']:
            category = items['category']
            v = items['obsrValue']

            info_dict[category] = v

        return True, info_dict
    except Exception as e:
        print(e)
        return False, dict()


def get_climate_forecast_info(res_dict):
    location = res_dict['location']
    dt = res_dict['date']

    # 분기를 타야 한다.
    diff_days = get_diff_day_from_today(dt)
    print(dt, diff_days)
    if diff_days == 0:
        print('======== 기상청_단기예보 ((구)_동네예보) 조회서비스 ==========')
        res, nx, ny = get_grid_info(location)
        if not res:
            return dict()

        res, _dict = get_short_climate_forecast_info(nx, ny, dt)
        if res:
            res_dict['climate_info'] = _dict
            return make_sentence(res_dict)

    else:
        print('======== 기상청_지상(종관, ASOS) 일자료 조회 ==========')
        station_id = location_asos_dict.get(location, 108)
        res, _dict = get_mid_climate_forecast_with_data_info(station_id, dt)
        if res:
            res_dict['climate_info'] = _dict
            return make_sentence(res_dict, short_forecast=False)

    return "날씨 정보를 읽어 오는 데 실패했습니다."


if __name__ == '__main__':
    dt = datetime.datetime.now() - datetime.timedelta(days=10)
    # for i in range(0, 2):
    #     mod_dt = dt - datetime.timedelta(days=i)
    #     print(f'==== {mod_dt} =====')
    #     # get_mid_climate_forecast_info(dt)
    #     _dict = get_short_climate_forecast_info('서울', mod_dt)
    #     if len(_dict) > 0:
    #         for k, v in _dict.items():
    #             print(mod_dt, k, v)
    #     else:
    #         print(f'{mod_dt} - Failed')

    dt = datetime.datetime(2024, 10, 12)
    # get_mid_climate_forecast_info(dt)
    # ans_dict = dict()
    # ans_dict['location'] = '서울'
    # ans_dict['date_str'] = '내일'
    # ans_dict['time'] = dt
    #
    # _dict = get_climate_forecast_info(ans_dict)
    # print(_dict)

    station_id = 108
    # get_mid_climate_forecast_info(station_id, dt)

    # res, info_dict = get_mid_climate_forecast_with_data_info(station_id, dt)
    # if res:
    #     for k, v in info_dict.items():
    #         print(k, v)
    #
    nx = 60
    ny = 127
    dt = datetime.datetime(2024, 10, 4)

    get_short_climate_forecast_info(nx, ny, dt)
