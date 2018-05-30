universe=vanilla
executable=run_summarization.sh
getenv=true
output=d4_tfidf_eval.out
error=d4_tfidf_eval.err
log=d4_tfidf_eval.log
arguments="../conf/patas_eval_tfidf_config.yaml ../outputs/d4/tfidf/ /dropbox/17-18/573/Data/models/evaltest/ ../results/d4_rouge_scores_tfidf.out eval"
notification=complete
transfer_executable=false
queue
