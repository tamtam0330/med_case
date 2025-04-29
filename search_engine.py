from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import streamlit as st

class MedicalCaseSearch:
    def __init__(self):
        # QdrantDB 클라이언트 설정
        self.client = QdrantClient(
            url="http://192.168.45.157:6333",
        )
        
        # 임베딩 모델 로드
        try:
            self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS', device='cpu')
        except Exception as e:
            st.error(f"모델 로드 중 오류 발생: {str(e)}")
            self.model = None
        
        # 컬렉션 이름
        self.collection_name = "medical_cases"
    
    def search_cases(self, query, department="전체", limit=10):
        """판례 검색"""
        if self.model is None:
            st.error("모델이 초기화되지 않았습니다.")
            return []
            
        # 쿼리 임베딩 생성
        try:
            query_embedding = self.model.encode(query)
        except Exception as e:
            st.error(f"임베딩 생성 중 오류 발생: {str(e)}")
            return []
        
        # 검색 필터 설정
        search_filter = None
        if department != "전체":
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="department",
                        match=models.MatchValue(value=department)
                    )
                ]
            )
        
        # 유사도 검색
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                query_filter=search_filter,
                limit=limit
            )
        except Exception as e:
            st.error(f"검색 중 오류 발생: {str(e)}")
            return []
        
        # 결과 처리
        cases = []
        for result in search_results:
            case = result.payload
            case['score'] = result.score  # 유사도 점수 추가
            cases.append(case)
        
        return cases
    