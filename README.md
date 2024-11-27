# Travelkit_Word_Embedding_Model

실행 순서
1.  crawling_travel.py 실행  -->  crawled_data.txt 파일 생성(덮어쓰기)   //파일 저장 위치 지정 필요
2.  travel_word2vec.py 실행 -->    word2vec_model_korean.txt 모델 생성(덮어쓰기 XX) //파일 위치 지정 필요    (단어 임베딩 모델 : 60mb라 업로드 불가) 
3.  WordCFTest.java 실행  --> 단어 의미 유사도 출력 // 파일 위치 지정 필요
