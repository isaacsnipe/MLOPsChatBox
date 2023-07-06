from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import nltk


def gen_title(input_text):
    tokenizer = AutoTokenizer.from_pretrained(
        "deep-learning-analytics/automatic-title-generation"
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        "deep-learning-analytics/automatic-title-generation"
    )
    # input_text = "Your input text goes here."
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=20, num_beams=4, early_stopping=True)
    generated_title = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_title
