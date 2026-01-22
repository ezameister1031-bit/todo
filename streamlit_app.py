import streamlit as st
from supabase import create_client
import datetime

# =====================
# Supabase 接続
# =====================
SUPABASE_URL = "https://uidimomhqldplhtvbchz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVpZGltb21ocWxkcGxodHZiY2h6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMjAyOTksImV4cCI6MjA4NDU5NjI5OX0.mzoug_p5WpFFQTUq-TTsffA8n7uRI77IqdZpAR5pTYg"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =====================
# タイトル
# =====================
st.title("📝 Todoリスト管理アプリ")

# =====================
# Todo 追加
# =====================
st.subheader("Todoを追加")

new_todo = st.text_input("やること")
due_date = st.date_input("期限", value=None)

if st.button("追加"):
    if new_todo:
        res = supabase.table("todos").insert({
            "title": new_todo,
            # date → 文字列に変換（重要）
            "due_date": due_date.isoformat() if due_date else None
        }).execute()

        if res.data is None:
            st.error("Todoの追加に失敗しました")
            st.write(res)
            st.stop()

        st.success("Todoを追加しました")
        st.rerun()
    else:
        st.warning("やることを入力してください")

# =====================
# Todo 一覧
# =====================
st.subheader("Todo一覧")

res = supabase.table("todos").select("*").order("created_at").execute()
todos = res.data or []

if not todos:
    st.info("Todoはまだありません")

for todo in todos:
    col1, col2, col3 = st.columns([5, 3, 2])

    # --- チェックボックス（完了）
    with col1:
        done = st.checkbox(
            todo["title"],
            value=todo["is_done"],
            key=todo["id"]
        )

        if done != todo["is_done"]:
            supabase.table("todos").update({
                "is_done": done
            }).eq("id", todo["id"]).execute()
            st.rerun()

    # --- 期限表示
    with col2:
        due = todo.get("due_date")
        st.write(f"📅 {due}" if due else "期限なし")

    # --- 削除
    with col3:
        if st.button("削除", key=f"del-{todo['id']}"):
            supabase.table("todos").delete().eq("id", todo["id"]).execute()
            st.rerun()
