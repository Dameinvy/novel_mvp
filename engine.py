import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def call_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=2000
    )
    return response["choices"][0]["message"]["content"]


# =========================
# 1. 生成100章大纲
# =========================
def generate_outline(topic):
    prompt = f"""
你是专业网文策划。

生成一个100章小说大纲：

题材：{topic}

要求：
- 100章
- 每10章一个阶段
- 主角成长清晰
- 持续冲突
- 爽点密集

输出格式：
第1章：xxx
...
第100章：xxx
"""
    return call_llm(prompt)


# =========================
# 2. 生成章节
# =========================
def generate_chapter(outline, memory, chapter_no):
    prompt = f"""
你是网文作者。

【小说大纲】
{outline}

【前情摘要】
{memory}

请写第{chapter_no}章：

要求：
- 连贯剧情
- 不崩人设
- 推动主线
- 有冲突
- 1500字左右
- 结尾留悬念
"""
    return call_llm(prompt)


# =========================
# 3. 爆点改写
# =========================
def rewrite_chapter(chapter):
    prompt = f"""
你是爆款小说改写专家。

请优化以下内容，使其更吸引人：

要求：
- 冲突更强
- 节奏更快
- 情绪更高
- 更容易上瘾

原文：
{chapter}
"""
    return call_llm(prompt)
