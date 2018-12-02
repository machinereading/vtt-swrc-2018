def attach_mention():
    f = open('friends.test.womention.scene_delim.conll','r',encoding='utf-8')
    line_list = [line.strip() for line in f]
    f.close()

    line_len = len(line_list)
    touched = [False for _ in range(line_len)]


    ner_count = 0
    pronoun_count = 0
    general_noun_count = 0

    # PERSON NER Detect
    for ner_len in reversed(range(1,5)):
        for i in range(line_len-ner_len):
            st = i
            en = i + ner_len

            is_ner = True
            for k in range(st,en):
                items = line_list[k].split()
                if (len(items) < 5):
                    is_ner = False
                    break
                t = items[-2]
                if (touched[k] or t != '(PERSON)'):
                    is_ner = False
                    break

            if (is_ner):
                ner_count += 1
                if (ner_len > 1):
                    line_list[st] = line_list[st][:-1] + '(0'
                    line_list[en-1] = line_list[en-1][:-1] + '0)'
                else:
                    line_list[st] = line_list[st][:-1] + '(0)'
                for k in range(st,en):
                    touched[k] = True

    # PRONOUN DETECT
    pronoun_list = ['i', 'my', 'me', 'mine', 'you', 'your', 'yours', 'she', 'her', 'hers', 'he', 'his', 'him', 'myself', 'yourself', 'herself', 'himself']
    pronoun_list_soyu = ['mine', 'hers', 'his', 'yours']
    for i in range(line_len):
        items = line_list[i].split()
        if (len(items) < 5):
            continue
        word = items[3].lower()
        pos = items[4]
        if (not touched[i]):
            if ( ('PRP' in pos and word in pronoun_list) or (word in pronoun_list_soyu)):
                pronoun_count += 1
                touched[i] = True
                line_list[i] = line_list[i][:-1] + '(0)'


    # PERSON
    f = open('personal_noun_list.txt','r',encoding='utf-8')
    personal_noun_list = [line.strip() for line in f]
    f.close()

    for i in range(line_len):
        items = line_list[i].split()
        if (len(items) < 5):
            continue
        word = items[3].lower()
        pos = items[4]
        if (not touched[i]):
            if (pos.startswith('NN') and 'S' not in pos and word in personal_noun_list):
                general_noun_count += 1
                touched[i] = True
                line_list[i] = line_list[i][:-1] + '(0)'


    f_write = open('friends.test.scene_delim.conll','w',encoding='utf-8')
    for line in line_list:
        f_write.write(line + '\n')
    f_write.close()

if __name__ == '__main__':
    attach_mention()
