import codecs, sys, string, re
import morfessor
from src.inlp import language_info
from src.inlp import common
from tokenize import tokenize


class MorphAnalyzerI(object):

    def morph_analyze(word):
        pass

    def morph_analyze_document(tokens):
        pass


class UnsupervisedMorphAnalyzer(MorphAnalyzerI):

    def __init__(self, lang, add_marker=False):
        self.lang = lang
        self.add_marker = add_marker
        io = morfessor.MorfessorIO()
        self._morfessor_model = io.read_any_model(
            common.INLP_RESOURCES_PATH + '/morph/morfessor/{}.model'.format(lang))
        self._script_range_pat = ur'^[{}-{}]+$'.format(unichr(language_info.SCRIPT_RANGES[lang][0]),
                                                       unichr(language_info.SCRIPT_RANGES[lang][1]))
        self._script_check_re = re.compile(self._script_range_pat)

    def _contains_number(self, text):
        if self.lang in language_info.SCRIPT_RANGES:
            for c in text:
                offset = ord(c) - language_info.SCRIPT_RANGES[self.lang][0]
                if offset >= language_info.NUMERIC_OFFSET_START and offset <= language_info.NUMERIC_OFFSET_END:
                    return True
        return False

    def _morphanalysis_needed(self, word):
        return self._script_check_re.match(word) and not self._contains_number(word)

    def morph_analyze(self, word):
        """
        analyzes a single word and returns a list of component morphemes
		@param word: string input word 
        """
        m_list = []
        if self._morphanalysis_needed(word):
            val = self._morfessor_model.viterbi_segment(word)
            m_list = val[0]
            if self.add_marker:
                m_list = [u'{}_S_'.format(m) if i > 0 else u'{}_R_'.format(m) for i, m in enumerate(m_list)]
        else:
            if self.add_marker:
                word = u'{}_E_'.format(word)
            m_list = [word]
        return m_list

        ### Older implementation
        # val=self._morfessor_model.viterbi_segment(word)
        # m_list=val[0]
        # if self.add_marker:
        #    m_list= [ u'{}_S_'.format(m) if i>0 else u'{}_R_'.format(m)  for i,m in enumerate(m_list)]
        # return m_list

    def morph_analyze_document(self, tokens):
        """
        analyzes a document, represented as a list of tokens
        Each word  is analyzed and result is a list of morphemes constituting the document

        @param tokens: string sequence of words 

        @return list of segments in the document after morph analysis 
        """
        out_tokens = []
        for token in tokens:
            morphs = self.morph_analyze(token)
            out_tokens.extend(morphs)
        return out_tokens

        #### Older implementation
        # out_tokens=[]
        # for token in tokens:
        #    if self._morphanalysis_needed(token): 
        #        morphs=self.morph_analyze(token)
        #        out_tokens.extend(morphs)
        #    else:
        #        if self.add_marker:
        #            token=u'{}_E_'.format(token)
        #        out_tokens.append(token)
        # return out_tokens


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python morph.py <infile> <outfile> <language> <INLP_resources_path> [<add_marker>]"
        sys.exit(1)
    language = sys.argv[3]
    common.INLP_RESOURCES_PATH = sys.argv[4]
    add_marker = False
    if len(sys.argv) == 6:
        add_marker = True if sys.argv[5] == 'True' else False
    print 'Loading morph analyser for ' + language
    analyzer = UnsupervisedMorphAnalyzer(language, add_marker)
    print 'Loaded morph analyser for ' + language
    with codecs.open(sys.argv[1], 'r', 'utf-8') as ifile:
        with codecs.open(sys.argv[2], 'w', 'utf-8') as ofile:
            for line in ifile.readlines():
                line = line.strip()
                tokens = tokenize.trivial_tokenize(line)
                morph_tokens = analyzer.morph_analyze_document(tokens)
                ofile.write(string.join(morph_tokens, sep=' '))
                ofile.write('\n')
