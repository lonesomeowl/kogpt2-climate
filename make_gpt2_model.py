import pandas as pd
from transformers import AutoTokenizer, TextDataset, DataCollatorForLanguageModeling, AutoModelForCausalLM, pipeline, \
                         Trainer, TrainingArguments
from datasets import Dataset

MODEL = 'gpt2'

tokenizer = AutoTokenizer.from_pretrained(MODEL)  # load up a standard gpt2 model

tokenizer.pad_token = tokenizer.eos_token  # set the pad token to avoid a warning

file_name = '~/projects/quick-start-guide-to-llms/data/english_to_latex.csv'

data = pd.read_csv(file_name)

print(data.shape)

CONVERSION_PROMPT = 'Convert English to LaTeX\n'  # LaTeX conversion task

CONVERSION_TOKEN = 'LaTeX:'


# This is our "training prompt" that we want GPT2 to recognize and learn
training_examples = f'{CONVERSION_PROMPT}English: ' + data['English'] + '\n' + CONVERSION_TOKEN + ' ' + data['LaTeX'].astype(str)

task_df = pd.DataFrame({'text': training_examples})

task_df.head(2)

# adding the EOS token at the end so the model knows when to stop predicting

task_df['text'] = task_df['text'].map(lambda x: f'{x}{tokenizer.eos_token}')

latex_data = Dataset.from_pandas(task_df)  # turn a pandas DataFrame into a Dataset


def preprocess(examples):
    # tokenize our text but don't pad because our collator will pad for us dynamically
    return tokenizer(examples['text'], truncation=True)


latex_data = latex_data.map(preprocess, batched=True)

latex_data = latex_data.train_test_split(train_size=.8)

print(latex_data['train'][0])

# standard data collator for auto-regressive language modelling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

latex_gpt2 = AutoModelForCausalLM.from_pretrained(MODEL)

print(latex_data)

training_args = TrainingArguments(
    output_dir="./english_to_latex",
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
    model=latex_gpt2,
    args=training_args,
    train_dataset=latex_data["train"],
    eval_dataset=latex_data["test"],
    data_collator=data_collator,
)

trainer.evaluate()

trainer.train()

trainer.save_model()

book_data = TextDataset(
    tokenizer=tokenizer,
    file_path='./data/latex-guide-cos423.txt',  # train on a LaTeX cheat sheet they made
    block_size=128
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False,  # MLM is Masked Language Modelling
)

latex_gpt2 = AutoModelForCausalLM.from_pretrained(MODEL)

training_args = TrainingArguments(
    output_dir="./math_book",
    overwrite_output_dir=True, # overwrite the content of the output directory
    num_train_epochs=10, # number of training epochs
    per_device_train_batch_size=2, # batch size for training
    per_device_eval_batch_size=32,  # batch size for evaluation
    load_best_model_at_end=True,
    logging_steps=10,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    use_mps_device=True
)

trainer = Trainer(
    model=latex_gpt2,
    args=training_args,
    data_collator=data_collator,
    train_dataset=book_data.examples[:int(len(book_data.examples)*.8)],
    eval_dataset=book_data.examples[int(len(book_data.examples)*.8):]
)

trainer.evaluate()

trainer.train()

trainer.save_model()

# load up our gpt pre-trained on latex cheat sheets
math_latex_gpt2 = AutoModelForCausalLM.from_pretrained('./math_book')

training_args = TrainingArguments(
    output_dir="./math_english_to_latex",
    overwrite_output_dir=True, #overwrite the content of the output directory
    num_train_epochs=5, # number of training epochs
    per_device_train_batch_size=1, # batch size for training
    per_device_eval_batch_size=20,  # batch size for evaluation
    load_best_model_at_end=True,
    logging_steps=5,
    log_level='info',
    evaluation_strategy='epoch',
    save_strategy='epoch',
    use_mps_device=True
)

trainer = Trainer(
    model=math_latex_gpt2,
    args=training_args,
    train_dataset=latex_data["train"],
    eval_dataset=latex_data["test"],
    data_collator=data_collator,
)

trainer.evaluate()  # loss is starting slightly lower than before

trainer.train()

trainer.save_model()  # save this model

