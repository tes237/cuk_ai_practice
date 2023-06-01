import pandas as pd
import numpy as np

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer(self, input_sentence):
        
        #레벤 슈타인 거리를 저장할 리스트
        similarities = []
        
        #question 리스트 루프를 돌면서 question 문장들과 내 문장들 사이에 레벤슈타인 거리를 모두 리스트에 insert
        for q_dic_sentense in self.questions:
            res = self.calc_distance(input_sentence, q_dic_sentense)
            similarities.append(res)
        
        best_match_index = np.argmin(similarities)   # 레벤슈타인거리 값이 가장 작은 값의 인덱스를 반환

        #해당 인덱스의 답변을 리턴
        return self.answers[best_match_index]

        # 레벤슈타인 거리 구하기
    def calc_distance(self, a, b):
        ''' 레벤슈타인 거리 계산하기 '''
        if a == b: return 0 # 같으면 0을 반환
        a_len = len(a) # a 길이
        b_len = len(b) # b 길이
        if a == "": return b_len
        if b == "": return a_len

        matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
        for i in range(a_len+1): # 0으로 초기화
            matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
        # 0일 때 초깃값을 설정
        for i in range(a_len+1):
            matrix[i][0] = i
        for j in range(b_len+1):
            matrix[0][j] = j
        # 표 채우기 --- (※2)
        for i in range(1, a_len+1):
            ac = a[i-1]
            for j in range(1, b_len+1):
                bc = b[j-1] 
                cost = 0 if (ac == bc) else 1  #  파이썬 조건 표현식 예:) result = value1 if condition else value2
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                ])
        return matrix[a_len][b_len]

# CSV 파일 경로를 지정하세요.
filepath = 'C:\\src\\python\\cuk\\ai_practice\\report2\\new_chatbot\\cuk_ai_practice\\ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)

# 실행결과
# You: 회사 퇴사해야지
# Chatbot: 부지런하시네요.
# You: 너도 퇴사해라
# Chatbot: 저도 몰랐어요.
# You: AI 개발 실무 과목 화이팅
# Chatbot: 시간을 정해보세요.
# You: