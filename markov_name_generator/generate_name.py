""" Generate random names based using Markov chains """
import argparse
from pathlib import Path
from typing import List, Tuple
import numpy as np
import pandas as pd

START = '^'
END = '?'

def extract_strings(words: List[str], nb_char: int = 1):
    """
    Take a list of words and return the list of all strings of characters
    nb_char control the length of those strings (e.g. nb_char 2 = 2 characters in
    each substring)
    """
    pairs = []
    for word in words:
        prev = START * nb_char
        for char in word:
            pairs.append((prev, char))
            prev = prev[1:] + char if nb_char > 1 else char
        pairs.append((prev, END))

    return pairs

def build_stochastic_matrix(list_strings: List[Tuple[str, str]]) -> pd.DataFrame:
    """
    Calculate transitions probabilities and build the stochastic matrix
    from a list of characters strings
    """
    df_pairs = pd.DataFrame(list_strings, columns=['current', 'next'])
    stoch_matrix = pd.crosstab(df_pairs['current'], df_pairs['next'], normalize='index')
    return stoch_matrix


def create_markov_sequence(df_stoch_matrix: pd.DataFrame, nb_char: int = 1) -> str:
    """
    Create a random sequence based on a given stochastic matrix
    """
    name = ''
    letter = ''
    prev = START * nb_char
    while letter != END:
        s_next = df_stoch_matrix.loc[prev, :]
        letter = np.random.choice(s_next.index.to_numpy(), 1, p=s_next.to_numpy())[0]
        prev = prev[1:] + letter if nb_char > 1 else letter
        if letter != END:
            name += letter
    return name


class WordGenerator:
    """
    Word Generator class
    Takes some input data, parameters and generate words
    """
    nb_char: int
    stochastic_matrix: pd.DataFrame

    def __init__(self, list_words: List[str], nb_char: int = 1):
        self.nb_char = nb_char
        self.stochastic_matrix = build_stochastic_matrix(extract_strings(list_words, self.nb_char))

    def generate(self) -> str:
        new_word = create_markov_sequence(self.stochastic_matrix, self.nb_char)
        return new_word


def main():
    """ Parse parameters and generate names """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path_examples', type=str,
        help="A .txt file with examples - 1 word per line"
    )
    parser.add_argument(
        '--nb_names', type=int, default=10,
        help="Number of random ciy names to print"
        )
    parser.add_argument(
        '--nb_char', type=int, default=5,
        help="Length of the sequence of characters to use when building the chains"
        )
    args = parser.parse_args()

    path_examples = Path(args.path_examples)
    if path_examples.suffix != '.txt':
        print(f"ERROR - File provided was not a text file - {path_examples.absolute()}")
    else:
        with open(path_examples) as f_in:
            examples = f_in.read().splitlines()
            name_gen = WordGenerator(examples, nb_char=args.nb_char)
            for i in range(args.nb_names):
                print(name_gen.generate())


if __name__ == "__main__":
    main()
