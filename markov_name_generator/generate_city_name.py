""" Generate random city names using Markov chains """
import argparse
from pathlib import Path
from typing import List
import pandas as pd
from markov_name_generator.generate_name import WordGenerator

PATH_DATA = Path(__file__).parent.parent / 'data'
PATH_CITY_NAMES = PATH_DATA / 'geonames_cities.csv'


def generate_city_names(country: str, nb_names: int, nb_char: int) -> List[str]:
    """ Generate city names """
    df = pd.read_csv(PATH_CITY_NAMES)
    city_gen = WordGenerator(df[df['Country Code'] == country]['Name'].tolist(), nb_char=nb_char)
    city_names = [city_gen.generate() for name in range(nb_names)]
    return city_names


def main():
    """ Parse parameters and generate names """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'iso_country_code', type=str,
        help="Country ISO code to generate city name from"
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
    if len(args.iso_country_code) != 2:
        print(f"ERROR - {args.iso_country_code} does not have 2 letters and is not a valid ISO country code")

    cities = generate_city_names(args.iso_country_code, args.nb_names, args.nb_char)
    for city in cities:
        print(city)


if __name__ == "__main__":
    main()
