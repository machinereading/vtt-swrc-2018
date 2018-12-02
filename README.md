# VTT SWRC 2018
## 개요
카이스트 [시맨틱웹첨단연구센터(SWRC)](http://semanticweb.kaist.ac.kr)의 VTT 프로젝트 2차년도(2018년) 연구 결과 통합 모듈 저장소 입니다. 대본에서 트리플(Triple) 형태로 표현되는 지식을 추출하는 모듈입니다. 크게 1. 자연어 전처리 모듈(input-parser), 2. 인물 개체 식별(character-identifier), 3. 표층형(Surface Form) 관계 추출, 이렇게 3가지로 구성되어 있습니다. 

## 환경설정
* 본 모듈은 python 3 기반으로 구현되었습니다.
* 다음 명령어를 통해 필요한 python 라이브러리들을 설치해 주세요. 
  * `pip install -r requirements.txt`
* `character-identifier/` 폴더 안으로 이동하여 아래 명령어를 통해 필요한 파일을 다운 받아주세요
  * `$ bash _fetch_data.sh`
* [Stanford Core NLP](https://stanfordnlp.github.io/CoreNLP/history.html) JAVA 라이브러를 다운로드 후 [open-ie/open_ie.py](open-ie/open_ie.py) 와 [input-parser/conll_file_generator.py](input-parser/conll_file_generator.py) 두 파일 4번째 줄에 아래와 같이 이 라이브러리 경로를 적어주세요
  * `nlp_parser = StanfordCoreNLP("your_Stanford_core_NLP_Java_library_directory")`


## 사용법
### Input
[input.json](input.json) 파일에 지식을 추출하고자 하는 대본 정보를 입력해주세요. 본 파일을 참조하면 되며 정보는 아래와 같습니다. 
```
{
	"scene_id":"friends-s01e01-00", // 임의의 문서 ID, String
	"sentences":[  // 대화 목록, Array
		{
			"speaker":"Monica Geller", // 화자, String
			"text":"There's nothing to tell! He's just some guy I work with!", // 대사, String
			"st":55422, // 대사의 시작 시간. ms. 정보를 모르면 0으로 적으면 됨, int
			"en":59256  // 대사의 시작 시간. ms. 정보를 모르면 0으로 적으면 됨, int
		}, ...
}
```
### 실행
 `python run.py` 파일을 실행시키면 output.json 이 생성 됩니다.
 
### Output
[output.json](output.json)에 지식 추출 결과가 저장됩니다. 본 파일을 참조하면 되며 정보는 아래와 같습니다. 
```
{
	"triples":[  // 지식 목록, Array
		{
			"source":"[Rachel Green] : ...", // 지식 출처 문장
			"sbj":"Rachel Green", // 주어 개체, String
			"relation":"'ll stay with", // 관계, String
			"obj":"Monica Geller"  // 목적어 개체, String
		}, ...
}
```

# Acknowledgements
* This work was supported by Institute for Information & communications Technology Promotion(IITP) grant funded by the Korea government(MSIT) (2017-0-01780, The technology development for event recognition/relational reasoning and learning knowledge based system for video understanding)

* 본 프로젝트는 requirements.txt에 적혀있는 파이썬 라이브러리 외에 아래 오픈소스의 도움을 받았습니다.
  * https://github.com/kentonl/e2e-coref
  * https://github.com/amore-upf/semeval2018-task4
  * https://github.com/emorynlp/semeval-2018-task4

