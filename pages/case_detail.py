import streamlit as st
from search_engine import MedicalCaseSearch
import glob
import os

# 검색 엔진 초기화
@st.cache_resource
def init_search_engine():
    return MedicalCaseSearch()

# st.write(st.session_state)
search_engine = init_search_engine()
# 스타일 설정
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .case-header {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .case-content {
        padding: 1rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 뒤로가기 버튼
if st.button("← 검색 결과로 돌아가기"):
    st.switch_page("main.py")


if 'selected_case' in st.session_state:
    case = st.session_state['selected_case']
    
    # 헤더 섹션
    st.markdown(f"""
        <div class="case-header">
            <h1>{case['title']}</h1>
            <p><strong>사건번호:</strong> {case['case_number']}</p>
            <p><strong>법원:</strong> {case['court']}</p>
            <p><strong>판결일자:</strong> {case['date']}</p>
            <p><strong>진료과:</strong> {case['department']}</p>
            <p><strong>키워드:</strong> {', '.join(case['keywords'])}</p>
        </div>
    """, unsafe_allow_html=True)
   
    # 판례 전문
    full_text = case['full_text']
    if full_text:
        with st.container(border=True):
           st.markdown(full_text, unsafe_allow_html=True)
    else:
        st.error("판례 전문을 불러올 수 없습니다.")
else:
    st.error("선택된 판례가 없습니다. 검색 결과 페이지에서 판례를 선택해주세요.")     
