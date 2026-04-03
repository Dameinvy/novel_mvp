from fastapi import FastAPI
from engine import generate_outline, generate_chapter, rewrite_chapter

app = FastAPI()

# 简单内存数据库（MVP用）
STORY_DB = {}


@app.get("/")
def root():
    print("🔥 VERSION 2026-04-03")
    return {"msg": "AI Novel API Running"}


# 创建小说
@app.post("/create_story")
def create_story(topic: str):
    outline = generate_outline(topic)

    story_id = str(len(STORY_DB) + 1)

    STORY_DB[story_id] = {
        "topic": topic,
        "outline": outline,
        "chapters": [],
        "memory": ""
    }

    return {
        "story_id": story_id,
        "outline": outline
    }


# 生成章节
@app.post("/generate_chapter")
def gen_chapter(story_id: str, chapter_no: int):
    story = STORY_DB.get(story_id)

    if not story:
        return {"error": "story not found"}

    chapter = generate_chapter(
        story["outline"],
        story["memory"],
        chapter_no
    )

    story["chapters"].append(chapter)
    story["memory"] = chapter[-500:]

    return {"chapter": chapter}


# 爆点改写
@app.post("/rewrite_boom")
def rewrite(story_id: str, chapter_index: int):
    story = STORY_DB.get(story_id)

    if not story:
        return {"error": "story not found"}

    if chapter_index >= len(story["chapters"]):
        return {"error": "chapter not exist"}

    chapter = story["chapters"][chapter_index]
    new_chapter = rewrite_chapter(chapter)

    story["chapters"][chapter_index] = new_chapter

    return {"chapter": new_chapter}
