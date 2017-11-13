from src.inlp.script import indian_language_scripts as si

chillu_char_map = {
    u'\u0d7a': u'\u0d23',
    u'\u0d7b': u'\u0d28',
    u'\u0d7c': u'\u0d30',
    u'\u0d7d': u'\u0d32',
    u'\u0d7e': u'\u0d33',
    u'\u0d7f': u'\u0d15',
}
char_chillu_map = {}
for k, v in chillu_char_map.iteritems():
    char_chillu_map[v] = k


def orthographic_syllabify_improved(word, lang):
    word_mask = ['0'] * len(word)
    p_vectors = [si.get_phonetic_feature_vector(c, lang) for c in word]
    syllables = []
    syllables_mask = []
    for i in xrange(len(word)):
        v = p_vectors[i]
        syllables.append(word[i])
        syllables_mask.append(word_mask[i])
        # simplified syllabification 
        # if i+1<len(word) and \
        #        (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
        #    syllables.append(u' ')
        #    syllables_mask.append(u'0')
        # elif not si.is_valid(v) or si.is_misc(v) or si.is_vowel(v):
        #    syllables.append(u' ')
        #    syllables_mask.append(u'0')
        # elif i+1<len(word) and \
        #     (si.is_consonant(v) or si.is_nukta(v)) and \
        #     (si.is_consonant(p_vectors[i+1]) or si.is_anusvaar(p_vectors[i+1])):
        #    syllables.append(u' ')
        #    syllables_mask.append(u'0')
        # better syllabification 
        if i + 1 < len(word) and (not si.is_valid(p_vectors[i + 1]) or si.is_misc(p_vectors[i + 1])):
            syllables.append(u' ')
            syllables_mask.append(u'0')
        elif not si.is_valid(v) or si.is_misc(v):
            syllables.append(u' ')
            syllables_mask.append(u'0')
        elif si.is_vowel(v):
            anu_nonplos = (i + 2 < len(word) and \
                           si.is_anusvaar(p_vectors[i + 1]) and \
                           not si.is_plosive(p_vectors[i + 2]) \
                           )
            anu_eow = (i + 2 == len(word) and \
                       si.is_anusvaar(p_vectors[i + 1]))
            if not (anu_nonplos or anu_eow):
                syllables.append(u' ')
                syllables_mask.append(u'0')
        elif i + 1 < len(word) and \
                (si.is_consonant(v) or si.is_nukta(v)):
            if si.is_consonant(p_vectors[i + 1]):
                syllables.append(u' ')
                syllables_mask.append(u'0')
            elif si.is_vowel(p_vectors[i + 1]) and \
                    not si.is_dependent_vowel(p_vectors[i + 1]):
                syllables.append(u' ')
                syllables_mask.append(u'0')
            elif si.is_anusvaar(p_vectors[i + 1]):
                anu_nonplos = (i + 2 < len(word) and \
                               not si.is_plosive(p_vectors[i + 2]) \
                               )
                anu_eow = i + 2 == len(word)
                if not (anu_nonplos or anu_eow):
                    syllables.append(u' ')
                    syllables_mask.append(u'0')
    syllables_mask = u''.join(syllables_mask)
    syllables = u''.join(syllables)
    # assert len(syllables_mask) == len(syllables)
    # assert syllables_mask.find('01') == -1
    if syllables_mask.find('01') >= 0:
        print 'Warning'
    return syllables.strip().split(u' ')


def orthographic_syllabify(word, lang):
    p_vectors = [si.get_phonetic_feature_vector(c, lang) for c in word]
    syllables = []
    for i in xrange(len(word)):
        v = p_vectors[i]
        syllables.append(word[i])
        # simplified syllabification 
        # if i+1<len(word) and \
        #        (not si.is_valid(p_vectors[i+1]) or si.is_misc(p_vectors[i+1])):
        #    syllables.append(u' ')
        # elif not si.is_valid(v) or si.is_misc(v) or si.is_vowel(v):
        #    syllables.append(u' ')
        # elif i+1<len(word) and \
        #     (si.is_consonant(v) or si.is_nukta(v)) and \
        #     (si.is_consonant(p_vectors[i+1]) or si.is_anusvaar(p_vectors[i+1])):
        #    syllables.append(u' ')
        # better syllabification 
        if i + 1 < len(word) and (not si.is_valid(p_vectors[i + 1]) or si.is_misc(p_vectors[i + 1])):
            syllables.append(u' ')
        elif not si.is_valid(v) or si.is_misc(v):
            syllables.append(u' ')
        elif si.is_vowel(v):
            anu_nonplos = (i + 2 < len(word) and \
                           si.is_anusvaar(p_vectors[i + 1]) and \
                           not si.is_plosive(p_vectors[i + 2]) \
                           )
            anu_eow = (i + 2 == len(word) and \
                       si.is_anusvaar(p_vectors[i + 1]))
            if not (anu_nonplos or anu_eow):
                syllables.append(u' ')
        elif i + 1 < len(word) and \
                (si.is_consonant(v) or si.is_nukta(v)):
            if si.is_consonant(p_vectors[i + 1]):
                syllables.append(u' ')
            elif si.is_vowel(p_vectors[i + 1]) and \
                    not si.is_dependent_vowel(p_vectors[i + 1]):
                syllables.append(u' ')
            elif si.is_anusvaar(p_vectors[i + 1]):
                anu_nonplos = (i + 2 < len(word) and \
                               not si.is_plosive(p_vectors[i + 2]) \
                               )
                anu_eow = i + 2 == len(word)
                if not (anu_nonplos or anu_eow):
                    syllables.append(u' ')
    return u''.join(syllables).strip().split(u' ')


def orthographic_simple_syllabify(word, lang):
    p_vectors = [si.get_phonetic_feature_vector(c, lang) for c in word]
    syllables = []
    for i in xrange(len(word)):
        v = p_vectors[i]
        syllables.append(word[i])
        # simplified syllabification 
        if i + 1 < len(word) and \
                (not si.is_valid(p_vectors[i + 1]) or si.is_misc(p_vectors[i + 1])):
            syllables.append(u' ')
        elif not si.is_valid(v) or si.is_misc(v) or si.is_vowel(v):
            syllables.append(u' ')
        elif i + 1 < len(word) and \
                (si.is_consonant(v) or si.is_nukta(v)) and \
                (si.is_consonant(p_vectors[i + 1]) or si.is_anusvaar(p_vectors[i + 1])):
            syllables.append(u' ')
    return u''.join(syllables).strip().split(u' ')
