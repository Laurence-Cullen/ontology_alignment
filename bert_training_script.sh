#!/usr/bin/env bash
python run_pretraining.py \
    --input_file gs://medical-bert-fine-tuning/corpuses/*.txt \
    --bert_config_file=gs://bert_models/2018_10_18/uncased_L-12_H-768_A-12/bert_config.json \
    --output_dir=gs://medical-bert-fine-tuning/models \
    --do_train=True
