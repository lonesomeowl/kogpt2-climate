import datetime

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, PreTrainedTokenizerFast

from read_sentence import extract_time_from_noun


class InfoExtruder:
    def __init__(self, model_name="skt/kogpt2-base-v2", model_path="./info_from_sentence"):
        # 설정 및 토크나이저 로드
        self.CONVERSION_PROMPT = 'Get Location, Time From Sentence\n'  # 기본 프롬프트
        self.CONVERSION_TOKEN = 'Info:'  # 토큰
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name,
                                                                 bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                                 pad_token='<pad>', mask_token='<mask>')
        self.tokenizer.pad_token = self.tokenizer.eos_token  # 패딩 토큰 설정
        # 모델 로드
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        # 파이프라인 설정
        self.info_extruder = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)

    def extract_info(self, text_sample):
        # 입력 텍스트 구성
        conversion_text_sample = f'{self.CONVERSION_PROMPT}Sentence: {text_sample}\n{self.CONVERSION_TOKEN}'
        # 정보 추출
        result = self.info_extruder(
            conversion_text_sample, num_beams=2, early_stopping=True, temperature=0.7,
            max_new_tokens=24
        )

        txt = result[0]['generated_text']
        print(txt)
        try:
            txt = txt.split('Info:')[-1]
            res_dict = dict()
            if '_' in txt:
                ii = txt.split('_')
                location = ii[0]
                date_time = ii[1]
                res_dict['location'] = location.strip()
                res_dict['date_str'] = date_time
                res, dt = extract_time_from_noun(date_time)
                if res:
                    dt = datetime.datetime(dt.year, dt.month, dt.day)
                    print(f"{date_time} ==> 시간: {dt}")
                    dt = datetime.datetime(dt.year, dt.month, dt.day)
                    res_dict['date'] = dt

            return res_dict
        except Exception as e:
            return dict()


if __name__ == "__main__":
    # 클래스 인스턴스 생성
    info_extruder = InfoExtruder()

    # 테스트 문장
    text_sample = '서울 모레 날씨는 어떨까요?'

    # 정보 추출 및 출력
    result = info_extruder.extract_info(text_sample)
    print(text_sample)
    print(f"추출된 정보: {result}")
