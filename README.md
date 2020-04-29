# Markov name generator

This project is a small experiment to play with Markov chains and generate random names.
This can either be used to generate city names, or any name if you provide a list of examples
to learn from.

This is also a pratice to learn how to use Poetry to structur projects

## Requirements

- If you don't have it, install poetry (<https://python-poetry.org/docs/>)
- Clone repository
- Install dependencies by opening a command line in the directory and running

```cmd
poetry install
```

## Usage

Run the module using poetry

```cmd
poetry shell
```

You can then use it to:

### Generate city names

Usage:

```cmd
usage: gen-city-name [-h] [--nb_names NB_NAMES] [--window_size WINDOW_SIZE] iso_country_code

positional arguments:
  iso_country_code     Country ISO code to generate city name from

optional arguments:
  -h, --help           show this help message and exit
  --nb_names NB_NAMES  Number of random ciy names to print
  --window_size WINDOW_SIZE    Length of the sequence of characters to use when building the chains
```

Example:

```cmd
gen-city-name FR --nb_names 30 --window_size 8
```



### Generate names based on examples

Usage:

```cmd
usage: gen-name [-h] [--nb_names NB_NAMES] [--window_size WINDOW_SIZE] path_examples

positional arguments:
  path_examples        A .txt file with examples - 1 word per line

optional arguments:
  -h, --help           show this help message and exit
  --nb_names NB_NAMES  Number of random ciy names to print
  --window_size WINDOW_SIZE    Length of the sequence of characters to use when building the chains
```

Example:

```cmd
gen-name data/list_first_names.txt --window_size 2 --nb_names 30
```
