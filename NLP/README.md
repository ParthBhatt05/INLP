# Indic NLP Library

The goal of the Indic NLP Library is to build Python based libraries for common text processing and Natural Language Processing in Indian languages. Indian languages share a lot of similarity in terms of script, phonology, language syntax, etc. and this library is an attempt to provide a general solution to very commonly required toolsets for Indian language text.

The library provides the following functionalities:

- Text Normalization
- Script Information
- Tokenization
- Word Segmentation
- Script Conversion
- Romanization
- Indicization
- Transliteration
- Translation

The data resources required by the Indic NLP Library are hosted in a different repository. These resources are required for some modules.

# Pre-requisites
- Python 2.7+
- [Morfessor 2.0 Python Library](http://www.cis.hut.fi/projects/morpho/morfessor2.shtml)
- [Indic NLP Resources]

# Configuration
- Add the project to the Python Path: 

    export PYTHONPATH=$PYTHONPATH:\<project base directory\>/src

- Export the path to the _Indic NLP Resources_ directory

    export INDIC_RESOURCES_PATH=\<path to Indic NLP resources\> 

# Usage 

- Python API: Check IPython Notebook
- Commandline Interface: The commandline interface is documented 