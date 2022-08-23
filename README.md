# MIDU2022 文本纠错调研

## 1. 语法纠错 [1][2]
传统方案（三段论 pipeline ）：错误检测，候选召回，候选排序

目前的研究方向：

* 训练数据自动构造：错误与正确文本数据 pair ，数据增强来逼近业务分布。

* 序列标注纠错：基于 token 进行增删改。
* 文本生成纠错：利用生成模型直接基于错误样本生成正确文本。

## 2. 中文错别字检查 [1]
中文错别字纠错（ Chinese Spelling Error Check ）的输入输出是完全对齐的，也就是错一个字改一个字。

## 3. Baseline解析
### 3.1 NEZHA+ERNIE+T5 [3]

使用 NEZHA 分类数据：错别字和语义错误；

对错别字先使用 ERNIE 纠错，无变化再下一步；

对语义错误先去重；

再使用 T5 纠正语义。

### 3.2 百度 UIE (ERNIE1.0) [4]

直接使用paddlenlp.TaskFlow.text_correction;

错纠情况很多！

（trick：针对A榜数据调研时发现，预处理中使用 zhconv 先将繁体字转为简体字，效果会不错。）

### 3.3 pycorrector (macbert) [5]

1、原始的mask策略不用多废话了；

2、wwm需要考虑分词器的分词结果，就是比如bert的分词器把某个词AB划分为两个subword A和B，则mask的时候将词AB的A和B的两个subword一起mask，因为二者的关联关系太强，会使得任务太easy；

3、n-gram mask，上升到词级别，原始mask和wwm都是在subword层面搞的，n-gram mask相当于一个对多个词构成的短语mask，至于1-gram，2-gram，3-gram，4-gram概率各不相同，具体忘记了可以参考mac bert中的介绍；

4、mac masking，不做mask，而是：

>我们建议不要使用[MASK]令牌进行掩蔽，因为令牌不会出现在微调阶段，我们建议使用类似的单词进行掩蔽。通过使用基于word2vec（Mikolov等人，2013）计算相似度的[英英解释工具包（Wang and Hu，2017）](https://link.zhihu.com/?target=https%3A//github.com/chatopera/Synonyms)获得相似的单词。如果选择一个N-gram进行遮罩，我们将分别找到相似的单词。在极少数情况下，当没有相似的单词时，我们将降级以使用随机单词替换。
mac-bert同时用了wwm、ngram mask和mac masking。

mac masking采用相似词进行代替【MASK】，这种切词MASK方式+同义词替换MASK，就有效解决了预训练阶段有mask标记，下游任务无mask，这种上下游任务不一致的问题。这也是MacBERT主要的改进点了。


## 4. 文本纠错大赛方案

我们基本继承了 Baseline 的思想框架，在实验中我们发现使用 ernie-csc 模型针对错别字进行纠错的效率比不上 macbert 模型；

随之我们进一步发现 macbert 的结果是较好的，因此我们主要使用了 macbert 作为单模型纠错的基础，后续在这上面进行模型融合。

首先我们在训练中发现 macbert 对于乱序的语法错误效果不佳，因此训练时在训练集中去除乱序数据，就可以很好地处理语义和拼写问题；

其次由于 T5 对于句子中缺失补齐非常有用，因此我们使用 T5 对 macbert 无法处理的错误进行补充；

最后采用 Nezha 模型对于生成结果进行再次分类，如果得到 Positive 结果证明纠错有效，得到其他标签则说明可能存在其他错误（我们发现标为 Positive 的 precision 很高，但是 recall 有待商榷，同时标为其他错误的 f1 很低，因此在比赛中没有引入重复循环纠错的 pipeline 设计）；

此外我们还参考了 HillZhang 大佬的纠错方案 [6]，试图使用 seq2edit 与 seq2seq 进行进一步的融合，但是提分效果不是很明显；

data 文件夹下的 same_pinyin 还记载了我们对同音同形混淆集解决拼写错误的尝试，由于时间关系没有融合进去。


## 5.总结

本次比赛的过程中我们涉足了许多之前未知的领域和知识，通过参考借鉴当今业界的部分方案 [6][7]，最终十分侥幸能够陪跑各个大佬挺进最后的决赛轮。

本项目出于技术整理和竞赛复盘的角度，欢迎大家一起学习讨论进步。

如果有任何问题，欢迎提 issue。




## 参考文献：

* 1. 文本语法纠错不完全调研：学术界 v.s. 工业界最新研究进展，[https://mp.weixin.qq.com/s/Dj8KIe6LbVGonV-Kk9mO2Q](https://mp.weixin.qq.com/s/Dj8KIe6LbVGonV-Kk9mO2Q)
* 2. Revisiting Pre-trained Models for Chinese Natural Language Processing，[https://arxiv.org/pdf/2004.13922.pdf](https://arxiv.org/pdf/2004.13922.pdf)
* 3. 文本智能校对Baseline，千鹤，[https://aistudio.baidu.com/aistudio/projectdetail/4340298](https://aistudio.baidu.com/aistudio/projectdetail/4340298)
* 4. PaddleNLP信息抽取技术重磅升级！开放域信息抽取来了！三行代码用起来~，[https://aistudio.baidu.com/aistudio/projectdetail/3914778](https://aistudio.baidu.com/aistudio/projectdetail/3914778)
* 5. pycorrector，[https://github.com/shibing624/pycorrector](https://github.com/shibing624/pycorrector)
* 6. MuCGEC: A Multi-Reference Multi-Source Evaluation Dataset for Chinese Grammatical Error Correction & SOTA Models，[https://github.com/HillZhang1999/MuCGEC](https://github.com/HillZhang1999/MuCGEC)
* 7. 竞赛大神易显维：带你深度认知文本校对和文本纠错问题，[https://www.bilibili.com/video/BV1fe4y1X7XW](https://www.bilibili.com/video/BV1fe4y1X7XW)
