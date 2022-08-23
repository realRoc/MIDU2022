import argparse
import json
from paddlenlp.transformers import AutoModelForSequenceClassification, AutoTokenizer

from eval import predict


def parse_args():
    parse = argparse.ArgumentParser(description='T5 Model Prediction After Having Macbert Result')
    parse.add_argument('--model_name_or_path', type=str, required=True, help='Model name or path')

    parse.add_argument('--data_dir', type=str, required=True, help='The dictionary of inference data')

    parse.add_argument('--save_dir', type=str, required=True, help='Final result save path')

    args = parse.parse_args()
    return args

if __name__ == "__main__":
    model_name = args.model_name_or_path
    num_classes = 3
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_classes=num_classes)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    resule_save = []
    with open(args.data_dir, 'r', encoding='utf-8') as f:
        test_raw_data = json.load(f)
    test_data = [{'text': data['source']} for data in test_raw_data]
    label_map = {
        0: 'Positive', 
        1: 'Misspelled words', 
        2: 'Semantic Error'
    }
    
    results = predict(model, test_data, tokenizer, label_map, batch_size=32)
    for idx, text in enumerate(test_data):
        resule_save.append({'source': text['text'], 
                            'type': results[idx],
                            'id': test_raw_data[idx]['id']})
        print('Data: {} \t Lable: {}'.format(text, results[idx]))
    
    with open(args.save_dir, 'w', encoding='utf-8') as f:
        json.dump(resule_save, f)