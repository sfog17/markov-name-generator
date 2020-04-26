import numpy as np
from markov_name_generator.generate_city_name import generate_city_names


def test_gen_city_name():
    np.random.seed(123)
    names = generate_city_names("GB", nb_names=4, nb_char=3)
    assert names == ["Penpointer", "Pickham", "Llanen", "Fall"]

