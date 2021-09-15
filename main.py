import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from googletrans import Translator
import tensorflow as tf
import wikipedia

import os
physical_devices = tf.config.list_physical_devices('GPU')

tf.config.experimental.set_memory_growth(physical_devices[0], True)
model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def gpu():
    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


def get_response(input_text,num_return_sequences):


  batch = tokenizer.prepare_seq2seq_batch([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = model.generate(**batch,max_length=60,num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text


def prepare_model():
    model_name = 'tuner007/pegasus_paraphrase'
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)



def prepare_data(path_to_data, filename):
    with open(path_to_data, 'r') as file:
        data = file.read().replace('\n', '')

    context = str(data)

    from sentence_splitter import SentenceSplitter, split_text_into_sentences

    splitter = SentenceSplitter(language='en')

    sentence_list = splitter.split(context)
    print(sentence_list)

    paraphrase = []

    for i in sentence_list:
      a = get_response(i,1)
      paraphrase.append(a)

    paraphrase2 = [' '.join(x) for x in paraphrase]
    paraphrase2

    paraphrase3 = [' '.join(x for x in paraphrase2) ]
    paraphrased_text = str(paraphrase3).strip('[]').strip("'")

    print(paraphrased_text)

    with open(filename + ".txt", "w") as text_file:
        text_file.write(paraphrased_text)


def write(query, filename):

    results = str(wikipedia.summary(query))

    with open('data.txt', "w") as text_file:
        text_file.write(results)

    print(prepare_data('data.txt', filename))


def find_subject():
    subject = input("What would you like me to write about sir? ")
    return str(subject)


def type_of_data():

    ch  = input('Do you want to bring in your own data')

    if "no" in ch:
        find_subject
