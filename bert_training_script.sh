#!/usr/bin/env bash
python run_pretraining.py \
    --input_file gs://bert-ontology/corpuses/*.txt \
    --bert_config_file=gs://bert_models/2018_10_18/uncased_L-12_H-768_A-12/bert_config.json \
    --output_dir=gs://bert-ontology/models \
    --use_tpu=True \
    --init_checkpoint gs://bert_models/2018_10_18/uncased_L-12_H-768_A-12/bert_model.ckpt \
    --tpu_name node-1 \
    --do_train=True \
    --gcp_project iris-unmind \
    --num_tpu_cores 2 \

