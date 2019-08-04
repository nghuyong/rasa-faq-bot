bert-serving-start \
    -pooling_layer -4 -3 -2 -1 \
    -model_dir=CHANGE_ME_TO_YOUR_BERT_CHINESE_MODEL_DIR
    -num_worker=8 \
    -max_seq_len=16