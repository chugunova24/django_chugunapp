from transformers import *

# source & destination languages
# c ru на en
src_ru = "ru"
dst_ru = "en"
task_name_ru = f"translation_{src_ru}_to_{dst_ru}"
model_name_ru = f"Helsinki-NLP/opus-mt-{src_ru}-{dst_ru}"
translator_ru = pipeline(task_name_ru, model=model_name_ru, tokenizer=model_name_ru)

# c en на ru
src_en = "en"
dst_en = "ru"
task_name_en = f"translation_{src_en}_to_{dst_en}"
model_name_en = f"Helsinki-NLP/opus-mt-{src_en}-{dst_en}"
translator_en = pipeline(task_name_en, model=model_name_en, tokenizer=model_name_en)


class TranslatedText:
    def __init__(self, article):
        self.article = article

    def translate_en(self):
        return translator_en(self.article)[0]["translation_text"]

    def translate_ru(self):
        return translator_ru(self.article)[0]["translation_text"]


# obj = Translator(article).translate_ru()
# print(obj)