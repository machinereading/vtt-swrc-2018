import os
import subprocess

print ('[Step1 Start] Running Character Entity Identification Module...')
os.chdir('./character-identifier')
os.system('python main.py --deploy_data test --model models/ptmodel/ckpt')
os.chdir('..')
print ('[Step1 Done] Character Entity Identified')