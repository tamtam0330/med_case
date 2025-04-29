import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from search_engine import MedicalCaseSearch

# Streamlit 설정
st.set_page_config(
    page_title="의료판례검색",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 검색 엔진 초기화
@st.cache_resource
def init_search_engine():
    return MedicalCaseSearch()

search_engine = init_search_engine()

# CSS 스타일
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .search-box {
        width: 100%;
        padding: 1rem;
        font-size: 1.2rem;
        border-radius: 25px;
        border: 1px solid #dfe1e5;
    }
    .search-box:focus {
        outline: none;
        box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
    }
    .case-card {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        background-color: #f8f9fa;
        transition: all 0.3s ease;
    }
    .case-card:hover {
        background-color: #e9ecef;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'sort_order' not in st.session_state:
    st.session_state.sort_order = "최신순"
if 'department' not in st.session_state:
    st.session_state.department = "전체"
if 'time_filter' not in st.session_state:
    st.session_state.time_filter = "전체"
if 'search' not in st.session_state:
    st.session_state.search = st.session_state.search_query
if 'sort_select' not in st.session_state:
    st.session_state.sort_select = st.session_state.sort_order
if 'department_select' not in st.session_state:
    st.session_state.department_select = st.session_state.department
if 'time_select' not in st.session_state:
    st.session_state.time_select = st.session_state.time_filter


# 검색 인터페이스
st.title("🏥 의료판례 검색 서비스")

# 검색창
search_query = st.text_input(
    "검색어",
    placeholder="판례 검색어를 입력하세요 (예: 의료사고, 과실, 손해배상)", 
    key="search",
    on_change=lambda: st.session_state.update(
            search_query=st.session_state.search
        )
)

# 필터 옵션
col1, col2, col3 = st.columns(3)

with col1:
    sort_order = st.selectbox(
        "정렬 순서",
        ["최신순", "유사도순"],
        key="sort_select",
        on_change=lambda: st.session_state.update(
            sort_order=st.session_state.sort_select,
            search_query=st.session_state.search
        )
    )

with col2:
    department = st.selectbox(
        "진료과",
        ["전체", "내과", "외과", "정형외과", "신경외과", "산부인과", "소아과", "이비인후과", "안과", "피부과"],
        key="department_select",
        on_change=lambda: st.session_state.update(
            department=st.session_state.department_select,
            search_query=st.session_state.search
        )
    )

with col3:
    time_filter = st.selectbox(
        "기간",
        ["전체", "최근 1년", "최근 3년", "최근 5년"],
        key="time_select"
    )

# st.write(st.session_state)

# 검색 결과 표시
if st.session_state.search_query:
    # 검색 실행
    cases = search_engine.search_cases(
        query=st.session_state.search_query,
        department=st.session_state.department
    )
    
    # 정렬
    if st.session_state.sort_order == "최신순":
        cases.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    else:  # 유사도순
        cases.sort(key=lambda x: x['score'], reverse=True)
    
    # 결과 표시
    st.subheader(f"검색 결과 ({len(cases)}건)")
    
    for idx, case in enumerate(cases):
        with st.expander(f"**{case['title']}** ({case['court']} {case['case_number']}) (유사도: {case['score']:.2f})"):
            st.write(f"**진료과:** {case['department']}")
            st.write(f"**판결일자:** {case['date']}")
            st.write(f"**사건 개요:** {case['summary']}")
            st.write(f"**키워드:** {', '.join(case['keywords'])}")
        
            # 판례 전문 보기 버튼
            if st.button("판례 전문 보기", key=f"btn_{case['department']}_{case['case_number']}_{idx}"):
                st.session_state['selected_case'] = case
                st.switch_page("pages/case_detail.py")
      
        