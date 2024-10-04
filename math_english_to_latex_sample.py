from transformers import AutoModelForCausalLM, pipeline, AutoTokenizer

CONVERSION_PROMPT = 'Convert English to LaTeX\n'  # LaTeX conversion task

CONVERSION_TOKEN = 'LaTeX:'

MODEL = 'gpt2'

tokenizer = AutoTokenizer.from_pretrained(MODEL)  # load up a standard gpt2 model

tokenizer.pad_token = tokenizer.eos_token  # set the pad token to avoid a warning

loaded_model = AutoModelForCausalLM.from_pretrained('./math_english_to_latex')
latex_generator = pipeline('text-generation', model=loaded_model, tokenizer=tokenizer)

text_sample = 'sum from 1 to 10 of pi squared'
# text_sample = 'g of x equals integral from 0 to 1 of x squared'
conversion_text_sample = f'{CONVERSION_PROMPT}English: {text_sample}\n{CONVERSION_TOKEN}'

print(latex_generator(
    conversion_text_sample, num_beams=2, early_stopping=True, temperature=0.7,
    max_new_tokens=24
)[0]['generated_text'])
