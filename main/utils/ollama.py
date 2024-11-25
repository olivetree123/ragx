from typing import Literal

from ollama import Client
from ollama import ChatResponse


class OllamaClient(object):
    client = Client(host="http://localhost:11434")

    @classmethod
    def check_relatedness(cls, query: str, title: str,
                          model: Literal["llama3.2:3b", "qwen2.5:7b"]):
        prompt = f"判断以下查询问题是否与文章相关：\n\n文章标题: {title}\n查询问题: {query}\n\n请回答“相关”或“不相关”。"
        messages = [{"role": "user", "content": prompt}]
        response: ChatResponse = cls.client.chat(model="llama3.2:3b",
                                                 messages=messages)
        print("response: ", response.message.content)
        result = response.message.content
        if result == "相关":
            return True
        return False


# client = Client(host="http://localhost:11434",
#                 headers={"x-some-header": "some-value"})
# response: ChatResponse = client.chat(model="llama3.2",
#                                      messages=[
#                                          {
#                                              "role": "user",
#                                              "content": "Why is the sky blue?",
#                                          },
#                                      ])
# print(response["message"]["content"])
# # or access fields directly from the response object
# print(response.message.content)
