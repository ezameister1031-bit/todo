import streamlit as st
from supabase import create_client
import datetime


# Supabase 接続
SUPABASE_URL = "https://uidimomhqldplhtvbchz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVpZGltb21ocWxkcGxodHZiY2h6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMjAyOTksImV4cCI6MjA4NDU5NjI5OX0.mzoug_p5WpFFQTUq-TTsffA8n7uRI77IqdZpAR5pTYg"
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


st.title("📝 Todoリスト管理アプリ")

# --- Todo追加 ---
st.subheader("Todoを追加")

new_todo = st.text_input("やること")
due_date = st.date_input(
    "期限",
    value=None
)


if st.button("追加"):
    if new_todo:
        supabase.table("todos").insert({
            "title": new_todo,
            "due_date": due_date
        }).execute()
        st.success("Todoを追加しました")
        st.rerun()


# --- Todo一覧 ---
st.subheader("Todo一覧")

res = supabase.table("todos").select("*").order("created_at").execute()


todos = res.data or []

for todo in todos:
    col1, col2, col3 = st.columns([5, 3, 2])

    with col1:
        done = st.checkbox(
            todo["title"],
            value=todo["is_done"],
            key=todo["id"]
        )

    with col2:
        if todo["due_date"]:
            st.write(f"📅 {todo['due_date']}")
        else:
            st.write("期限なし")



