import json
from stanfordcorenlp import StanfordCoreNLP

nlp_parser = StanfordCoreNLP('../stanford-corenlp-full-2018-10-05')

def generate_conll_lines(path):
    global nlp_parser
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return None
    output_lines = []
    scene_id = data['scene_id']
    sentences = data['sentences']
    output_lines.append('#begin document ({}); part000\n'.format(scene_id))
    for sent_count,sent in enumerate(sentences):
        speaker = sent['speaker'].replace(' ', '_')
        st_time = str(sent['st'])
        en_time = str(sent['en'])
        text = str(sent['text'])
        props = {'annotators': 'tokenize,pos,lemma,ner,depparse', 'pipelineLanguage': 'en', 'outputFormat': 'conll'}
        result = nlp_parser.annotate(text, properties=props)
        conll_lines = result.split('\n')

        token_count = 0
        for conll_line in conll_lines:
            if (len(conll_line) < 2):
                if (output_lines[-1] != '\n'):
                    output_lines.append('\n')
            else:
                items = conll_line.split()
                utid, word, lemma, pos, ner, dep_tag = items[0], items[1], items[2], items[3], items[4], items[6]

                if (len(ner) > 6):
                    ner = ner[0:6]
                ner = '*' if ner == 'O' else '(' + ner + ')'

                output_lines.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    scene_id, str(sent_count), str(token_count), word, pos, dep_tag, lemma, '-', '-', speaker, ner, st_time, en_time, '000.pickle', '-'
                ))
                token_count += 1

    output_lines.append('#end document\n')
    return output_lines



if __name__ == '__main__':
    result = generate_conll_lines('../input.json')
    if result is None:
        print ('Error : Fail to parse JSON input')

    f_write = open('friends.test.womention.scene_delim.conll', 'w', encoding='utf-8')
    for line in result:
        f_write.write(line)
    f_write.close()