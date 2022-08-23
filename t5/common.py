from LAC import LAC

# 装载LAC模型
lac = LAC(mode='lac')

def is_chinese(char):
    if char >= "\u4e00" and char <= "\u9fa5":
        return True
    else:
        return False

def check_chinese(zh):
    for char in zh:
        if not is_chinese(char):
            return False
    return True

def check_valid_duplication(candidate, text):
    tokens, characters = lac.run(text)
    ind = text.index(candidate)
    pointer = 0
    for token, next_token, charact in zip(tokens, tokens[1:], characters):
        pointer += len(token)
        if pointer > ind:
            if candidate*2 == token:
                return True
            elif candidate == next_token:
                return False
            elif token != next_token:
                return True
            else:
                return False

def if_duplication(text: str):
    '''
    不考虑是否可能是 valid duplication
    Return:
        flag (bool)
    '''
    length = len(text)
    for i in range(length):
        cp_range = min(i + 1, length - i - 1)
        j = 0
        flag = False
        candidate = ""
        for j in range(cp_range):
            if text[i - j:i + 1] == text[i + 1:i + 1 + j + 1]:
                candidate = text[i - j:i + 1]
                if not check_chinese(candidate):
                    continue
                flag = True
                break
        if flag:
            return flag
    return flag

def remove_duplication(text: str):
    length = len(text)
    for i in range(length):
        cp_range = min(i+1, length-i-1)
        j = 0
        flag = False
        candidate = ""
        for j in range(cp_range):
            if text[i-j:i+1] == text[i+1:i+1+j+1]:
                candidate = text[i-j:i+1]
                if not check_chinese(candidate):
                    continue
                if len(candidate) == 1 and check_valid_duplication(candidate, text):
                    continue
                flag = True
                break
        if flag:
            return text.replace(candidate, '', 1)

    return text

# NER检测
from paddlenlp import Taskflow

ner = Taskflow("ner")

def more_ner(source, target):
    # 看一下纠错后是否会增加实体个数
    source_ner = ner(source)
    target_ner = ner(target)
    if len(target_ner) > len(source_ner):
        return True
    return False

def check_misspelled_result(source, target):
    target = remove_duplication(target)
    if len(target) == len(source) and not more_ner(source, target):
        return True, target
    return False, source

def check_semantic_result(source, target):
    target = remove_duplication(target)
    if more_ner(source, target):
        return False, source
    return True, target