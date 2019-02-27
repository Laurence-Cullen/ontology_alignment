#!/usr/bin/env bash
python run_pretraining.py \
    --input_file gs://bert-ontology/corpuses/*.txt \
    --bert_config_file gs://bert-ontology/uncased_L-24_H-1024_A-16/bert_config.json \
    --output_dir=gs://bert-ontology/models \
    --use_tpu=True \
    --init_checkpoint gs://bert-ontology/uncased_L-24_H-1024_A-16/bert_model.ckpt \
    --tpu_name node-1 \
    --do_train=True \
    --gcp_project iris-unmind \
    --num_tpu_cores 8 \
    --tpu_zone us-central1-c


