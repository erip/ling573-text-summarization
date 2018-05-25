# Text Summarization

### Documentation

Documentation can be found in the [docs/](./docs/) directory.

### Installing dependencies

Ensure you're working on a [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/).

Once working on a virtualenv, you can simply `pip3 install -r requirements.txt`.

### Run the System
To run the system on Training data: 

```bash
$./run_summarization.sh ../conf/patas_config.yaml <output_dir> /dropbox/17-18/573/Data/models/training/2009/ <rouge_outfile> <experiment_name>
```

To run the system on DevTest data: 

```bash
$./run_summarization.sh ../conf/patas_devtest_config.yaml <output_dir> /dropbox/17-18/573/Data/models/devtest/ <rouge_outfile> <experiment_name>
```

The currently supported summarization methods are:

1. **first**, use the first sentence as the summary.
1. **random**, use a random sentence as the summary.
1. **lexrank**, use lexrank to determine the summary.

Different methods of sentence representation for lexrank are also now supported, and are:

1. **tfidf**, use tfidf metrics for sentence salience.
1. **spacy**, use spacy sentence vectors for sentence salience. Spacy sentence vectors are the averaged GloVe embeddings 
of words


If `en_vectors_web_lg` hasn't been downloaded from spacy before, it may be necessary to first download it. It is ~600MB.

In the environment you intend to use:
```bash 
python -m spacy download en_vectors_web_lg
```

Because our code uses bleeding-edge features of Python (like the `typing` module for linting), you'll need to ensure that
Python 3.6 is the python version when running the code. On patas, this can be done by adding  
`export PATH="/opt/python-3.6/bin/:$PATH"` to your `~/.bashrc` (be sure to `. ~/.bashrc` your first time).

To run `run_summarization.sh` on condor: 

```bash
condor_submit D4_tfidf.cmd
```

This runs the best performing of the permutations of the system. All the varied permutations are configurable via 
`run_summarization.sh`.

### Testing

Once all dependencies are installed, running `nosetests` from the `src/` directory should run all unit tests.

### Results

Results can be found in the [results/](./results/) directory.

### Outputs

Outputs can be found in the [outputs/](./outputs/) directory. tfidf results will be top-level, other permutations 
will be in sub-folders with the vec_type name.

### Team

- [Ayushi Aggarwal](mailto:ayushiag@uw.edu)
- [Elijah Rippeth](mailto:rippeth@uw.edu)
- [Seraphina Goldfarb-Tarrant](mailto:serif@uw.edu)
