import os
import subprocess

# 0.Input Parsing : Raw Text -> CoNLL Format(ner, pos, dependency...)
print ('[Step0 Start] Running Input NLP Parser Module...')
os.chdir('./input-parser')
print ('  ---NLP Parsing(pos,dependency,ner)...')
os.system('python conll_file_generator.py')
print ('  ---Done')
print ('  ---Detecting Mention...')
os.system('python conll_file_mention_detector.py')
print ('  ---Done')
os.chdir('..')
os.system('cp ./input-parser/friends.test.scene_delim.conll ./character-identifier/data/friends/friends.test.scene_delim.conll')
print ('[Step0 Done] Character Entity Identified')

# 1.Charater Identification
print ('[Step1 Start] Running Character Entity Identification Module...')
os.chdir('./character-identifier')
os.system('python main.py --deploy_data test --model models/ptmodel/ckpt --no_cuda')
os.chdir('..')
print ('[Step1 Done] Character Entity Identified')

# 2.Open Information Extration
print ('[Step2 Start] Running Open IE to get Triples...')
os.system('cp ./character-identifier/models/ptmodel/answers/friends_test_scene/ckpt--ensemble.csv ./open-ie/ckpt--ensemble.csv')
os.chdir('./open-ie')
os.system('python open_ie.py')
os.chdir('..')
print ('[Step2 Done] Open IE done')
