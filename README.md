# Semantic Password Guesser

Tools for training probabilistic context-free grammars on password lists. The
models encode syntactic and semantic linguistic patterns and can be used to
generate guesses.

[Read the paper](http://vialab.dc-uoit.net/wordpress/wp-content/papercite-data/pdf/ver2014a.pdf)

Cite:

```
@inproceedings{Veras2014,
  title={On Semantic Patterns of Passwords and their Security Impact.},
  author={Veras, Rafael and Collins, Christopher and Thorpe, Julie},
  booktitle={NDSS},
  year={2014}
}
```


## Basic Usage

To train a grammar with a password list:

```
cd semantic_guesser  
python -m learning.train password_list.txt ~/grammars/test_grammar -vv
```

A password list has one password per line:

```
$ head password_list.txt
@fl!pm0de@
pass
steveol
chotzi
lb2512
scotch
passwerd
flipmode
flipmode
alden2
```

The resulting folder has a number of tab-separated, human readable files:

- `rules.txt` - grammar's base structures in highest probability order.
- `nonterminals/*.txt` - each file lists the terminal strings generated by a nonterminal symbol. For instance, `jj.txt` lists all strings classified as adjective along with their probabilities.

### Options

```
usage: train.py [-h] [--estimator {mle,laplace}] [-a ABSTRACTION] [-v]
                [--tags {pos_semantic,pos,backoff,word}] [-w NUM_WORKERS]
                [passwords] output_folder

positional arguments:
  passwords             a password list
  output_folder         a folder to store the grammar model

optional arguments:
  -h, --help            show this help message and exit
  --estimator {mle,laplace}
  -a ABSTRACTION, --abstraction ABSTRACTION
                        Detail level of the grammar. An integer > 0
                        proportional to the desired specificity.
  -v                    verbose level (e.g., -vvv)
  --tags {pos_semantic,pos,backoff,word}
  -w NUM_WORKERS, --num_workers NUM_WORKERS
                        number of cores available for parallel work

```

## Sampling from a grammar

Sample 1,000 passwords from `mygrammar`:

```
python -m guessing.sample 1000 mygrammar
```

## Generating guesses

The guess generator is a C++ program, you need to compile it first.

```
cd guessing
make
```

Then run it with a trained grammar model.

```
guessmaker -g /path/to/my/grammar --mangle
```

guessmaker implements the algorithms described in [Matt Weir's dissertation][1]: next and deadbeat. Deadbeat is the default.

The grammars have only lowercase strings. By passing `--mangle` in the above command we derive uppercase, lowercase, capitalized, and camelcase (when applicable) versions of every guess.

## Password probability

You can calculate the probability of a password given a grammar:

```
python -m guessing.score \
  --uppercase            \
  --camelcase            \
  --capitalized          \
  path_to_my_grammar     \
	a_list_of_passwords.txt
```

If you will be using `guessmaker --mangle` to generate guesses, unless you pass `--uppercase`, `--camelcase` and/or `--capitalized` to `guessing.score`, it will assume that non-lowercase passwords cannot be guessed by the grammar (_p=0_).

## Calculating password strength

We can calculate the strength of a password given a grammar using Filippone and Dell'Amico's [Monte Carlo strength evaluation](http://www.dcs.gla.ac.uk/~maurizio/Publications/ccs15.pdf). The strength is an estimate for how many passwords would need to be output (using the guess generation procedure above) before the password is guessed. We need a large sample (see how to generate samples above) from the grammar. The largest the sample the more accurate the estimates.

```
python -m guessing.sample 1000 path_to_grammar/ > sample.txt
python -m guessing.score path_to_grammar/ passwords.txt > scored_passwords.txt
python -m guessing.strength sample.txt scored_passwords.txt
```


## Environment Setup

venv is preferred:

```
cd semantic_guesser
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then download NLTK data:

```
python -m nltk.downloader wordnet wordnet_ic
```

[1]: http://purl.flvc.org/fsu/fd/FSU_migr_etd-1213 "Weir, C. M. (2010). Using Probabilistic Techniques to Aid in Password Cracking Attacks."
