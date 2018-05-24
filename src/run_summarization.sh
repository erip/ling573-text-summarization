#!/usr/bin/env bash

# example run command:
#first sentences
#training
# ./run_summarization.sh ../conf/patas_config.yaml ../conf/UpdateSumm09_test_topics.xml ../outputs/D#/ /dropbox/17-18/573/Data/models/training/2009/ ../results/D3_rouge_scores.out some_experiment_name
#devtest
# ./run_summarization.sh ../conf/patas_devtest_config.yaml /dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml ../outputs/D#/ /dropbox/17-18/573/Data/models/devtest/ ../results/D3_rouge_scores.out some_experiment_name

#example run command with pretrained model
#TODO add this

config_file=$1
topic_cluster_file=$2
output_dir=$3
model_dir=$4
rouge_output_file=$5
experiment_number=$6
vec_model_path=${7:-""}
rouge_dir="/mnt/dropbox/17-18/573/code/ROUGE/"
rouge_config_file="../results/rouge_config_${experiment_number}.xml"

python3 summarize.py -c ${config_file} -t ${topic_cluster_file} -d ${output_dir} -m ${vec_model_path}

# generate ROUGE config file
python3 "${rouge_dir}/create_config.py" ${output_dir} ${model_dir} ${rouge_config_file}

# generate ROUGE results
python3 "${rouge_dir}/run_rouge.py" ${rouge_config_file} > ${rouge_output_file}



