import streamlit as st
import requests

# 👉 上线后改成你的 Render 地址
API = "https://novel-mvp.onrender.com"

st.title("📚 AI番茄小说生成器")

# 输入题材
topic = st.text_input("输入小说题材（例如：都市+系统+逆袭）")

if st.button("生成小说大纲"):
    res = requests.post(f"{API}/create_story", params={"topic": topic})
    data = res.json()

    st.session_state["story_id"] = data["story_id"]
    st.session_state["outline"] = data["outline"]

    st.success("大纲生成成功！")

# 显示大纲
if "outline" in st.session_state:
    st.text_area("📖 100章大纲", st.session_state["outline"], height=300)


# 章节生成
if "story_id" in st.session_state:

    chapter_no = st.number_input("章节号", min_value=1, value=1)

    if st.button("生成章节"):
        res = requests.post(
            f"{API}/generate_chapter",
            params={
                "story_id": st.session_state["story_id"],
                "chapter_no": chapter_no
            }
        )
        st.session_state["chapter"] = res.json()["chapter"]

# 显示章节
if "chapter" in st.session_state:
    st.text_area("📄 章节内容", st.session_state["chapter"], height=400)


# 爆点优化
if st.button("🔥 爆点优化当前章节"):
    if "story_id" in st.session_state:
        res = requests.post(
            f"{API}/rewrite_boom",
            params={
                "story_id": st.session_state["story_id"],
                "chapter_index": 0
            }
        )
        st.text_area("🚀 优化后章节", res.json()["chapter"], height=400)
