import pandas as pd
import joblib
from fastapi import FastAPI, Form
from sqlalchemy import create_engine, text

# 모델 및 데이터베이스 설정
model = joblib.load("getLocal.joblib")
db = create_engine("sqlite:///food.db")  # 전역 연결로 설정

# FastAPI 앱 초기화
app = FastAPI()

@app.get("/")
def root():
    return "테스트"

@app.post("/GetLocal")
def get_local(lat: str = Form(...), lon: str = Form(...), kind: str = Form("")):
    # 위도와 경도를 float으로 변환
    lat = float(lat)
    lon = float(lon)
    print((lat, lon))
    
    # 지역 예측
    prediction = model.predict([[lat, lon]])
    region = prediction[0]
    print(region)
    
    # 기본 쿼리와 파라미터 설정
    query = "SELECT 시설명 FROM food WHERE 지역명=:local"
    params = {'local': region}
    
    # `kind`가 주어지면 카테고리 필터 추가
    if kind:
        query += " AND 카테고리=:kind"
        params['kind'] = kind
    
    # SQL 쿼리 실행
    df = pd.read_sql(text(query), con=db, params=params)
    
    # 결과를 리스트로 반환
    return {'foods':list(df['시설명'])}
