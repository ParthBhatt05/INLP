import string, re, sys, codecs

triv_tokenizer_indic_pat = re.compile(ur'([' + string.punctuation + ur'\u0964\u0965' + ur'])')
triv_tokenizer_urdu_pat = re.compile(ur'([' + string.punctuation + ur'\u0609\u060A\u060C\u061E\u066A\u066B\u066C\u066D\u06D4' + ur'])')


def trivial_tokenize(s, lang='hi'):
    tok_str = triv_tokenizer_indic_pat.sub(r' \1 ', s.replace('\t', ' '))
    return re.sub(r'[ ]+', u' ', tok_str).strip(' ').split(' ')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python tokenize.py <infile> <outfile> <language>"
        sys.exit(1)
    with codecs.open(sys.argv[1], 'r', 'utf-8') as ifile:
        with codecs.open(sys.argv[2], 'w', 'utf-8') as ofile:
            for line in ifile.readlines():
                tokenized_line = string.join(trivial_tokenize(line, sys.argv[3]), sep=' ')
                ofile.write(tokenized_line)
