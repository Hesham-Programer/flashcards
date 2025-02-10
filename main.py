import streamlit as st
import base64

if 'cards' not in st.session_state:
    st.session_state.cards = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

def add_card(image, definition):
    """إضافة بطاقة تعل    يمية جديدة مع صورة وتعريف"""
    if image and definition.strip() != '':
        image_bytes = image.getvalue()
        st.session_state.cards.append({
            "image": image_bytes,
            "definition": definition.strip(),
            "mime_type": image.type
        })
        st.session_state.current_index = len(st.session_state.cards) - 1
        st.session_state.show_answer = False

st.title("📷 تطبيق بطاقات الصور التعليمية")
st.markdown("قم بتحميل الصور وتعلم تعريفاتها!")

with st.form("add_card_form"):
    image = st.file_uploader("اضف صورة", type=["png", "jpg", "jpeg"])
    definition = st.text_input("تعريف")
    submitted = st.form_submit_button("اضف بطاقة")

if submitted:
    if image and definition.strip() != '':
        add_card(image, definition)
    else:
        st.error("يرجى تقديم صورة وتعريف")

if len(st.session_state.cards) == 0:
    st.info("لا توجد بطاقات تعليمية بعد. قم بتحميل صورتك الأولى أعلاه!")
else:
    current_card = st.session_state.cards[st.session_state.current_index]

    st.markdown(
        f"""
        <div style="
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            padding: 20px;
            margin: 10px 0;
            background-color: white;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            {f'<h3 style="text-align: center; color: #333333;">{current_card["definition"]}</h3>' if st.session_state.show_answer else 
            f'<img src="data:{current_card["mime_type"]};base64,{base64.b64encode(current_card["image"]).decode()}" style="max-width: 100%; max-height: 400px;"/>'}
        </div>
        """,
        unsafe_allow_html=True
    )

    flip_button_text = "عرض التعريف" if not st.session_state.show_answer else "عرض الصورة"
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("⬅️ السابق", on_click=lambda: st.session_state.update(current_index=max(0, st.session_state.current_index-1), show_answer=False))
    with col2:
        st.button(f"🔁 {flip_button_text}", on_click=lambda: st.session_state.update(show_answer=not st.session_state.show_answer))
    with col3:
        st.button("➡️ التالي", on_click=lambda: st.session_state.update(current_index=min(len(st.session_state.cards)-1, st.session_state.current_index+1), show_answer=False))

    st.caption(f"البطاقة {st.session_state.current_index + 1} من {len(st.session_state.cards)}")