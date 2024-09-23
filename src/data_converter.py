from collections import deque
from typing import List, Optional
import re
from enum import Enum, auto
from langchain_core.pydantic_v1 import BaseModel

class FeatureType(Enum):
    BLANK = auto()
    CENTER_TITLE_ONLY = auto()
    CENTER_TITLE_WITH_PICTURE = auto()
    CENTER_TITLE_AND_SUBTITLE = auto()
    CENTER_TITLE_AND_SUBTITLE_WITH_PICTURE = auto()
    TITLE_ONLY = auto()
    TITLE_WITH_PICTURE = auto()
    TITLE_AND_CONTENT = auto()
    CONTENT_WITH_PICTURE = auto()
    CONTENT_WITH_TABLE = auto()
    CONTENT_WITH_CHART = auto()
    TWO_CONTENTS = auto()
    TWO_CONTENTS_WITH_PICTURE = auto()
    THREE_CONTENTS = auto()
    THREE_CONTENTS_WITH_PICTURE = auto()

class Feature(BaseModel):
    type: FeatureType = FeatureType.BLANK
    placeholder_types: Optional[List[int]] = [] 

    def inference_type(self):
        if self.placeholder_types == [3]:
            return FeatureType.CENTER_TITLE_ONLY
        if self.placeholder_types == [3, 18]:
            return FeatureType.CENTER_TITLE_WITH_PICTURE        
        elif self.placeholder_types == [3, 4]:
            return FeatureType.CENTER_TITLE_AND_SUBTITLE
        elif self.placeholder_types == [3, 4, 18]:
            return FeatureType.CENTER_TITLE_AND_SUBTITLE_WITH_PICTURE        
        elif self.placeholder_types == [1]:
            return FeatureType.TITLE_ONLY
        elif self.placeholder_types == [1, 18]:
            return FeatureType.TITLE_WITH_PICTURE        
        elif self.placeholder_types == [1, 7]:
            return FeatureType.TITLE_AND_CONTENT
        elif self.placeholder_types == [1, 7, 18]:
            return FeatureType.CONTENT_WITH_PICTURE
        elif self.placeholder_types == [1, 2, 18]:
            return FeatureType.CONTENT_WITH_PICTURE
        elif self.placeholder_types == [1, 7, 12]:
            return FeatureType.CONTENT_WITH_TABLE
        elif self.placeholder_types == [1, 7, 8]:
            return FeatureType.CONTENT_WITH_CHART       
        elif self.placeholder_types == [1, 7, 7]:
            return FeatureType.TWO_CONTENTS
        elif self.placeholder_types == [1, 2, 7]:
            return FeatureType.TWO_CONTENTS        
        elif self.placeholder_types == [1, 7, 7, 18, 18]:
            return FeatureType.TWO_CONTENTS_WITH_PICTURE
        elif self.placeholder_types == [1, 7, 7, 7]:
            return FeatureType.THREE_CONTENTS
        elif self.placeholder_types == [1, 7, 7, 7, 18, 18, 18]:
            return FeatureType.THREE_CONTENTS_WITH_PICTURE
        else:
            return FeatureType.BLANK

    def set_placeholder_types(self,placeholder_types:List[int]):
        self.placeholder_types = placeholder_types
        self.type = self.inference_type()

class ImageType(Enum):
    KEYWORD = auto()
    URL = auto()

class Image(BaseModel):
    type:ImageType = 1
    value:str = ""

class Element(BaseModel):
    title:str = ""
    contents:Optional[List[str]] = []
    images:Optional[List[Image]] = []
    level:int = 0
    feature:Optional[Feature] = None

class Node(Element):
    children: Optional[List[Element]] = []

