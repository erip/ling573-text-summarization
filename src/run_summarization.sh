#!/usr/bin/env bash

# example run command:
#first sentences
#training
# ./run_summarization.sh first ../conf/patas_config.yaml ../conf/UpdateSumm09_test_topics.xml ../outputs/D#/ /dropbox/17-18/573/Data/models/training/2009/
#devtest
# ./run_summarization.sh first ../conf/patas_devtest_config.yaml /dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml ../outputs/D#/ /dropbox/17-18/573/Data/models/devtest/

#example run command with pretrained model
#TODO add this

sum_type=$1
vec_type=$2
config_file=$3
topic_cluster_file=$4
output_dir=$5
model_path=${6:-""}
rouge_dir="/mnt/dropbox/17-18/573/code/ROUGE/"
rouge_config_file="../results/rouge_config.xml"
rouge_output_file="../results/D3_rouge_scores.out"

# generate output files
if [ ${sum_type} = "first" ]
then
    python3 baseline.py ${sum_type} -c ${config_file} -t ${topic_cluster_file} -n 100 -d ${output_dir}
elif [ ${sum_type} = "lexrank" ]
then
    if [ ${vec_type} = "doc2vec" ] || [ ${vec_type} = "word2vec" ]
    then
        python3 lexrank_driver.py -c ${config_file} -t ${topic_cluster_file} -n 100 -v ${vec_type} -th 0.1 -e 0.1 -d ${output_dir} -m ${model_path}
    else
        python3 lexrank_driver.py -c ${config_file} -t ${topic_cluster_file} -n 100 -v ${vec_type} -th 0.1 -e 0.1 -d ${output_dir}
    fi
fi

# generate ROUGE config file
python3 "${rouge_dir}/create_config.py" ${output_dir} ${model_dir} ${rouge_config_file}

# generate ROUGE results
python3 "${rouge_dir}/run_rouge.py" ${rouge_config_file} > ${rouge_output_file}



