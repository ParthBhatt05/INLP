import pandas as pd
import numpy as np

from src.inlp import common
from src.inlp.common import inlpException
from src.inlp import language_info as li

ALL_PHONETIC_DATA = None
ALL_PHONETIC_VECTORS = None
PHONETIC_VECTOR_LENGTH = 38
PHONETIC_VECTOR_START_OFFSET = 6

# PHONETIC PROPERTIES in order in which they occur in the vector 
# This list must be in sync with the keys in the PV_PROP_RANGES dictionary 
PV_PROP = ['basic_type',
           'vowel_length',
           'vowel_strength',
           'vowel_status',
           'consonant_type',
           'articulation_place',
           'aspiration',
           'voicing',
           'nasalization',
           'vowel_horizontal',
           'vowel_vertical',
           'vowel_roundness',
           ]

# Bit vector ranges for various properties 
PV_PROP_RANGES = {
    'basic_type': [0, 6],
    'vowel_length': [6, 8],
    'vowel_strength': [8, 11],
    'vowel_status': [11, 13],
    'consonant_type': [13, 18],
    'articulation_place': [18, 23],
    'aspiration': [23, 25],
    'voicing': [25, 27],
    'nasalization': [27, 29],
    'vowel_horizontal': [29, 32],
    'vowel_vertical': [32, 36],
    'vowel_roundness': [36, 38],
}

# Indexes into the Phonetic Vector 
PVIDX_BT_VOWEL = 0
PVIDX_BT_CONSONANT = 1
PVIDX_BT_NUKTA = 2
PVIDX_BT_HALANT = 3
PVIDX_BT_ANUSVAAR = 4
PVIDX_BT_MISC = 5
PVIDX_BT_S = PVIDX_BT_VOWEL
PVIDX_BT_E = PVIDX_BT_MISC + 1
PVIDX_VSTAT_DEP = 12

# Unicode information about characters 
SCRIPT_OFFSET_START = 0
SCRIPT_OFFSET_RANGE = 0x80


def init():
    global ALL_PHONETIC_DATA, ALL_PHONETIC_VECTORS, PHONETIC_VECTOR_LENGTH, PHONETIC_VECTOR_START_OFFSET
    ALL_PHONETIC_DATA = pd.read_csv(common.get_resources_path() + '/script/all_script_phonetic_data.csv',
                                    encoding='utf-8')
    ALL_PHONETIC_VECTORS = ALL_PHONETIC_DATA.ix[:, PHONETIC_VECTOR_START_OFFSET:].as_matrix()
    PHONETIC_VECTOR_LENGTH = ALL_PHONETIC_VECTORS.shape[1]


def is_supported_language(lang):
    return lang in li.SCRIPT_RANGES.keys()


def get_offset(c, lang):
    if not is_supported_language(lang):
        raise inlpException('Language {}  not supported'.format(lang))
    return ord(c) - li.SCRIPT_RANGES[lang][0]


def offset_to_char(off, lang):
    """
    Applicable to Brahmi derived Indian scripts 
    """
    if not is_supported_language(lang):
        raise inlpException('Language {}  not supported'.format(lang))
    return unichr(off + li.SCRIPT_RANGES[lang][0])


def is_indianlanguage_char(c, lang):
    """
    Applicable to Brahmi derived Indian scripts 
    Note that DANDA and DOUBLE_DANDA have the same Unicode codepoint for all Indian scripts 
    """
    if not is_supported_language(lang):
        raise inlpException('Language {}  not supported'.format(lang))
    o = get_offset(c, lang)
    return (o >= SCRIPT_OFFSET_START and o < SCRIPT_OFFSET_RANGE) \
           or ord(c) == li.DANDA or ord(c) == li.DOUBLE_DANDA


def in_coordinated_range_offset(c_offset):
    """ 
    Applicable to Brahmi derived Indian scripts 
    """
    return (c_offset >= li.COORDINATED_RANGE_START_INCLUSIVE and c_offset <= li.COORDINATED_RANGE_END_INCLUSIVE)


def in_coordinated_range(c, lang):
    if not is_supported_language(lang):
        raise inlpException('Language {}  not supported'.format(lang))
    return in_coordinated_range_offset(get_offset(c, lang))


def get_phonetic_info(lang):
    if not is_supported_language(lang):
        raise inlpException('Language {}  not supported'.format(lang))
    phonetic_data = ALL_PHONETIC_DATA
    phonetic_vectors = ALL_PHONETIC_VECTORS
    return (phonetic_data, phonetic_vectors)


def invalid_vector():
    ##  TODO: check if np datatype is correct?
    return np.array([0] * PHONETIC_VECTOR_LENGTH)


def get_phonetic_feature_vector(c, lang):
    offset = get_offset(c, lang)
    if not in_coordinated_range_offset(offset):
        return invalid_vector()
    phonetic_data, phonetic_vectors = get_phonetic_info(lang)
    if phonetic_data.ix[offset, 'Valid Vector Representation'] == 0:
        return invalid_vector()
    return phonetic_vectors[offset]


### Unary operations on vectors
def is_valid(v):
    return np.sum(v) > 0


def is_vowel(v):
    return v[PVIDX_BT_VOWEL] == 1


def is_consonant(v):
    return v[PVIDX_BT_CONSONANT] == 1


def is_halant(v):
    return v[PVIDX_BT_HALANT] == 1


def is_nukta(v):
    return v[PVIDX_BT_NUKTA] == 1


def is_anusvaar(v):
    return v[PVIDX_BT_ANUSVAAR] == 1


def is_misc(v):
    return v[PVIDX_BT_MISC] == 1


def is_dependent_vowel(v):
    return is_vowel(v) and v[PVIDX_VSTAT_DEP] == 1


def is_plosive(v):
    return is_consonant(v) and get_property_vector(v, 'consonant_type')[0] == 1


# Binary operations on phonetic vectors
def or_vectors(v1, v2):
    return np.array([1 if (b1 + b2) >= 1 else 0 for b1, b2 in zip(v1, v2)])


def xor_vectors(v1, v2):
    return np.array([1 if b1 != b2 else 0 for b1, b2 in zip(v1, v2)])


# Getting properties from phonetic vectors
def get_property_vector(v, prop_name):
    return v[PV_PROP_RANGES[prop_name][0]:PV_PROP_RANGES[prop_name][1]]


def get_property_value(v, prop_name):
    factor_bits = get_property_vector(v, prop_name).tolist()
    v = 0
    c = 1
    for b in factor_bits[::-1]:
        v += (c * b)
        c = c * 2.0
    return int(v)


if __name__ == "__main__":
    init()
