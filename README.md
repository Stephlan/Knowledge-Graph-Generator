# Knowledge Graph Generator



## Introduction

This project aims at generating knowledge graph for any target field. It provides every common user access to their on knowledge bases. The only thing it necessarily requires is the name of the target fields. Following the guideline will show examples using topic -- "Medical". However, it is highly recommended to fully utilize all the functionalities of the project by adding supporting materials like books. The more materials you fed to the system, the broader the knowledge range and the higher accuracy could it achieve.

The whole process contains four steps:  

1. **Collecting Knowledge** from Internet & Books
2. **Extracting Entity Relations** Based on NLP
3. **Constructing Knowledge Graph** with Graphic Database
4. **Evaluating Current Knowledge and Deciding Corrections** 



## Structure

```
|____ Datasets	// Data collected by spiders and book provided by users
|	  |__ NFolders
|	  |		|__cutFolders.py
|	  |__ PreProcess.py
|	  |__ book.doc
|	  |__ book.txt	  
|
|____ Evaluator
|	  |__ BookLearner.py
|	  |__ CleanResult.py
|	  |__ DependencyParser.py
|	  |__ EvaluteCredits.py
|	  |__ NeoManager.py
|
|____ Learner
|	  |__ Two-Layer Learner
|	  |__ config.py
|	  |__ initial.py
|	  |__ Learner.py
|	  |__ network.py
|	  |__ runModelOnBookKnowledge.py
|	  |__ Seq2seq.py
|	  |__ test_GRU.py
|	  |__ test.txt
|	  |__ train_GRU.py
|
|____ Spider
|	  |__
|	  |__
|	  |__
|	  |__
|	  |__
|	  |__
|
|____ Utils
|
|____ README.md

```



## Setup



## Demonstration



## Details



## Contacts

Feel free to mail: yhan.lan2017@gmail.com / yhlan@zju.edu.cn

