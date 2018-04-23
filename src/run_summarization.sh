#!/usr/bin/env bash

# example run command:
# ./run_summarization.sh first ../conf/patas_config.yaml ../conf/UpdateSumm09_test_topics.xml ../outputs/D2/ /dropbox/17-18/573/Data/models/training/2009/
sum_type=$1
config_file=$2
topic_cluster_file=$3
output_dir=$4
model_dir=$5
rouge_dir="/mnt/dropbox/17-18/573/code/ROUGE/"
rouge_config_file="rouge_config.xml"
rouge_output_file="D2_rouge_scores.out"

# generate output files
if [ ${sum_type} = "first" ]
then
    python3 baseline.py ${sum_type} -c ${config_file} -t ${topic_cluster_file} -n 100 -d ${output_dir}
elif [ ${sum_type} = "lexrank" ]
then
    python3 lexrank.py # Add lexrank stuff here
fi

# generate ROUGE config file
python3 ${rouge_dir}create_config.py ${output_dir} ${model_dir} ${rouge_config_file}

# generate ROUGE results
python3 ${rouge_dir}run_rouge.py ${rouge_config_file} > ${rouge_output_file}



