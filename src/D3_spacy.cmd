universe=vanilla
executable=run_summarization.sh
getenv=true
output=d3_spacy.out
error=d3_spacy.err
log=d3_spacy.log
arguments="lexrank spacy ../conf/patas_devtest_config.yaml /dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml ../outputs/D3/spacy/ /dropbox/17-18/573/Data/models/devtest/ ../results/D3_rouge_scores_spacy.out"
notification=complete
transfer_executable=false
queue
