from transformers import GPT2LMHeadModel
import pandas as pd
from datasets import Dataset
from transformers import PreTrainedTokenizerFast
from transformers import DataCollatorForLanguageModeling, AutoModelForCausalLM, pipeline, \
                         Trainer, TrainingArguments

model_name = "skt/kogpt2-base-v2"

tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name,
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>')

# 한국어 GPT-2 모델 로드 (Hugging Face에서 제공하는 한국어 모델 사용)
kogpt2_model = GPT2LMHeadModel.from_pretrained(model_name)

# 데이터 읽기
file_name = './data/climate_sentence.csv'

data = pd.read_csv(file_name)

print(data.shape)

CONVERSION_PROMPT = 'Get Location, Time From Sentence\n'  # LaTeX conversion task

CONVERSION_TOKEN = 'Info:'


# This is our "training prompt" that we want GPT2 to recognize and learn
training_examples = f'{CONVERSION_PROMPT}Sentence: ' + data['Sentence'] + '\n' + CONVERSION_TOKEN + ' ' + data['Info'].astype(str)

task_df = pd.DataFrame({'text': training_examples})

task_df.head(2)

# adding the EOS token at the end so the model knows when to stop predicting

task_df['text'] = task_df['text'].map(lambda x: f'{x}{tokenizer.eos_token}')

info_data = Dataset.from_pandas(task_df)  # turn a pandas DataFrame into a Dataset


def preprocess(examples):
    # tokenize our text but don't pad because our collator will pad for us dynamically
    return tokenizer(examples['text'], truncation=True)


info_data = info_data.map(preprocess, batched=True)

info_data = info_data.train_test_split(train_size=.8)

print(info_data['train'][0])

# standard data collator for auto-regressive language modelling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./info_from_sentence",
    overwrite_output_dir=True, # overwrite the content of the output directory
    num_train_epochs=5, # number of training epochs
    per_device_train_batch_size=1, # batch size for training
    per_device_eval_batch_size=20,  # batch size for evaluation
    load_best_model_at_end=True,
    logging_steps=5,
    log_level='info',
    eval_strategy='epoch',
    save_strategy='epoch',
    # use_mps_device=True
)

trainer = Trainer(
    model=kogpt2_model,
    args=training_args,
    train_dataset=info_data["train"],
    eval_dataset=info_data["test"],
    data_collator=data_collator,
)

trainer.evaluate()

trainer.train()

trainer.save_model()
