import json
from LAC import LAC
from pypinyin import pinyin, lazy_pinyin

with open('same_pinyin.json', encoding='utf-8') as f:
    same_pinyin = json.load(f)
    
def anteroposterior(word):
    word_py = lazy_pinyin(word)
    candidate = []

    for i, yin in enumerate(word_py):
        req = [yin]
        if yin.endswith('eng'):
            req.append(yin.strip('eng') + 'en')
        elif yin.endswith('en'):
            req.append(yin.strip('en') + 'eng')
        elif yin.endswith('ing'):
            req.append(yin.strip('ing') + 'in')
        elif yin.endswith('in'):
            req.append(yin.strip('in') + 'ing')

        if yin.startswith('zh'):
            req.append(yin.replace('zh', 'z'))
        elif yin.startswith('z'):
            req.append(yin.replace('z', 'zh'))
        elif yin.startswith('ch'):
            req.append('c' + yin.strip('ch'))
        elif yin.startswith('c'):
            req.append('ch' + yin.strip('c'))
        elif yin.startswith('sh'):
            req.append('s' + yin.strip('sh'))
        elif yin.startswith('s'):
            req.append('sh' + yin.strip('s'))

        candidate.append(req)

    requests = []
    for can in candidate:
        if len(can) == 1:
            if not requests:
                requests.append(can[0])
            else:
                for i, req in enumerate(requests):
                    requests[i] = req + '\t' + can[0]
        else:
            if not requests:
                requests = can
            else:
                length = len(requests)
                requests = requests*len(can)
                for i, c in enumerate(can):
                    for j in range(length):
                        requests[i*length+j] = requests[i*length+j] + '\t' + c
    return requests

def check_same_pinyin(word, anteroposterior_flag = True):
    requests = anteroposterior(word) if anteroposterior_flag else ['\t'.join(lazy_pinyin(word))]
    # same_pinyin_dict = same_pinyin_single if len(word) == 1 else same_pinyin_multi
    same_pinyin_dict = same_pinyin
    ret = []
    for req in requests:
        if req in same_pinyin_dict:
            ret += same_pinyin_dict[req]
    if word in ret:
        ret.remove(word)
    return ret

# example
word = '吃饭'
check_same_pinyin(word, True)