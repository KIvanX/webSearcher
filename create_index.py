import json

index = {}
for i in range(100):
    with open(f'static/lemmas/lemmas_{i}.txt') as f:
        lemmas = [l.split(':')[0] for l in f.read().split('\n')]
        for lemma in lemmas:
            if lemma not in index:
                index[lemma] = []
            index[lemma].append(i)

with open('static/index.json', 'w') as f:
    f.write(json.dumps(index, indent=4, ensure_ascii=False))
