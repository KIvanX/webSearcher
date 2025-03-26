import nltk
from nltk.corpus import stopwords
import pymorphy2


nltk.download('punkt_tab')
nltk.download('stopwords')

morph = pymorphy2.MorphAnalyzer()
stop_words = set(stopwords.words()).union({'-'})
available_simbols = {chr(i) for c0, c1 in [('a', 'z'), ('а', 'я'), ('-', '-')] for i in range(ord(c0), ord(c1) + 1)}

for i in range(100):
    with open(f'static/pages/page_{i}.txt', 'r', encoding='utf-8') as f:
        text = f.read().lower()

    words = nltk.word_tokenize(text)
    tokens = {word for word in words if not word in stop_words and not [c for c in word if c not in available_simbols]}
    lemmatized_words = {morph.parse(word)[0].normal_form for word in tokens}
    lemma_to_tokens = {l: [] for l in lemmatized_words}
    for word in tokens:
        lemma_to_tokens[morph.parse(word)[0].normal_form].append(word)

    with open(f'static/tokens/tokens_{i}.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(tokens))

    with open(f'static/lemmas/lemmas_{i}.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join([f'{k}: {", ".join(v)}' for k, v in lemma_to_tokens.items()]))
