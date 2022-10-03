import torch
from text_gen.lstm_nn.preprocessing_data import evaluate, word_to_idx, idx_to_word
from models import TextRNN


# from preprocessing_data import evaluate, word_to_idx, idx_to_word
# from text_gen.lstm_nn.models import TextRNN
from models import TextRNN

# model_load = torch.load('./text_gen/lstm_nn/weight/model_all')
model_load = torch.load('./text_gen/lstm_nn/weight/model_all')



def generate_blabla():
    predicted_text = evaluate(model_load, word_to_idx, idx_to_word)
    # print(predicted_text)