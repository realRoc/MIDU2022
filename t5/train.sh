pip install --upgrade paddlenlp

python train.py --batch_size 32 --logging_steps 100 --epochs 5 --learning_rate 5e-5 --max_seq_length 128\
--model_name_or_path Langboat/mengzi-t5-base\
--output_dir ../models/t5_ft_ckpt/ \
--train_ds_dir /train_data/ \
--eval_ds_dir /val_data/