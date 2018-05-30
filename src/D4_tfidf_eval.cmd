universe=vanilla
executable=run_summarization.sh
getenv=true
output=d4_tfidf.out
error=d4_tfidf.err
log=d4_tfidf.log
arguments="../conf/patas_eval_tfidf_config.yaml ../outputs/d4/tfidf/ /dropbox/17-18/573/Data/models/devtest/ ../results/d4_rouge_scores_tfidf.out experiment_two"
notification=complete
transfer_executable=false
queue
