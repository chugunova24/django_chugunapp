import pandas as pd
import re
import numpy as np

import torch
import torch.nn.functional as F

# TRAIN_TEXT_FILE_PATH = './encodeshit.txt'

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
TRAIN_TEXT_FILE_PATH = 'text_gen/lstm_nn/dataset/Book1.txt'

with open(TRAIN_TEXT_FILE_PATH) as text_file:
    text_sample = text_file.readlines()

text = []
for line in text_sample:
    i = re.findall(r'[0-9]+|[A-z]+|,|.|"|!', line)
    for h in i:
        if h != ' ':
            text.append(h)

text_in_line = ' '.join(text).lower()


def text_to_seq(text_in_line):
    word_counts = text_in_line.split()
    space = ' '

    sorted_words = list(set(word_counts))

    sorted_words.append(space)

    idx_to_word = {}
    number = 0
    for word in sorted_words:
        idx_to_word[number] = word  # idx_to_word
        number += 1

    word_to_idx = {}
    number = 0
    for word in sorted_words:
        word_to_idx[word] = number  # word_to_idx
        number += 1

    print(word_to_idx[' '])

    sequence = np.array([word_to_idx[word] for word in text_in_line.split()])

    return sequence, word_to_idx, idx_to_word


sequence, word_to_idx, idx_to_word = text_to_seq(text_in_line)



SEQ_LEN = 256
BATCH_SIZE = 16

def get_batch(sequence):
    trains = []
    targets = []
    for _ in range(BATCH_SIZE):
        batch_start = np.random.randint(0, len(sequence) - SEQ_LEN)
        chunk = sequence[batch_start: batch_start + SEQ_LEN]
        train = torch.LongTensor(chunk[:-1]).view(-1, 1)
        target = torch.LongTensor(chunk[1:]).view(-1, 1)
        trains.append(train)
        targets.append(target)
    return torch.stack(trains, dim=0), torch.stack(targets, dim=0)


def evaluate(model, char_to_idx, idx_to_char, start_text=' ', prediction_len=10, temp=0.3):
    hidden = model.init_hidden()
    idx_input = [word_to_idx[word] for word in start_text]
    train = torch.LongTensor(idx_input).view(-1, 1, 1).to(device)
    predicted_text = start_text

    '''
    idx_to_word
    word_to_idx
    '''

    _, hidden = model(train, hidden)

    inp = train[-1].view(-1, 1, 1)

    for i in range(prediction_len):
        output, hidden = model(inp.to(device), hidden)
        output_logits = output.cpu().data.view(-1)
        p_next = F.softmax(output_logits / temp, dim=-1).detach().cpu().data.numpy()
        top_index = np.random.choice(len(char_to_idx), p=p_next)
        inp = torch.LongTensor([top_index]).view(-1, 1, 1).to(device)
        predicted_char = idx_to_word[top_index]
        predicted_text += predicted_char + ' '

    return predicted_text