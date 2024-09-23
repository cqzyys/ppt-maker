## PPT-MAKER
### 项目概述
输入一句简单的提示语，AI根据提示语自动规划PPT大纲，然后根据大纲自动生成PPT。
### 安装步骤
**poetry(推荐)**

1. 下载项目源代码```git clone https://github.com/cqzyys/ppt-maker.git```

2. 安装poetry(类似于pip、conda的包管理器)，[poetry官方文档](https://python-poetry.org/docs/)

3. 先激活python环境```poetry shell```，再安装依赖包```poetry install```

4. 复制.env.example文件为.env文件，并修改OPENAI_API_KEY为你的openai_key，OPENAI_BASE_URL、CHAT_MODEL、IMAGE_MODEL根据你的实际需要修改

5. ```python webui.py```[启动web页面](http://127.0.0.1:7860)

**pip install**

1. 下载项目源代码```git clone https://github.com/cqzyys/ppt-maker.git```

2. 切换到你的python环境

3. 安装依赖包```pip install -r requirements.txt```

4. 复制.env.example文件为.env文件，并修改OPENAI_API_KEY为你的openai key，OPENAI_BASE_URL、CHAT_MODEL、IMAGE_MODEL根据你的实际需要修改

5. ```python webui.py```[启动web页面](http://127.0.0.1:7860)

### outline语法
项目根据用户的提示语生成outline，其格式大致如下：
```
    # 揭秘太阳系奥秘：星系之舞，探索宇宙起源
    <sub>2024科普演讲</sub>
    ## 第一章 太阳系概览
    ### 第一节 太阳系的基本组成
    <p>太阳系是由太阳及其周围的八大行星、五颗矮行星、无数的小行星、彗星以及卫星等组成的庞大系统。太阳是这个系统中的核心，占据了太阳系99.86%的质量，其余天体围绕着太阳进行公转。</p>
    <k>core sun, planets, dwarf planets, asteroids, comets, moons</k>
    <p>太阳系中的行星分为类地行星和类木行星。类地行星包括水星、金星、地球和火星，它们主要由岩石和金属组成。类木行星则包括木星、土星、天王星和海王星，它们以巨大的气体和冰层为主。</p>
    <k>terrestrial planets, gas giants, rocky composition, icy layers</k>
    <p>除行星外，太阳系中还有许多小行星、彗星以及卫星。这些小天体在太阳系中扮演着重要的角色，它们为科学家提供了研究太阳系起源和演化的宝贵资料。</p>
    <k>minor bodies, research, solar system origin, evolution</k>
```
其中，```#```代表PPT的标题(必须)，```<sub></sub>```代表PPT的副标题(非必须)，```##```代表章节，```###```代表章节的要点，```<p></p>```代表文本内容(可以根据实际需要修改)，```<k></k>```代表文本关键词(必须为英文，用于之后的图片检索或者生成，可以根据实际需要修改)，如果关键词始终不足以完全表达你所希望的图片，你也可以直接使用```<img>你的图片的url</img>```来代替```<k></k>```

如果生成的outline的格式跟上述格式差异较大，有可能是因为：
1. 大语言模型的能力较弱。可以在.env文件中配置CHAT_MODEL为gpt-4o或者能力更强的模型
2. 由于大语言模型生成时具有一定的随机性，小概率会生成不符合的outline，可以重新生成outline再看看格式是否正常

### 项目的不足

1. 目前只有blue-line和purple-modern两种ppt母版
2. 每种母版只支持TITLE_ONLY、TITLE_WITH_PICTURE、TITLE_AND_CONTENT、CONTENT_WITH_PICTURE、TWO_CONTENTS、TWO_CONTENTS_WITH_PICTURE、THREE_CONTENTS、THREE_CONTENTS_WITH_PICTURE有限的几种布局形式

是的，我们缺少专业的ppt母版制作人员，如果你擅长PPT母版制作且对本项目感兴趣，希望你能加入我们，我们会将突出贡献者列为本项目的主要作者

## 引用

如果本项目有帮助到您的研究，请引用我们：

```
@software{ppt-maker,
    title        = {{ppt-maker}},
    author       = {Andy Zhou,Colin Wang,Wang Hong},
    year         = 2024,
    journal      = {GitHub repository},
    publisher    = {GitHub},
    howpublished = {\url{https://github.com/cqzyys/ppt-maker.git}}
}
```
