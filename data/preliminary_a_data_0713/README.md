# 文本智能校对大赛(初赛a)-数据集
## source: https://aistudio.baidu.com/aistudio/projectdetail/4357987

## **背景描述**
智能文本校对大赛的初赛(a)数据集, 包括训练集、验证集、测试集。参赛队伍需提交针对测试集的预测结果文件。

## **数据说明**

### 数据文件

> 数据文件都为json格式，可使用json读取加载

- preliminary_train：伪数据约100w, 均为负样本
- preliminary_extend_train: 真实场景训练数据约1000条, 均为负样本
- preliminary_val：真实场景下验证集约1000条(包括约500条正样本和500条负样本）
- preliminary_a_test_source: 真实场景下测试集约1000条（包括约500条正样本和500条负样本）

### json文件字段说明

- id: 文本id
- source: 源文本（可能包含错误的文本）
- target: 目标文本（正确文本）
- type: positive代表正样本， negative代表负样本

## 初赛(a)提交格式

### 提供preliminary_a_test_source.json文件内容示例

```
[
    {
        "source": "领导的按排，我坚决服从",
        "id": 1
    },
    {
        "source": "今天的天气真错！",
        "id": 2
    }
]
```
### 提交preliminary_a_test_inference.json文件内容示例

- 初赛提交JSON文件名为: preliminary_a_test_inference.json

```
[
    {
        "inference": "领导的安排，我坚决服从",
        "id": 1
    },
    {
        "inference": "今天的天气真不错！",
        "id": 2
    }
]
```