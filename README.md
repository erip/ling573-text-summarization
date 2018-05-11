# Text Summarization

### Documentation

Documentation can be found in the [docs/](./docs/) directory.

### Installing dependencies

Ensure you're working on a [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/).

Once working on a virtualenv, you can simply `pip3 install -r requirements.txt`.

### Run the System
To run the system on Training data: 

```bash
$./run_summarization.sh <method> ../conf/patas_config.yaml ../conf/UpdateSumm09_test_topics.xml ../outputs/D2/ /dropbox/17-18/573/Data/models/training/2009/
```

To run the system on DevTest data: 

```bash
$./run_summarization.sh <method> ../conf/patas_devtest_config.yaml /dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml ../outputs/D2/ /dropbox/17-18/573/Data/models/devtest/
```

The currently supported summarization methods are:

1. **first**, use the first sentence as the summary.
1. **random**, use a random sentence as the summary.
1. **lexrank**, use lexrank to determine the summary.


Different methods of sentence representation for lexrank are also now supported, and are:
1. **tfidf**, use tfidf metrics for sentence salience.
1. **spacy**, use spacy sentence vectors for sentence salience. Soacy sentence vectors are the averaged GloVe embeddings 
of words
1. **doc2vec**, use doc2vec vectors for sentence salience. This trains word vectors on the Gigaword corpus in the 
context of the paragraph that the words appear in.
1. TBA **word2vec**, use word2vec metrics, trained on Google News, for sentence salience.



If `en_vectors_web_lg` hasn't been downloaded from spacy before, it may be necessary to first download it. It is ~600MB.
In the environment you intend to use:
```python -m spacy download en_vectors_web_lg
```

To run `run_summarization.sh` on condor: 

```bash
condor_submit D2.cmd
```

### Results

Results can be found in the [results/](./results/) directory.

### Team

- [Ayushi Aggarwal](mailto:ayushiag@uw.edu)
- [Elijah Rippeth](mailto:rippeth@uw.edu)
- [Seraphina Goldfarb-Tarrant](mailto:serif@uw.edu)
