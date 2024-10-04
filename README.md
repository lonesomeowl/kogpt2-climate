# kogpt2-climate
kogpt2를 이용한 시간,  장소 정보 추출해서 날씨 정보 보여주기

사용한 python version : 3.8.10

# step 1
> pip install -r requirements.txt
> source venv/bin/activate

# step 2
모델 FineTuning하기

data/climate_sentence.csv를 가지고 문장에서 시간과 장소를 뽑아내는 모델을 튜닝함

> python model_kogpt2.py

이를 실행하면 ./info_from_sentence 라는 디렉토리가 생기고 모델이 저장됨

# Step 3
> python main.py

Sentence: 서울 어제 날씨는 어떨까요?

Info: 서울_어제

어제 ==> 시간: 2024-10-03 00:00:00

서울 어제 날씨는 어떨까요?

추출된 정보: {'location': '서울', 'date_str': '어제', 'date': datetime.datetime(2024, 10, 3, 0, 0)}

======== 기상청_지상(종관, ASOS) 일자료 조회 ==========

서울에서 어제 날씨는

평균 기온 는 16.4 입니다.

최저 기온 는 10.8 입니다.

최고 기온 는 22.5 입니다.

평균풍속 는 1.9 입니다.


