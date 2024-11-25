from openai import OpenAI

client = OpenAI(base_url="", api_key="")


def check_relatedness(sentence1, sentence2):
    # prompt = f"判断以下查询问题是否与文章相关：\n\n文章标题: {sentence1}\n查询问题: {sentence2}\n\n请回答“相关”或“不相关”。"
    prompt = f"判断以下两个句子是否相关：\n\n句子1: {sentence1}\n句子2: {sentence2}\n\n请回答“相关”或“不相关”。"
    chat = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model="gpt-4o-mini",
    )
    result = chat.choices[0].message.content
    if result == "相关":
        return True
    return False


# 示例用法
sentence1 = "人才落户政策有哪些？"
sentence2 = "老年人落户"

relatedness = check_relatedness(sentence1, sentence2)
print(f"句子1: {sentence1}")
print(f"句子2: {sentence2}")
print(f"相关性判断: {relatedness}")
