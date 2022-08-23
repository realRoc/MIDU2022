pip install --upgrade paddlenlp

python train_classification.py --model_name_or_path nezha_el_ckpt --learning_rate 2e-5\
--train_data_path train_data/classify_train.json --train_data_is_ground_eval False\
--eval_data_path train_data/classify_val.json --eval_data_is_ground_eval False\
--max_seq_length 128 --batch_size 32\
--model_save_path ../models/nezha_el_ckpt --epoch 30 --print_step 100 --eval_step 100