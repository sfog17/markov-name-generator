""" Generate random names based using Markov chains """
import argparse
from pathlib import Path
from typing import List, Tuple
import numpy as np
import pandas as pd

START = '^'
END = '?'

def extract_strings(words: List[str], window_size: int = 1):
    """
    Take a list of words and return the list of all strings of characters
    window_size control the length of those strings (e.g. window_size 2 = 2 characters in
    each substring)
    """
    pairs = []
    for word in words:
        prev = START * window_size
        for char in word:
            pairs.append((prev, char))
            prev = prev[1:] + char if window_size > 1 else char
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


def create_markov_sequence(df_stoch_matrix: pd.DataFrame, window_size: int = 1) -> str:
    """
    Create a random sequence based on a given stochastic matrix
    """
    name = ''
    letter = ''
    prev = START * window_size
    while letter != END:
        s_next = df_stoch_matrix.loc[prev, :]
        letter = np.random.choice(s_next.index.to_numpy(), 1, p=s_next.to_numpy())[0]
        prev = prev[1:] + letter if window_size > 1 else letter
        if letter != END:
            name += letter
    return name


class WordGenerator:
    """
    Word Generator class
    Takes some input data, parameters and generate words
    """
    window_size: int
    stochastic_matrix: pd.DataFrame

    def __init__(self, list_words: List[str], window_size: int = 1):
        self.window_size = window_size
        self.stochastic_matrix = build_stochastic_matrix(extract_strings(list_words, self.window_size))

    def generate(self) -> str:
        new_word = create_markov_sequence(self.stochastic_matrix, self.window_size)
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
        '--window_size', type=int, default=5,
        help="Length of the sequence of characters to use when building the chains"
        )
    args = parser.parse_args()

    path_examples = Path(args.path_examples)
    if path_examples.suffix != '.txt':
        print(f"ERROR - File provided was not a text file - {path_examples.absolute()}")
    else:
        with open(path_examples) as f_in:
            examples = f_in.read().splitlines()
            name_gen = WordGenerator(examples, window_size=args.window_size)
            for i in range(args.nb_names):
                print(name_gen.generate())


if __name__ == "__main__":
    main()
