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


The lexrank method relies on detokenizing input, for which we use the Moses detokenizer.

If `nltk_data` have not been downloaded before, it may be necessary to first download them:

```python3
>>> import nltk
>>> nltk.download('perluniprops')
```

To run `run_summarization.sh` on condor: 

```bash
condor_submit D2.cmd
```

### Testing

Once all dependencies are installed, running `nosetests` from the project root shoudl run all unit tests.

### Results

Results can be found in the [results/](./results/) directory.

### Team

- [Ayushi Aggarwal](mailto:ayushiag@uw.edu)
- [Elijah Rippeth](mailto:rippeth@uw.edu)
- [Seraphina Goldfarb-Tarrant](mailto:serif@uw.edu)
