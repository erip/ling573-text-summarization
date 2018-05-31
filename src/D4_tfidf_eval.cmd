universe=vanilla
executable=run_summarization.sh
getenv=true
output=D4_tfidf_eval.out
error=D4_tfidf_eval.err
log=D4_tfidf_eval.log
arguments="../conf/patas_eval_tfidf_config.yaml ../outputs/D4_evaltest/ /dropbox/17-18/573/Data/models/evaltest/ ../results/D4_evaltest_rouge_scores.out eval"
notification=complete
transfer_executable=false
queue
