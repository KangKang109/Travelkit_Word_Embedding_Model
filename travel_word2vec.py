import re
from konlpy.tag import Okt
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors

# Okt 형태소 분석기 초기화
okt = Okt()

# 불용어 리스트
stopwords = ['은', '는', '이', '가', '에', '의', '을', '를', '도', '다', '로', '과', '하고', '에서', '더', '으로', '하다']

# 텍스트 파일 읽기
with open('C:\\Users\\minwo\\Documents\\word2vec\\crawled_data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 텍스트 전처리 함수
def preprocess_text_korean(text):
    text = text.lower()  # 소문자 변환
    text = re.sub(r'[^ㄱ-ㅎ가-힣\s]', '', text)  # 특수문자 제거 (한글과 공백만 유지)
    tokens = okt.morphs(text)  # 형태소 분석
    tokens = [word for word in tokens if word not in stopwords]  # 불용어 제거
    return tokens

# 텍스트 전처리
processed_text = preprocess_text_korean(text)

# 형태소 분석 후 빈 문자열 제거
processed_text = [token for token in processed_text if token.strip()]

# 형태소 분석 후 비어 있는지 확인
if not processed_text:
    print("전처리된 텍스트가 비어 있습니다!")
else:
    print(f"전처리된 텍스트 예시: {processed_text[:10]}")  # 일부 출력

# 문장 단위로 나누기 (이 부분에서 여러 문장으로 나누어야 합니다)
sentences = text.split('\n')  # 줄바꿈을 기준으로 여러 문장으로 나누기
sentences = [preprocess_text_korean(sentence) for sentence in sentences]  # 각 문장 전처리
sentences = [[token for token in sentence if token.strip()] for sentence in sentences]  # 빈 문자열 제거

# 형태소 분석 후 첫 몇 문장을 출력하여 확인
print(f"전처리된 첫 3개 문장: {sentences[:3]}")

# Word2Vec 모델 학습
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# 모델을 텍스트 형식으로 저장
txt_model_path = 'C:\\Users\\minwo\\Documents\\word2vec\\word2vec_model_korean.txt'
model.wv.save_word2vec_format(txt_model_path, binary=False)  # 텍스트 형식으로 저장
print(f"한글 Word2Vec 모델 학습 완료 및 저장!")

# 모델 로딩 확인
try:
    loaded_model = KeyedVectors.load_word2vec_format(txt_model_path, binary=False)
    print(f"모델 로딩 완료: {loaded_model}")
except Exception as e:
    print(f"모델 로딩 중 오류 발생: {e}")
