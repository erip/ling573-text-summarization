universe=vanilla
executable=run_summarization.sh
getenv=true
output=D4_tfidf.out
error=D4_tfidf.err
log=D4_tfidf.log
arguments="../conf/patas_devtest_tfidf_config.yaml ../outputs/D4_devtest/ /dropbox/17-18/573/Data/models/devtest/ ../results/D4_devtest_rouge_scores.out devtest"
notification=complete
transfer_executable=false
queue
