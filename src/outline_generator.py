import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
load_dotenv()

__all__ = ["generate_outline","generate_outline_gr"]

chat_model = ChatOpenAI(model=os.environ.get("CHAT_MODEL") if os.environ.get("CHAT_MODEL") is not None else "gpt-3.5-turbo", max_tokens=4096)

TITLE_TEMPLATE = """
    以{{theme}}为题生成一个既专业又吸引人的PPT标题。
    该标题应该简洁有力，同时吸引从业者和行业专家的注意。
    只返回标题的内容，不要有多余的符号
"""

OUTLINE_TEMPLATE = """
    使用markdown的格式根据主标题{{title}}生成一个中文大纲，遵循以下要求:
    1.用#号来标识大纲的层级机构。第一级(#)表示大纲的主标题，第二级(##)表示章节，第三级(###)表示章节的要点
    2.标题中只有中文，不要出现序号
    3.总共生成{{chapter_counts}}个章节，每个章节有{{keynote_counts}}个要点
    4.只返回大纲的内容，不要有多余的符号

    按以下格式返回:
        # 主标题
        ## 二级标题
        ### 三级标题
"""

BODY_TEMPLATE = """
    根据大纲{{outline}}填充markdown文本,同样以markdown的格式返回,遵循以下要求:
    1.不要丢失或改变原有的大纲markdown的内容
    2.根据每个要点扩写一到三个中文段落，每个段落必须使用<p></p>标签包裹
    3.只返回markdown的内容，不要有多余的说明

    按以下格式返回:
        # 主标题
        ## 二级标题
        ### 三级标题1
        <p>要点1</p>
        <p>要点2</p>
        ### 三级标题2
        <p>要点3</p>
"""

KEYWORDS_TEMPLATE = """
    你是一位插画师，现在有一段makdown格式的大纲{{body}}，找出大纲中被<p></p>包裹的段落，然后构思一些元素能够用插画的形式准确的表达出段落的内容
    用英文关键词来表达插画元素，不超过10个英文单词，然后用<k></k>标签将这些英文关键词包裹起来，并且插入对应的段落之后，返回markdown格式的大纲

    按以下格式返回:
        # 主标题
        ## 二级标题
        ### 三级标题1
        <p>三级标题扩写段落1</p>
        <k>keywords 1</k>
        <p>三级标题扩写段落2</p>
        <k>keywords 2</k>
        ### 三级标题2
        <p>三级标题扩写段落3</p>
        <k>keywords 3</k>
"""

def generate_outline(theme:str,chapter_counts:int,keynote_counts:int) -> str:
    output_parser = StrOutputParser()
    def complete(x: str) -> dict:
        return {"title": x,"chapter_counts":chapter_counts,"keynote_counts":keynote_counts}
    
    gen_title_prompt = PromptTemplate(template=TITLE_TEMPLATE, input_variables=["theme"],template_format="mustache")
    gen_outline_prompt = PromptTemplate(template=OUTLINE_TEMPLATE, input_variables=["title","chapter_counts","keynote_counts"],template_format="mustache")
    gen_body_prompt = PromptTemplate(template=BODY_TEMPLATE, input_variables=["outline"],template_format="mustache")
    gen_keywords_prompt = PromptTemplate(template=KEYWORDS_TEMPLATE, input_variables=["body"],template_format="mustache")
    ppt_chain = gen_title_prompt | chat_model | RunnableLambda(complete) | gen_outline_prompt | chat_model | gen_body_prompt | chat_model | gen_keywords_prompt | chat_model | output_parser
    response = ppt_chain.invoke(theme)
    return response

def generate_outline_gr(theme:str,chapter_counts:int,keynote_counts:int) -> str:
    return generate_outline(theme,chapter_counts,keynote_counts)