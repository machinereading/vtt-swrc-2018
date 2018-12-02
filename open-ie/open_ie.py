import json
from stanfordcorenlp import StanfordCoreNLP

nlp_parser = StanfordCoreNLP('../stanford-corenlp-full-2018-10-05')

def get_entity_id_name_map():
    f = open('friends_entity_map.txt','r',encoding='utf-8')
    entity_map = {}
    for line in f:
        eid, ename = line.strip().split('\t')
        entity_map[eid] = ename
    f.close()
    return entity_map

def get_origin_sent_list():
    try:
        with open('../input.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return None
    return data["sentences"]

def get_mention_character_map(entity_map):
    f = open('ckpt--ensemble.csv', 'r', encoding='utf-8')
    line_num = 0
    mention_character_map = {}
    for line in f:
        line_num += 1
        if (line_num <= 2):
            continue
        index, eid, _ = line.strip().split()
        mention_character_map[index] = entity_map[eid]

    f.close()
    return mention_character_map


def write_open_ie_result(open_ie_result):
    output_obj = {}
    output_obj['triples'] = []
    for item in open_ie_result:
        output_obj['triples'].append({
            'source': item['source_sentence'],
            'sbj': item['sbj'],
            'relation': item['relation'],
            'obj' : item['obj']
        })
    f_write = open('../output.json','w',encoding='utf-8')
    f_write.write(json.dumps(output_obj,ensure_ascii=False,indent=4))
    f_write.close()

def parse_open_ie():
    global nlp_parser
    entity_map = get_entity_id_name_map()
    origin_sent_list = get_origin_sent_list()
    mention_character_map = get_mention_character_map(entity_map)

    open_ie_result = []
    token_idx = 0
    for idx,sent in enumerate(origin_sent_list):
        speaker = sent["speaker"]
        text = sent["text"]
        props = {'annotators': 'openie', 'pipelineLanguage': 'en', 'outputFormat': 'json'}
        result = json.loads(nlp_parser.annotate(text, properties=props))

        source_sentence = '[' + speaker + '] : ' + text

        for sentresult in result['sentences']:
            token_list = sentresult['tokens']
            for token in token_list:
                token['is_resolved'] = False
                if (str(token_idx) in mention_character_map):
                    token['is_resolved'] = True
                    token['character_name'] = mention_character_map[str(token_idx)]
                token_idx += 1

            for triple in sentresult['openie']:
                sbj = triple['subject']
                relation = triple['relation']
                obj = triple['object']

                if (triple['subjectSpan'][1] - triple['subjectSpan'][0] == 1):
                    if (token_list[triple['subjectSpan'][0]]['is_resolved'] == True):
                        sbj = token_list[triple['subjectSpan'][0]]['character_name']

                if (triple['objectSpan'][1] - triple['objectSpan'][0] == 1):
                    if (token_list[triple['objectSpan'][0]]['is_resolved'] == True):
                        obj = token_list[triple['objectSpan'][0]]['character_name']
                open_ie_result.append({'source_sentence': source_sentence, 'sbj':sbj, 'relation':relation, 'obj':obj})
        write_open_ie_result(open_ie_result)

if __name__ == '__main__':
    parse_open_ie()