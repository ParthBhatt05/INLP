import sys, codecs, re


class NormalizerI(object):
    """
    The normalizer classes do the following: 
        Some characters have multiple Unicode code-points. The normalizer chooses a single standard representation
        Some control characters are deleted
        While typing using the Latin keyboard, certain typical mistakes occur which are corrected by the module
    Base class for normalizer. Performs some common normalization, which includes: 
        Byte order mark, word joiner, etc. removal
        ZERO_WIDTH_NON_JOINER and ZERO_WIDTH_JOINER removal
        ZERO_WIDTH_SPACE and NO_BREAK_SPACE replaced by spaces
    Script specific normalizers should derive from this class and override the normalize() method. 
    They can call the super class 'normalize() method to avail of the common normalization 
    """
    BYTE_ORDER_MARK = u'\uFEFF'
    BYTE_ORDER_MARK_2 = u'\uFFFE'
    WORD_JOINER = u'\u2060'
    SOFT_HYPHEN = u'\u00AD'
    ZERO_WIDTH_SPACE = u'\u200B'
    NO_BREAK_SPACE = u'\u00A0'
    ZERO_WIDTH_NON_JOINER = u'\u200C'
    ZERO_WIDTH_JOINER = u'\u200D'

    def normalize(self, text):
        text = text.replace(NormalizerI.BYTE_ORDER_MARK, '')
        text = text.replace(NormalizerI.BYTE_ORDER_MARK_2, '')
        text = text.replace(NormalizerI.WORD_JOINER, '')
        text = text.replace(NormalizerI.SOFT_HYPHEN, '')
        text = text.replace(NormalizerI.ZERO_WIDTH_SPACE, ' ')  # ??
        text = text.replace(NormalizerI.NO_BREAK_SPACE, ' ')
        text = text.replace(NormalizerI.ZERO_WIDTH_NON_JOINER, '')
        text = text.replace(NormalizerI.ZERO_WIDTH_JOINER, '')
        return text

    def get_char_stats(self, text):
        print(len(re.findall(NormalizerI.BYTE_ORDER_MARK, text)))
        print(len(re.findall(NormalizerI.BYTE_ORDER_MARK_2, text)))
        print(len(re.findall(NormalizerI.WORD_JOINER, text)))
        print(len(re.findall(NormalizerI.SOFT_HYPHEN, text)))
        print(len(re.findall(NormalizerI.ZERO_WIDTH_SPACE, text)))
        print(len(re.findall(NormalizerI.NO_BREAK_SPACE, text)))
        print(len(re.findall(NormalizerI.ZERO_WIDTH_NON_JOINER, text)))
        print(len(re.findall(NormalizerI.ZERO_WIDTH_JOINER, text)))
        # for mobj in re.finditer(NormalizerI.ZERO_WIDTH_NON_JOINER,text):
        #    print text[mobj.start()-10:mobj.end()+10].replace('\n', ' ').replace(NormalizerI.ZERO_WIDTH_NON_JOINER,'').encode('utf-8')
        # print hex(ord(text[mobj.end():mobj.end()+1]))

    def correct_visarga(self, text, visarga_char, char_range):
        text = re.sub(ur'([\u0900-\u097f]):', u'\\1\u0903', text)


