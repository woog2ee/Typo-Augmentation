from random import randrange
from soynlp.hangle import compose, decompose, character_is_korean

class WordTypoMaker():
    # jaso_near: 키보드 상에서 각 자소와 한 칸 이내로 가까운 자소들의 리스트
    def __init__(self):
        # ㅂ, ㅈ, ㄷ, ㄱ, ㅅ
        self.bieup_near  = ['ㅈ', 'ㅁ']
        self.jieut_near  = ['ㅂ', 'ㄷ', 'ㄴ']
        self.digeut_near = ['ㅈ', 'ㄱ', 'ㅇ'] 
        self.giyeok_near = ['ㄷ', 'ㅅ', 'ㄹ']
        self.siot_near   = ['ㄱ', 'ㅎ']
        # ㅁ, ㄴ, ㅇ, ㄹ, ㅎ
        self.mieum_near  = ['ㅂ', 'ㄴ', 'ㅋ']
        self.nieun_near  = ['ㅈ', 'ㅁ', 'ㅇ', 'ㅌ']
        self.ieung_near  = ['ㄷ', 'ㄴ', 'ㄹ', 'ㅊ']
        self.rieul_near  = ['ㄱ', 'ㅇ', 'ㅎ', 'ㅍ']
        self.hieut_near  = ['ㅅ', 'ㄹ', 'ㅍ']
        # ㅋ, ㅌ, ㅊ, ㅍ, 
        self.kieuk_near  = ['ㅁ', 'ㅌ']
        self.tieut_near  = ['ㄴ', 'ㅋ', 'ㅊ']
        self.chieut_near = ['ㅇ', 'ㅌ', 'ㅍ']
        self.pieup_near  = ['ㄹ', 'ㅊ']
        
        # ㅛ, ㅕ, ㅑ, ㅐ, ㅔ
        self.yo_near  = ['ㅕ', 'ㅗ']
        self.yeo_near = ['ㅛ', 'ㅑ', 'ㅓ']
        self.ya_near  = ['ㅕ', 'ㅐ', 'ㅓ']
        self.ae_near  = ['ㅑ', 'ㅔ', 'ㅏ']
        self.e_near   = ['ㅐ', 'ㅣ']
        # ㅗ, ㅓ, ㅏ, ㅣ
        self.o_near   = ['ㅛ', 'ㅓ', 'ㅠ']
        self.eo_near  = ['ㅕ', 'ㅗ', 'ㅏ', 'ㅜ']
        self.a_near   = ['ㅑ', 'ㅓ', 'ㅣ', 'ㅡ']
        self.i_near   = ['ㅔ', 'ㅏ']
        # ㅠ, ㅜ, ㅡ
        self.yu_near  = ['ㅗ', 'ㅜ']
        self.u_near   = ['ㅓ', 'ㅠ', 'ㅡ']
        self.eu_near  = ['ㅏ', 'ㅜ']
        
        # ㄲ, ㄸ, ㅃ, ㅆ, ㅉ
        self.ssang_giyeok_near = ['ㄱ'] + self.giyeok_near
        self.ssang_digeut_near = ['ㄷ'] + self.digeut_near
        self.ssang_bieup_near  = ['ㅂ'] + self.bieup_near
        self.ssang_siot_near   = ['ㅅ'] + self.siot_near
        self.ssang_jieut_near  = ['ㅈ'] + self.jieut_near
        
        # ㄳ, ㄵ, ㄶ, ㄺ, ㄻ, ㄼ, ㄾ, ㅀ, ㅄ
        self.giyeok_siot_near  = ['ㄱ', 'ㅅ']
        self.nieun_jieut_near  = ['ㄴ', 'ㅈ']
        self.nieun_hieut_near  = ['ㄴ', 'ㅎ']
        self.rieul_giyeok_near = ['ㄹ', 'ㄱ']
        self.rieul_mieum_near  = ['ㄹ', 'ㅁ']
        self.rieul_bieup_near  = ['ㄹ', 'ㅂ']
        self.rieul_tieut_near  = ['ㄹ', 'ㅌ']
        self.rieul_hieut_near  = ['ㄹ', 'ㅎ']
        self.bieup_siot_near   = ['ㅂ', 'ㅅ']
        
        # ㅒ, ㅖ, ㅚ, ㅟ, ㅢ
        self.yae_near = ['ㅐ'] + self.ae_near
        self.ye_near  = ['ㅔ'] + self.e_near
        self.oe_near  = ['ㅗ', 'ㅣ']
        self.wi_near  = ['ㅜ', 'ㅣ']
        self.ui_near  = ['ㅡ', 'ㅣ']
        # ㅘ, ㅝ, ㅙ, ㅞ
        self.wa_near  = ['ㅗ', 'ㅏ']
        self.wo_near  = ['ㅜ', 'ㅓ']
        self.wae_near = ['ㅗ', 'ㅐ']
        self.we_near  = ['ㅜ', 'ㅔ']
        
        
    # 입력된 자소에 따라 대응되는 가까운 자소들의 리스트 리턴
    def match_near_jaso(self, jaso):    
        if jaso == 'ㅂ': return self.bieup_near
        elif jaso == 'ㅈ': return self.jieut_near
        elif jaso == 'ㄷ': return self.diguet_near
        elif jaso == 'ㄱ': return self.giyeok_near
        elif jaso == 'ㅅ': return self.siot_near
        elif jaso == 'ㅁ': return self.mieum_near
        elif jaso == 'ㄴ': return self.nieun_near
        elif jaso == 'ㅇ': return self.ieung_near
        elif jaso == 'ㄹ': return self.rieul_near
        elif jaso == 'ㅎ': return self.hieut_near
        elif jaso == 'ㅋ': return self.kieuk_near
        elif jaso == 'ㅌ': return self.tieut_near
        elif jaso == 'ㅊ': return self.chieut_near
        elif jaso == 'ㅍ': return self.pieup_near
        
        elif jaso == 'ㅛ': return self.yo_near
        elif jaso == 'ㅕ': return self.yeo_near
        elif jaso == 'ㅑ': return self.ya_near
        elif jaso == 'ㅐ': return self.ae_near
        elif jaso == 'ㅔ': return self.e_near
        elif jaso == 'ㅗ': return self.o_near
        elif jaso == 'ㅓ': return self.eo_near
        elif jaso == 'ㅏ': return self.a_near
        elif jaso == 'ㅣ': return self.i_near
        elif jaso == 'ㅠ': return self.yu_near
        elif jaso == 'ㅜ': return self.u_near
        elif jaso == 'ㅡ': return self.eu_near
        
        elif jaso == 'ㄲ': return self.ssang_giyeok_near
        elif jaso == 'ㄸ': return self.ssang_digeut_near
        elif jaso == 'ㅃ': return self.ssang_bieup_near
        elif jaso == 'ㅆ': return self.ssang_siot_near
        elif jaso == 'ㅉ': return self.ssang_jieut_near
        
        elif jaso == 'ㄳ': return self.giyeok_siot_near
        elif jaso == 'ㄵ': return self.nieun_jieut_near
        elif jaso == 'ㄶ': return self.nieun_hieut_near
        elif jaso == 'ㄺ': return self.rieul_giyeok_near
        elif jaso == 'ㄻ': return self.rieul_mieum_near
        elif jaso == 'ㄼ': return self.rieul_bieup_near
        elif jaso == 'ㄾ': return self.rieul_tieut_near
        elif jaso == 'ㅀ': return self.rieul_hieut_near
        elif jaso == 'ㅄ': return self.bieup_siot_near
        
        elif jaso == 'ㅒ': return self.yae_near
        elif jaso == 'ㅖ': return self.ye_near
        elif jaso == 'ㅚ': return self.oe_near
        elif jaso == 'ㅟ': return self.wi_near
        elif jaso == 'ㅢ': return self.ui_near
        elif jaso == 'ㅘ': return self.wa_near
        elif jaso == 'ㅝ': return self.wo_near
        elif jaso == 'ㅙ': return self.wae_near
        elif jaso == 'ㅞ': return self.we_near
        
        else: raise Exception(f'{jaso}는 유효한 한국어 자소가 아닙니다.')
        

    # 자소 자체를 바꾸는 경우 
    def change_near_jaso(self, jaso):
        assert character_is_korean(jaso), '입력이 한국어 자소가 아닙니다.'
        assert ' ' in decompose(jaso), '입력이 한국어 자소가 아닌 단일 글자 형태입니다.'
        
        # selected_idx: 한 글자 안에서 바뀌게 될 자소 위치
        nearest = self.match_near_jaso(jaso)
        selected_idx = randrange(0, len(nearest))
        return nearest[selected_idx]
    
    
    # 한 단어에서 오타낼 글자 위치 선정
    def select_char_idx(self, word, strength='default'):
        # selected_idx: 한 단어 안에서 오타낼 글자 위치
        # strength에 따라 한 단어에서 오타를 얼마나 낼 것인지 결정
        selected_idx = []

        # 'default': 단어 길이 상관없이 오타 한번
        if strength == 'default':
            selected_idx.append(randrange(0, len(word)))

        # 'normal': 4글자 이하 단어 오타 한번, 5글자 이상 단어 오타 두번
        elif strength == 'normal':
            if len(word) <= 4:
                selected_idx.append(randrange(0, len(word)))
            else:
                selected_idx.append(randrange(0, len(word)))
                while True:
                    temp = randrange(0, len(word))
                    if temp not in selected_idx:
                        selected_idx.append(temp)
                        break

        # 'strong': 단어 길이 상관없이 오타 두번
        elif strength == 'strong':
            selected_idx.append(randrange(0, len(word)))
            while True:
                temp = randrange(0, len(word))
                if temp not in selected_idx:
                    selected_idx.append(temp)
                    break
        return selected_idx
    
    
    # 자소 순서를 바꾸는 경우
    def change_locate_jaso(self, word):
        first_jasos  = list(decompose(word[0]))
        second_jasos = list(decompose(word[1]))

        # 첫번째 글자: 초성+중성, 두번째 글자: 초성+중성+종성인 경우
        if ' ' in first_jasos and ' ' not in second_jasos:
            first_jasos[2]  = second_jasos[0]
            second_jasos[0] = second_jasos[2]
            second_jasos[2] = ' '

            first_char  = compose(first_jasos[0], first_jasos[1], first_jasos[2])
            second_char = compose(second_jasos[0], second_jasos[1], second_jasos[2])
            word = word.replace(word[:2], first_char+second_char)
            return word

        # 첫번째 글자: 초성+중성+종성, 두번째 글자: 초성+중성인 경우
        elif ' ' not in first_jasos and ' ' in second_jasos:
            second_jasos[0] = first_jasos[2]
            first_jasos[2]  = ' '

            first_char  = compose(first_jasos[0], first_jasos[1], first_jasos[2])
            second_char = compose(second_jasos[0], second_jasos[1], second_jasos[2])
            word = word.replace(word[:2], first_char+second_char)
            return word
    
        # 두 글자 다 초성+중성이거나 초성+중성+종성인 경우 순서 바뀌는 경우 없음
        else: return word  
    
    
    # 입력된 단어에서 오타 만들어냄
    def make_typo_in_word(self, word, strength='default'):
        # 자소 순서를 바꿀지, 자소 자체를 바꿀지 50%의 확률로 결정
        # 자소 순서를 바꾸는 경우, 바로 리턴
        # 자소 자체를 바꾸는 경우, 아래대로 진행 후 리턴
        if randrange(2) == 0:
            new_word = self.change_locate_jaso(word)
            if new_word != word: return new_word
        else: pass
            
        # 입력된 단어에서 오타낼 글자 위치 반환
        selected_idx = self.select_char_idx(word, strength)
        
        new_word = ''
        for idx in range(len(word)):
            # 해당 글자에 오타를 내야 하는 경우
            if idx in selected_idx:
                decomposed = list(decompose(word[idx]))
                
                # 해당 글자가 초성+중성만으로 이루어진 경우, 중성에서 오타를 냄
                if ' ' in decomposed:
                    new_jaso = self.change_near_jaso(decomposed[1])
                    decomposed[1] = new_jaso
                    new_char = compose(decomposed[0], decomposed[1], decomposed[2])
                    new_word += new_char
                    
                # 해당 글자가 초성+중성+종성으로 이루어진 경우, 중성 혹은 종성에서 오타를 냄
                else:
                    change_idx = randrange(1, 3)
                    new_jaso = self.change_near_jaso(decomposed[change_idx])
                    decomposed[change_idx] = new_jaso
                    new_char = compose(decomposed[0], decomposed[1], decomposed[2])
                    new_word += new_char
                
            # 해당 글자에 오타를 내지 않는 경우
            else: new_word += word[idx]
        return new_word