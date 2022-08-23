import argparse
import json
from LAC import LAC
import paddle
from paddlenlp.transformers import T5ForConditionalGeneration, T5Tokenizer

from common import *


def parse_args():
    parse = argparse.ArgumentParser(description='T5 Model Prediction After Having Macbert Result')
    parse.add_argument('--model_name_or_path', type=str, required=True, help='Model name or path')

    parse.add_argument('--nezha_opt_dir', type=str, required=True, help='The dictionary of Nezha output data')

    parse.add_argument('--mac_opt_dir', type=str, required=True, help='The dictionary of Macbert output data')

    parse.add_argument('--save_dir', type=str, required=True, help='Final result save path')

    args = parse.parse_args()
    return args

def T5_predict(samples: list) -> list:
    res_t5_pre = []
    for text in samples:
        inputs = T5_tokenizer(text)
        inputs = {k:paddle.to_tensor([v]) for (k, v) in inputs.items()}
        output = T5_model.generate(**inputs)
        gen_text = T5_tokenizer.decode(list(output[0].numpy()[0]), skip_special_tokens=True)
        gen_text = gen_text.replace(',', '，')
        gen_text = gen_text.replace('?', '？')
        gen_text = gen_text.replace(';', '；')
        gen_text = gen_text.replace('!', '！')
        # 这里是补充生成文本不完整，可能会缺失后半部分文本
        gen_text.replace(gen_text[-3:], text[text.rfind(gen_text[-3:]):])
        gen_text = gen_text if text.rfind(gen_text[-3:]) == -1 else gen_text + text[text.rfind(gen_text[-3:])+3:]
        # 如果生成文本还是不完整，则不生成了
        if len(gen_text) < len(text) - 2:
            res_t5_pre.append(text)
        else:
            res_t5_pre.append(gen_text)
    
    return res_t5_pre


if __name__ == "__main__":
    args = parse_args()

    model_name = args.model_name_or_path
    T5_tokenizer = T5Tokenizer.from_pretrained(model_name)
    T5_model = T5ForConditionalGeneration.from_pretrained(model_name)

    with open(args.nezha_opt_dir, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    with open(args.mac_opt_dir, 'r', encoding='utf-8') as f:
        mac_data = json.load(f)

    res = []
    # 这里为了简单，就没有把同一种模型的调用合并成一个list
    for ori, mac in zip(raw_data, mac_data):
        assert ori['id'] == mac['id']
        if ori['source'] == mac['inference'] and ori['type'] == 'Semantic Error':
            source = remove_duplication(ori['source'])
            t5_res = T5_predict([source], T5_model_1)[0]
            flag, checked_t5_res = check_semantic_result(source, t5_res)
            res.append({'source': ori['source'],
                        'inference': checked_t5_res, 'id': ori['id'],
                        'model': 't5' if flag else 'none'})
        elif remove_duplication(mac['inference']) != mac['inference']:
        # elif if_duplication(mac['inference']): # val降了6个点
            source = remove_duplication(ori['source'])
            t5_res = T5_predict([source], T5_model_1)[0]
            flag, checked_t5_res = check_semantic_result(source, t5_res)
            res.append({'source': ori['source'],
                        'inference': checked_t5_res if flag else source, 'id': ori['id'],
                        'model': 't5' if flag else 'remove duplicate'})
        else:
            ori_lac, ori_type = lac.run(ori['source'])
            mac_lac, mac_type = lac.run(mac['inference'])
            if ori_type == mac_type:
                mac['model'] = 'none'
                mac['inference'] = ori['source']
                res.append(mac)
                continue
            mac['model'] = 'mac'
            res.append(mac)

    with open(args.save_dir, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)