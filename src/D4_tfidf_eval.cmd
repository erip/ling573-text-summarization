universe=vanilla
executable=run_summarization.sh
getenv=true
output=d4_tfidf.out
error=d4_tfidf.err
log=d4_tfidf.log
arguments="../conf/patas_evaltest_tfidf_config.yaml ../outputs/D4/tfidf/ /dropbox/17-18/573/Data/models/evaltest/ ../results/d4_rouge_scores_tfidf.out evaltest_one"
notification=complete
transfer_executable=false
queue
