import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")
model = AutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine", from_tf=True)

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).tolist()[0]
    positive_probability = probabilities[1]
    return positive_probability