import streamlit as st

# --- 초기 설정(세션 상태) ---
if "notes" not in st.session_state:
    # notes 리스트에, 각각 { 'text': "메모내용", 'favorite': bool } 구조로 저장
    st.session_state.notes = []

if "new_note" not in st.session_state:
    st.session_state.new_note = ""

if "edit_index" not in st.session_state:
    # 현재 수정 중인 메모의 인덱스 (없으면 -1)
    st.session_state.edit_index = -1

if "edit_text" not in st.session_state:
    # 수정 시 임시로 메모 내용을 담아두는 상태
    st.session_state.edit_text = ""

# --- 기능 함수들 ---
def add_note():
    """새로운 메모 추가"""
    note_content = st.session_state.new_note.strip()
    if note_content:
        st.session_state.notes.append({
            'text': note_content,
            'favorite': False
        })
    # 메모 입력창 초기화
    st.session_state.new_note = ""

def delete_note(index):
    """메모 삭제"""
    st.session_state.notes.pop(index)

def toggle_favorite(index):
    """메모 즐겨찾기 토글"""
    st.session_state.notes[index]['favorite'] = not st.session_state.notes[index]['favorite']

def start_edit(index):
    """메모 수정 모드 진입"""
    st.session_state.edit_index = index
    st.session_state.edit_text = st.session_state.notes[index]['text']

def save_edit(index):
    """메모 수정 사항 저장"""
    edited_content = st.session_state.edit_text.strip()
    if edited_content:
        st.session_state.notes[index]['text'] = edited_content
    # 수정 모드에서 빠져나오기
    st.session_state.edit_index = -1
    st.session_state.edit_text = ""

def cancel_edit():
    """메모 수정 취소"""
    st.session_state.edit_index = -1
    st.session_state.edit_text = ""

# --- 메인 화면 구성 ---
st.title("간단 메모장")

# 1) 메모 추가 섹션
st.subheader("새 메모 작성")
st.text_input("메모 내용", key="new_note", on_change=None)
st.button("추가", on_click=add_note)

st.divider()  # 구분선

# 2) 즐겨찾기 메모 목록 섹션 (새로 추가된 부분)
st.subheader("즐겨찾기 메모 목록")

# 즐겨찾기된 메모의 인덱스만 추출
favorite_indices = [i for i, note in enumerate(st.session_state.notes) if note["favorite"]]

if not favorite_indices:
    st.info("즐겨찾기로 등록된 메모가 없습니다.")
else:
    for i in favorite_indices:
        note = st.session_state.notes[i]

        # 수정 모드인 경우
        if st.session_state.edit_index == i:
            st.text_input("메모 수정", key="edit_text")
            col_save, col_cancel = st.columns([1, 1])
            with col_save:
                st.button("저장", on_click=save_edit, args=(i,))
            with col_cancel:
                st.button("취소", on_click=cancel_edit)
            st.write("---")

        else:
            # 즐겨찾기 표시(⭐)는 이미 favorite_notes 섹션이므로 자동으로 즐겨찾기된 것임
            st.markdown(f"**⭐ {i+1}. {note['text']}**")

            col_del, col_fav, col_edit = st.columns([1, 1, 1])
            with col_del:
                st.button("삭제", on_click=delete_note, args=(i,),
                          key=f"delete_fav_{i}")
            with col_fav:
                st.button("즐겨찾기 해제", on_click=toggle_favorite, args=(i,),
                          key=f"favorite_fav_{i}")
            with col_edit:
                st.button("수정", on_click=start_edit, args=(i,),
                          key=f"edit_fav_{i}")
            st.write("---")

st.divider()

# 2) 기존 메모 목록 표시
st.subheader("메모 목록")
if not st.session_state.notes:
    st.info("아직 메모가 없습니다. 메모를 추가해보세요!")
else:
    for i, note in enumerate(st.session_state.notes):
        # (A) 수정 모드인 경우
        if st.session_state.edit_index == i:
            st.text_input("메모 수정", key="edit_text")
            col_save, col_cancel = st.columns([1, 1])
            with col_save:
                st.button("저장", on_click=save_edit, args=(i,))
            with col_cancel:
                st.button("취소", on_click=cancel_edit)
            st.write("---")

        # (B) 일반 메모 표시인 경우
        else:
            # 즐겨찾기 여부에 따라 별(⭐) 표시
            favorite_star = "⭐ " if note['favorite'] else ""
            st.markdown(f"**{favorite_star}{i+1}. {note['text']}**")

            col_del, col_fav, col_edit = st.columns([1, 1, 1])
            with col_del:
                st.button("삭제", on_click=delete_note, args=(i,),
                          key=f"delete_{i}")
            with col_fav:
                st.button("즐겨찾기", on_click=toggle_favorite, args=(i,),
                          key=f"favorite_{i}")
            with col_edit:
                st.button("수정", on_click=start_edit, args=(i,),
                          key=f"edit_{i}")
            st.write("---")
