import re
from typing import List

from openai import OpenAI

from main.utils.log import get_logger

logger = get_logger(name="utils.llm")

client = OpenAI(base_url="", api_key="")


# model = "gpt-4o-mini" || aws-llama3.2:3b || aws-llama3.2:11b
def check_relatedness(query, content, model="gpt-4o-mini"):
    logger.info(f"query={query}")
    logger.info(f"content={content}")
    prompt = f"判断以下查询问题是否与文章相关：\n\n查询问题: {query}\文章内容: {content}\n\n请回答“相关”或“不相关”。"
    # prompt = f"判断以下两个句子是否相关：\n\n句子1: {sentence1}\n句子2: {sentence2}\n\n请回答“相关”或“不相关”。"
    chat = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model=model,
    )
    result = chat.choices[0].message.content
    if result == "相关":
        logger.info(f"result={result}")
        return True
    logger.error(f"result={result}")
    return False


def check_relatedness_v2(query: str, titles: List[str], model="gpt-4o"):
    title_list = [f"{i+1}. {title}" for i, title in enumerate(titles)]
    title_list = "\n".join(title_list)
    # prompt = f"判断查询问题与哪些文章相关：\n\n查询问题: {sentence2}\n文章标题如下: {titles}\n\n请回答与查询问题可能相关的文章序号，以逗号分隔，不需要给出标题内容，不要空格，也不要其他词汇。"
    prompt = f"判断查询问题与哪些文章相关：\n\n查询问题: {query}\n文章标题如下: {title_list}\n\n请回答与查询问题肯定不相关的文章序号，以逗号分隔，不需要给出标题内容，不要空格，也不要其他词汇。"
    chat = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model=model,
        temperature=0.0,
    )
    result = chat.choices[0].message.content
    numbers = re.findall(r"\d+", result)
    if not numbers:
        return titles
    numbers = [int(number) for number in numbers]
    titles_negtive = [titles[number - 1] for number in numbers]
    for title in titles_negtive:
        logger.info(f"[Negtive] {title}")
    titles_positive = list(set(titles) - set(titles_negtive))
    return titles_positive


if __name__ == "__main__":
    # 示例用法
    #     titles = """1. 技能人才落户可以随迁配偶、未成年子女吗?
    # 2. 杭州人才引进落户申请条件有哪些？
    # 3. 杭州全日制本科和硕士学历人才最新落户政策
    # 4. 杭州人才落户怎么选择落户地址？
    # 5. 杭州全日制本科和硕士学历人才最新落户政策
    # 6. 杭州技能人才落户需要什么条件？
    # 7. 省外22届本科毕业生可以落户杭州吗？
    # 8. 杭州全日制本科和硕士学历人才最新落户政策
    # 9. 2021怎样才能落户杭州
    # 10. 2022杭州人才引进落户条件详情
    # 11. 杭州积分落户2024年新政策
    # 12. 杭州全日制本科和硕士学历人才最新落户政策
    # 13. 杭州人才落户申请条件一览
    # 14. 2023年杭州户籍政策改革有什么区别？"""
    sentence1 = "人才落户政策有哪些？"
    sentence2 = "人才落户"

    relatedness = check_relatedness_v2(sentence1, sentence2, model="gpt-4o")
    print(f"句子1: {sentence1}")
    print(f"句子2: {sentence2}")
    print(f"相关性判断: {relatedness}")