class DevanagariNormalizer(NormalizerI):
    """
    Normalizer for the Devanagari script. In addition to basic normalization by the super class, 
        Replaces the composite characters containing nuktas by their decomposed form
        replace pipe character '|' by poorna virama character
        replace colon ':' by visarga if the colon follows a charcter in this script
    """

    NUKTA = u'\u093C'

    def __init__(self, remove_nuktas=False):
        self.remove_nuktas = remove_nuktas

    def normalize(self, text):
        # common normalization for INLP scripts
        text = super(DevanagariNormalizer, self).normalize(text)
        # decomposing Nukta based composite characters
        text = text.replace(u'\u0929', u'\u0928' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u0931', u'\u0930' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u0934', u'\u0933' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u0958', u'\u0915' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u0959', u'\u0916' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u095A', u'\u0917' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u095B', u'\u091C' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u095C', u'\u0921' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u095D', u'\u0922' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u095E', u'\u092B' + DevanagariNormalizer.NUKTA)
        text = text.replace(u'\u095F', u'\u092F' + DevanagariNormalizer.NUKTA)
        if self.remove_nuktas:
            text = text.replace(DevanagariNormalizer.NUKTA, '')
        # replace pipe character for poorna virama 
        text = text.replace(u'\u007c', u'\u0964')
        # correct visarge 
        text = re.sub(ur'([\u0900-\u097f]):', u'\\1\u0903', text)
        return text

    def get_char_stats(self, text):
        super(DevanagariNormalizer, self).get_char_stats(text)
        print(len(re.findall(u'\u0929', text)))
        print(len(re.findall(u'\u0931', text)))
        print(len(re.findall(u'\u0934', text)))
        print(len(re.findall(u'\u0958', text)))
        print(len(re.findall(u'\u0959', text)))
        print(len(re.findall(u'\u095A', text)))
        print(len(re.findall(u'\u095B', text)))
        print(len(re.findall(u'\u095C', text)))
        print(len(re.findall(u'\u095D', text)))
        print(len(re.findall(u'\u095E', text)))
        print(len(re.findall(u'\u095F', text)))
        # print(len(re.findall(u'\u0928'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u0930'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u0933'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u0915'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u0916'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u0917'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u091C'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u0921'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u0922'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u092B'+DevanagariNormalizer.NUKTA,text)))
        # print(len(re.findall(u'\u092F'+DevanagariNormalizer.NUKTA,text)))
        # print(u'\u0929')
        # print(u'\u0931')
        # print(u'\u0934')
        # print(u'\u0958')
        # print(u'\u0959')
        # print(u'\u095A')
        # print(u'\u095B')
        # print(u'\u095C')
        # print(u'\u095D')
        # print(u'\u095E')
        # print(u'\u095F')


class GujaratiNormalizer(NormalizerI):
    """
    Normalizer for the Gujarati script. In addition to basic normalization by the super class, 
        Replace the reserved character for poorna virama (if used) with the recommended generic INLP scripts poorna virama
        replace colon ':' by visarga if the colon follows a charcter in this script
    """

    NUKTA = u'\u0ABC'

    def __init__(self, remove_nuktas=False):
        self.remove_nuktas = remove_nuktas

    def normalize(self, text):
        # common normalization for INLP scripts
        text = super(GujaratiNormalizer, self).normalize(text)
        # decomposing Nukta based composite characters
        if self.remove_nuktas:
            text = text.replace(GujaratiNormalizer.NUKTA, '')
        # replace the poorna virama codes specific to script 
        # with generic INLP script codes
        text = text.replace(u'\u0ae4', u'\u0964')
        text = text.replace(u'\u0ae5', u'\u0965')
        # correct visarge 
        text = re.sub(ur'([\u0a80-\u0aff]):', u'\\1\u0a83', text)
        return text


class IndianLanguageNormalizerFactory(object):
    """
    Factory class to create language specific normalizers. 
    """

    def get_normalizer(self, language, remove_nuktas=False):
        """
            Call the get_normalizer function to get the language specific normalizer
            @params
            |language: language code
            |remove_nuktas: boolean, should the normalizer remove nukta characters 
        """
        normalizer = None
        if language in ['hi']:
            normalizer = DevanagariNormalizer(remove_nuktas)
        elif language in ['gu']:
            normalizer = GujaratiNormalizer(remove_nuktas)
        else:
            normalizer = NormalizerI()
        return normalizer

    def is_language_supported(self, language):
        if language in ['hi', 'gu']:
            return True
        else:
            return False


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python normalize.py <infile> <outfile> <language> [<replace_nukta(True,False>]"
        sys.exit(1)
    language = sys.argv[3]
    remove_nuktas = False
    if len(sys.argv) >= 5:
        remove_nuktas = bool(sys.argv[4])
    # create normalizer
    factory = IndianLanguageNormalizerFactory()
    normalizer = factory.get_normalizer(language, remove_nuktas)
    # DO normalization 
    with codecs.open(sys.argv[1], 'r', 'utf-8') as ifile:
        with codecs.open(sys.argv[2], 'w', 'utf-8') as ofile:
            for line in ifile.readlines():
                normalized_line = normalizer.normalize(line)
                ofile.write(normalized_line)
                # gather status about normalization
                # with codecs.open(sys.argv[1],'r','utf-8') as ifile:
                #    normalizer=DevanagariNormalizer()
                #    text=string.join(ifile.readlines(),sep='')
                #    normalizer.get_char_stats(text)
