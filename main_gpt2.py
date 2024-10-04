from transformers import GPT2LMHeadModel
import torch

from transformers import PreTrainedTokenizerFast

model_name = "skt/kogpt2-base-v2"

tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name,
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>')

# 한국어 GPT-2 모델 로드 (Hugging Face에서 제공하는 한국어 모델 사용)
model = GPT2LMHeadModel.from_pretrained(model_name)


def generate_response(prompt):
    # 텍스트 생성
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1, do_sample=True)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


def extract_info(text):
    # 특정 질문을 통해 정보 추출
    prompt = f"{text}: 장소와 시간을 알려줘."
    print(prompt)
    prompt = "날씨 정보"
    response = generate_response(prompt)

    return response


# 테스트 문장
text = "내일 서울에서 날씨가 어떨까요?"
response = extract_info(text)

print(f"응답: {response}")