class Root(Node):
    level = 1
    subtitle: Optional[str] = ""
    children: Optional[List[Node]] = []
    nodes: Optional[List[Node]] = []
    def complete_nodes(self):
        if len(self.images) ==1 and self.subtitle is not None:
            self.feature = Feature(type=FeatureType.CENTER_TITLE_AND_SUBTITLE_WITH_PICTURE)
        elif len(self.images) ==1 and self.subtitle is None:
            self.feature = Feature(type=FeatureType.CENTER_TITLE_WITH_PICTURE)
        elif len(self.images) ==0 and self.subtitle is not None:
            self.feature = Feature(type=FeatureType.CENTER_TITLE_AND_SUBTITLE)
        else:
            self.feature = Feature(type=FeatureType.CENTER_TITLE_ONLY)
        for node in self.nodes:
            contents_counts = len(node.contents)
            images_counts = len(node.images)            
            if contents_counts ==0 and images_counts ==0:
                node.feature = Feature(type=FeatureType.TITLE_ONLY)
            elif contents_counts ==1 and images_counts ==0:
                node.feature = Feature(type=FeatureType.TITLE_AND_CONTENT)
            elif contents_counts ==2 and images_counts ==0:
                node.feature = Feature(type=FeatureType.TWO_CONTENTS)
            elif contents_counts ==3 and images_counts ==0:
                node.feature = Feature(type=FeatureType.THREE_CONTENTS)
            elif contents_counts ==1 and images_counts ==1:
                node.feature = Feature(type=FeatureType.CONTENT_WITH_PICTURE)                
            elif contents_counts ==2 and images_counts ==2:
                node.feature = Feature(type=FeatureType.TWO_CONTENTS_WITH_PICTURE)
            elif contents_counts ==3 and images_counts ==3:
                node.feature = Feature(type=FeatureType.THREE_CONTENTS_WITH_PICTURE)
            else:

                raise Exception(f"Not support {contents_counts} contents and {images_counts} images feature")

def get_level(line):
    if bool(re.match(r'^#(?!#)', line)):
        return 1
    if bool(re.match(r'^##(?!#)', line)):
        return 2
    if bool(re.match(r'^###(?!#)', line)):
        return 3
    return None


def markdown2Root(markdown_text:str):
    markdown_text = markdown_text.strip('\n')
    if markdown_text.startswith("```markdown"):
        markdown_text = markdown_text[11:]
    if markdown_text.startswith("```md"):
        markdown_text = markdown_text[5:]
    if markdown_text.startswith("```"):
        markdown_text = markdown_text[3:]
    if markdown_text.endswith("```"):
        markdown_text = markdown_text[:-3]
    lines = markdown_text.split('\n')
    root = Root()
    stack = deque([root])
    for line in lines:
        line = line.strip()
        if line.strip() == "":
            continue
        level = get_level(line)
        if level is not None:
            title = line.strip('#').strip()
            if level == 1:
                root.title = title
            else:
                new_node = Node(title=title, level=level, contents=[], images=[], children=[])
                while len(stack) >= level:
                    stack.pop()
                stack[-1].children.append(new_node)
                stack.append(new_node)
                root.nodes.append(new_node)
        elif bool(re.match(r'^<p>(?!<p>)', line)):
            content = line[line.index('<p>')+3:line.index('</p>')]
            if content:
                stack[-1].contents.append(content.strip())
        elif bool(re.match(r'^<img>(?!<img>)', line)):
            img_url = line[line.index('<img>')+5:line.index('</img>')]
            if img_url:
                stack[-1].images.append(Image(type=ImageType.URL, value=img_url.strip()))
        elif bool(re.match(r'^<k>(?!<k>)', line)):
            keyword = line[line.index('<k>')+3:line.index('</k>')]
            if keyword:
                stack[-1].images.append(Image(type=ImageType.KEYWORD, value=keyword.strip()))
        elif bool(re.match(r'^<sub>(?!<sub>)', line)):
            subtitle = line[line.index('<sub>')+5:line.index('</sub>')]
            if subtitle and stack[-1].level == 1:
                stack[-1].subtitle = subtitle.strip()
    root.complete_nodes()
    return root