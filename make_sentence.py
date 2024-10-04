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

mid_index_dict = {
    "sumRn": {"name": "일강수량", "unit": "mm"},
    "avgTa": {"name": "평균 기온", "unit": "℃"},
    "minTa": {"name": "최저 기온", "unit": "℃"},
    "maxTa": {"name": "최고 기온", "unit": "℃"},
    "avgWs": {"name": "평균풍속", "unit":	"m/s"}
}

sky_code = {
    1: '맑음',
    3: '구름많음',
    4: '흐림'
}

pty_code = {
    0: '없음',
    1: '비',
    2: '비/눈',
    3: '눈',
    4: '소나기'
}


def make_sentence(info_dict, short_forecast=True):
    date_str = info_dict.get('date_str', '')
    location = info_dict.get('location', '')
    info = info_dict.get('climate_info', '')

    if short_forecast:
        info_str = get_response(info)
    else:
        info_str = get_response_mid(info)
    return f'{location}에서 {date_str} 날씨는\n{info_str}'


def get_response(info):
    info_str_list = []
    if info:
        for k, v in info.items():
            if k in short_forecast_dict:
                unit_info = short_forecast_dict[k]
                if k == 'PTY':
                    unit_info_str = get_response_pty(v)
                else:
                    unit_info_str = f'{unit_info["name"]}는 {v} {unit_info["unit"]} 입니다.'

                if unit_info_str:
                    info_str_list.append(unit_info_str)

    if info_str_list:
        return '\n'.join(info_str_list)
    return ''


def get_response_mid(info):
    info_str_list = []
    if info:
        for k, v in info.items():
            if k in mid_index_dict:
                index_name = mid_index_dict[k]
                unit_info_str = f'{index_name["name"]} 는 {v} {index_name["unit"]} 입니다.'

                info_str_list.append(unit_info_str)

    if info_str_list:
        return '\n'.join(info_str_list)
    return ''


def get_response_pty(v, unit_info):
    v = int(v)
    pty_v = pty_code.get(v, '')
    if pty_v:
        return f'{unit_info["name"]}는 {pty_v} 입니다.'
    return pty_v
