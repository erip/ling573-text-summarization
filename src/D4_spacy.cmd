universe=vanilla
executable=run_summarization.sh
getenv=true
output=d4_spacy.out
error=d4_spacy.err
log=d4_spacy.log
arguments="../conf/patas_devtest_config.yaml ../outputs/d4/spacy/ /dropbox/17-18/573/Data/models/devtest/ ../results/d4_rouge_scores_spacy.out experiment_one"
notification=complete
transfer_executable=false
queue
