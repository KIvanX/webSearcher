"""
Суть алгоритма в том, чтобы преобразовать запрос в выражение над множествами,
где слова - это множество номеров релевантных страниц, а AND и OR это соответственно
пересечение и объединение множеств. Оператор NOT преобразуется в разность между
множеством всех страниц и исходным множеством.

Преобразованный запрос вычисляется с помощью встроенной функцией eval.
"""

import json

QUERY = 'image AND (NOT компьютер AND экран) OR (бит AND NOT(техника OR рюкзак))'


def operator_not(s):
    def find_end_staples(s0, i0):
        k, i0 = 1, i0 + 1
        while k and i0 < len(s0):
            k = (k + 1) if s0[i0] == '(' else (k - 1) if s0[i0] == ')' else k
            i0 += 1
        return i0

    def find_end(s0, i0):
        while s0[i0] not in [')', ' ', '&', '|', '_'] and i0 < len(s0):
            i0 += 1
        return i0

    for i in range(len(s)):
        if s[i] == '_':
            if s[i + 2] == '(':
                end = find_end_staples(s, i + 2)
                s = s[:end] + ')' + s[end:]
                s = s.replace('_ (', f'(ALL - (', 1)
            else:
                end = find_end(s, i + 2)
                s = s[:end] + ')' + s[end:]
                s = s.replace('_', f'(ALL -', 1)

    return s


raw_request_1 = QUERY.strip().replace('  ', ' ')
raw_request_2 = raw_request_1.replace('AND', ' & ').replace('OR', ' | ').replace('NOT', ' _ ')
request = raw_request_2.replace('  ', ' ').lower()

with open('static/index.json', 'r') as f:
    index = json.loads(f.read())
    index['ALL'] = [i for i in range(100)]

request = operator_not(request)
request_words = [w for w in request.replace('(', '').replace(')', '').split() if w and w not in ['&', '|', '-']]
for word in request_words:
    request = request.replace(word, str(set(index.get(word, []))))

result = list(eval(request))
print('Найденные страницы:', result)
