import numpy as np
from keras.models import load_model

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-8) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)

def predict_next_words(model, seed_text, word2idx, idx2word, seq_lenght, num_words=10, temperature=1.0):
    words = seed_text.lower().split()
    for _ in range(num_words):
        seq = [word2idx.get(w, 0) for w in words[-seq_lenght:]]
        if len(seq) < seq_lenght:
            seq = [0]*(seq_lenght - len(seq)) + seq
        x = np.array([seq])
        preds = model.predict(x, verbose=0)[0]
        next_idx = sample(preds, temperature)
        next_word = idx2word.get(next_idx, '')
        words.append(next_word)
    return ' '.join(words)

# Load model and vocab if needed
model = load_model('word_lstm_best.h5')
data = np.load('word_vocab.npz', allow_pickle=True)
word2idx = data['word2idx'].item()
idx2word = data['idx2word'].item()

seq_lenght = 10
seed = "I am very happy to be here today because I am very happy to annouce "
generated = predict_next_words(
    model, seed, word2idx, idx2word, seq_lenght=seq_lenght, num_words=1, temperature=0.8
)
print(generated)