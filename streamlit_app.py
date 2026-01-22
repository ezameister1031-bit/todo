import streamlit as st
from supabase import create_client

# Supabase 接続
SUPABASE_URL = "https://supabase.com/dashboard/project/uidimomhqldplhtvbchz"
SUPABASE_KEY = "sb_publishable_rE4-yWr4dICRl3laxhjspA_mbAVh5TW"
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("📝 Todoリスト管理アプリ")

# --- Todo追加 ---
st.subheader("Todoを追加")

new_todo = st.text_input("やること")

if st.button("追加"):
    if new_todo:
        supabase.table("todos").insert({
            "title": new_todo
        }).execute()
        st.success("Todoを追加しました")
        st.rerun()

# --- Todo一覧 ---
st.subheader("Todo一覧")

todos = supabase.table("todos").select("*").order("created_at").execute().data

for todo in todos:
    col1, col2, col3 = st.columns([6, 2, 2])

    with col1:
        done = st.checkbox(
            todo["title"],
            value=todo["is_done"],
            key=todo["id"]
        )

        # 完了状態更新
        if done != todo["is_done"]:
            supabase.table("todos").update({
                "is_done": done
            }).eq("id", todo["id"]).execute()
            st.rerun()

    with col2:
        st.write("✅" if todo["is_done"] else "")

    with col3:
        if st.button("削除", key=f"del-{todo['id']}"):
            supabase.table("todos").delete().eq("id", todo["id"]).execute()
            st.rerun()


