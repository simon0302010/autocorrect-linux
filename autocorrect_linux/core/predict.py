import os
from time import time

import numpy as np
from keras.models import load_model

from . import utils

os.environ["CUDA_VISIBLE_DEVICES"] = ""

model_path, vocab_path = utils.download_model()

model = load_model(model_path)
data = np.load(vocab_path, allow_pickle=True)
word2idx = data["word2idx"].item()
idx2word = data["idx2word"].item()
seq_lenght = 10


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds + 1e-8) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)


def predict_next_words(
    model, seed_text, word2idx, idx2word, seq_lenght, temperature=1.0
):
    words = seed_text.split()
    seq = [word2idx.get(w, 0) for w in words[-seq_lenght:]]
    if len(seq) < seq_lenght:
        seq = [0] * (seq_lenght - len(seq)) + seq
    x = np.array([seq])
    preds = model.predict(x, verbose=0)[0]
    next_idx = sample(preds, temperature)
    next_word = idx2word.get(next_idx, "")
    return next_word


def generate(base_text: str, outputs):
    if not base_text.endswith(" "):
        base_text += " "
    start_time = time()
    output = set()
    attempts = 0
    max_attempts = outputs * 3

    while len(output) < outputs and attempts < max_attempts:
        result = predict_next_words(
            model, base_text, word2idx, idx2word, seq_lenght=seq_lenght, temperature=0.8
        )
        output.add(result)
        attempts += 1

    result_list = list(output)
    while len(result_list) < outputs:
        result_list.append(None)

    print(f"took {round((time() - start_time) * 1000)}ms")
    return result_list


predict_next_words(
    model, "I ", word2idx, idx2word, seq_lenght=seq_lenght, temperature=0.8
)

if __name__ == "__main__":
    print(generate("I really like ", 3))
