import re
from random import randrange

def make_typo_in_sent(sent, word_typo_maker,
                      typo_ratio=0.5, strength='default'):
    # 공백 기준 토큰화 및 한국어로만 정제
    words = sent.split(' ')
    clean_words = []
    for i in range(len(words)):
        ko_word = re.compile(r'[가-힣]+').findall(words[i])
        clean_words.extend(ko_word)
        
        
    # 한국어와 한국어 사이에 특수문자, 영어 등이 포함된 경우 고려
    separate_idx = []
    val = 0
    for i in range(len(words)):
        ko_word = re.compile(r'[가-힣]+').findall(words[i])
        if len(ko_word) == 1: separate_idx.append(val)
        else:
            separate_idx.append(val)
            for _ in range(len(ko_word)-1):
                val += 1
                separate_idx.append(val) 
                
    
    # 한글자 이상인 단어 개수 * typo_ratio만큼 오타낼 예정
    over1_cnt = sum([1 if len(word) > 1 else 0 for word in clean_words])
    typo_word_cnt = int(over1_cnt * typo_ratio)
    #print(f'{typo_word_cnt}개의 단어로 오타를 만듭니다.')
    
    
    # 한글자 이상인 단어들 중 오타낼 단어 선택
    selected_idx = []
    for _ in range(typo_word_cnt):
        while True:
            temp = randrange(0, len(clean_words))
            if len(clean_words[temp]) < 2: continue
            if temp not in selected_idx:
                selected_idx.append(temp)
                break
            
            
    # 선택된 단어들로 오타 변형
    for idx in selected_idx:
        cur_word = clean_words[idx]
        try:
            new_word = word_typo_maker.make_typo_in_word(cur_word, strength)
        except: new_word = cur_word
        
        # 한국어와 한국어 사이에 특수문자, 영어 등이 포함된 경우 고려
        origin_idx = idx - separate_idx[idx]
        
        # 기존 문장에서 오타난 단어로 대체
        words[origin_idx] = words[origin_idx].replace(cur_word, new_word)
        #print(f'"{cur_word}" -> "{new_word}" 오타를 만들었습니다.')
    return ' '.join(words)