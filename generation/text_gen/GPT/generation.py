# pip install transformers==4.12.4 sentencepiece
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)

class GPT:
  def __init__(self, input, min_length, max_length):
    self.input = input
    self.min_length = min_length
    self.max_length = max_length

  def get_sentence(self):
    input_ids = tokenizer.encode(self.input, return_tensors='pt')
    output = model.generate(input_ids,
                            min_length=self.min_length,
                            max_length=self.max_length,
                            num_beams=5,
                            no_repeat_ngram_size=2, top_k=50,
                            top_p=0.95, early_stopping=True)
    return tokenizer.decode(output[0], skip_special_tokens=True)


# input = 'Russian woman'
# min_length = 5
# max_length = 20
#
# # tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# # model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)
#
# obj = GPT(input, min_length, max_length)
# out = obj.get_sentence()

