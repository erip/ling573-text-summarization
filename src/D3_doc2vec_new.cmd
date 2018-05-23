universe=vanilla
executable=run_summarization.sh
getenv=true
output=d3.out
error=d3.err
log=d3.log
arguments="lexrank doc2vec ../conf/patas_devtest_config.yaml /dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml ../outputs/D3/doc2vec/ /dropbox/17-18/573/Data/models/devtest/ ../results/D3_rouge_scores_doc2vec.out /dropbox/17-18/573/other_resources/word_embeddings/eng_gw/doc2vec/doc2vec_100M_cased.vecs"
notification=complete
transfer_executable=false
queue
