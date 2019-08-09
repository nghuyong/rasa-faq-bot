bert-serving-start \
    -pooling_layer -4 -3 -2 -1 \
    -model_dir=./bert-models
    -num_worker=8 \
    -max_seq_len=16