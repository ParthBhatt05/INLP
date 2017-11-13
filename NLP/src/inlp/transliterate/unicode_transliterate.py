import sys, codecs, string

from src.inlp import language_info
from src.inlp.transliterate import itrans_transliterator
from src.inlp.transliterate.sinhala_transliterator import SinhalaDevanagariTransliterator  as sdt


class UnicodeIndianLanguageTransliterator(object):
    """
    Base class for rule-based transliteration among Indian languages. 
    Script pair specific transliterators should derive from this class and override the transliterate() method. 
    They can call the super class 'transliterate()' method to avail of the common transliteration
    """

    @staticmethod
    def transliterate(text, lang1_code, lang2_code):
        """
        convert the source language script (lang1) to target language script (lang2)
        text: text to transliterate
        lang1_code: language 1 code 
        lang1_code: language 2 code 
        """
        if language_info.SCRIPT_RANGES.has_key(lang1_code) and language_info.SCRIPT_RANGES.has_key(lang2_code):
            # if Sinhala is source, do a mapping to Devanagari first 
            if lang1_code == 'si':
                text = sdt.sinhala_to_devanagari(text)
                lang1_code = 'hi'
            # if Sinhala is target, make Devanagiri the intermediate target
            org_lang2_code = ''
            if lang2_code == 'si':
                lang2_code = 'hi'
                org_lang2_code = 'si'
            trans_lit_text = []
            for c in text:
                newc = c
                offset = ord(c) - language_info.SCRIPT_RANGES[lang1_code][0]
                if offset >= language_info.COORDINATED_RANGE_START_INCLUSIVE and offset <= language_info.COORDINATED_RANGE_END_INCLUSIVE:
                    newc = unichr(language_info.SCRIPT_RANGES[lang2_code][0] + offset)
                trans_lit_text.append(newc)
                # if Sinhala is source, do a mapping to Devanagari first
            if org_lang2_code == 'si':
                return sdt.devanagari_to_sinhala(string.join(trans_lit_text, sep=''))
            return string.join(trans_lit_text, sep='')
        else:
            return text


class ItransTransliterator(object):
    """
    Transliterator between Indian scripts and ITRANS
    """

    @staticmethod
    def to_itrans(text, lang_code):
        if language_info.SCRIPT_RANGES.has_key(lang_code):
            devnag = UnicodeIndianLanguageTransliterator.transliterate(text, lang_code, 'hi')
            itrans = itrans_transliterator.transliterate(devnag.encode('utf-8'), 'devanagari', 'itrans',
                                                         {'outputASCIIEncoded': False,
                                                          'handleUnrecognised': itrans_transliterator.UNRECOGNISED_ECHO})
            return itrans.decode('utf-8')
        else:
            return text

    @staticmethod
    def from_itrans(text, lang_code):
        if language_info.SCRIPT_RANGES.has_key(lang_code):
            devnag_text = itrans_transliterator.transliterate(text.encode('utf-8'), 'itrans', 'devanagari',
                                                              {'outputASCIIEncoded': False,
                                                               'handleUnrecognised': itrans_transliterator.UNRECOGNISED_ECHO})
            lang_text = UnicodeIndianLanguageTransliterator.transliterate(devnag_text.decode('utf-8'), 'hi', lang_code)
            return lang_text
        else:
            return text


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python unicode_transliterate.py <command> <infile> <outfile> <src_language> <tgt_language>"
        sys.exit(1)
    if sys.argv[1] == 'transliterate':
        src_language = sys.argv[4]
        tgt_language = sys.argv[5]
        with codecs.open(sys.argv[2], 'r', 'utf-8') as ifile:
            with codecs.open(sys.argv[3], 'w', 'utf-8') as ofile:
                for line in ifile.readlines():
                    transliterated_line = UnicodeIndianLanguageTransliterator.transliterate(line, src_language, tgt_language)
                    ofile.write(transliterated_line)
    elif sys.argv[1] == 'romanize':
        language = sys.argv[4]
        with codecs.open(sys.argv[2], 'r', 'utf-8') as ifile:
            with codecs.open(sys.argv[3], 'w', 'utf-8') as ofile:
                for line in ifile.readlines():
                    transliterated_line = ItransTransliterator.to_itrans(line, language)
                    ofile.write(transliterated_line)
    elif sys.argv[1] == 'indianize':
        language = sys.argv[4]
        with codecs.open(sys.argv[2], 'r', 'utf-8') as ifile:
            with codecs.open(sys.argv[3], 'w', 'utf-8') as ofile:
                for line in ifile.readlines():
                    transliterated_line = ItransTransliterator.from_itrans(line, language)
                    ofile.write(transliterated_line)
