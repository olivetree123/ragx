import re
from typing import List

from langchain.text_splitter import MarkdownHeaderTextSplitter


class MarkChunkHandler(object):
    split_chunk_pattern = "！|。|\n|；|;"
    min_chunk_len = 10

    @classmethod
    def handle(cls, chunk_list: List[str]):
        """
        对文本按语句进行拆分
        - 根据分隔符！|。|\n|；|;对文本进行拆分。切片后，如果某一段内容长度小于20，将它与前面一段进行拼接；
        - 拆分后，将每个片段转成向量保存到向量数据库；
        """
        result = []
        for chunk in chunk_list:
            base_chunk = re.split(cls.split_chunk_pattern, chunk)
            base_chunk = [
                chunk.strip() for chunk in base_chunk if len(chunk.strip()) > 0
            ]
            result_chunk = []
            for c in base_chunk:
                if len(result_chunk) == 0:
                    result_chunk.append(c)
                else:
                    if len(result_chunk[-1]) < cls.min_chunk_len:
                        result_chunk[-1] = result_chunk[-1] + "。" + c
                    else:
                        if len(c) < cls.min_chunk_len:
                            result_chunk[-1] = result_chunk[-1] + "。" + c
                        else:
                            result_chunk.append(c)
            result += result_chunk
        return result


class DocPart(object):

    def __init__(self, title, content):
        self.title = title
        self.content = content


class MarkdownSplitter(object):
    delimiters = [
        ("#", "Header1"),
        ("##", "Header2"),
        ("###", "Header3"),
    ]
    text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=delimiters)

    @classmethod
    def split_text(cls, text: str) -> List[DocPart]:
        """对文章进行分段(paragraph)"""
        result = []
        documents = cls.text_splitter.split_text(text=text)
        for doc in documents:
            header1 = doc.metadata.get("Header1")
            header2 = doc.metadata.get("Header2")
            header3 = doc.metadata.get("Header3")
            headers = [header1, header2, header3]
            title = " ".join([h for h in headers if h])
            result.append(DocPart(title=title, content=doc.page_content))
        return result
