import imp
from itertools import combinations
from math import log2

from tqdm import tqdm
class Wordle:
    def __init__(self, file_name :str):
        self.remaining_words = list()
        i = 0
        for line in open("allowed_words.txt",'r'):
            self.remaining_words.append(line.rstrip('\n'))
            i += 1
        self.len_remaining = i
        self.correct_word = "creep"
    
    def information_get_using(self,word):
        cases = ['GRAY','YELLOW',"GREEN"]
        info_in_bits = 0
        for case_1 in cases:
            for case_2 in cases:
                for case_3 in cases:
                    for case_4 in cases:
                        for case_5 in cases:
                            combination = [case_1,case_2,case_3,case_4,case_5]
                            p = len(self.possible_words(word,combination))/self.len_remaining
                            info_in_bits -= p*self.__log2(p)
        return info_in_bits

    def possible_words(self,word,combination):
        remaining_words = self.remaining_words.copy()
        count = 0
        for case in combination:
            if case == "GREEN":
                remaining_words = self.__match_green(word[count],count,remaining_words)
            elif case == "YELLOW":
                remaining_words = self.__match_yellow(word[count],count,remaining_words)
            else:
                remaining_words = self.__match_gray(word[count],remaining_words)
            count += 1
        return remaining_words

    def __match_green(self,character,position,remaining_words):
        result = list()
        for word in remaining_words :
            if word[position] == character :
                result.append(word)
        return result

    def __match_yellow(self,character,position,remaining_words):
        result = list()
        for word in remaining_words :
            if (character in word ) and (word[position] != character):
                result.append(word)
        return result

    def __match_gray(self,character,remaining_words):
        result = list()
        for word in remaining_words:
            if character not in word :
                result.append(word)
        return result
    def __log2(self,x):
        return log2(x) if x>0 else 0
    
    def best_word(self):
        MAX = 0
        best_word = ''
        for word in self.remaining_words:
            if self.information_get_using(word) > MAX :
                best_word = word
                MAX = self.information_get_using(best_word)
        return best_word
    def set_remaining_words(self,remaining_words):
        self.remaining_words = remaining_words
        self.len_remaining = len(remaining_words)
    def solve(self):
        print('insert','tares')
        word = 'tares'
        while(self.len_remaining != 1):
            combination = input().split()
            self.set_remaining_words(self.possible_words(word,combination))
            word = self.best_word()
            print(word)
    def game(self,gess_word):
        combination = list()
        for i in range(5):
            if gess_word[i] not in self.correct_word :
                combination.append('GRAY')
            elif gess_word[i] == self.correct_word[i]:
                combination.append('GREEN')
            else:
                combination.append('YELLOW')
        return combination
    
    def score(self):
        word = 'tares'
        count = 0
        while(self.len_remaining != 1):
            combination = self.game(word)
            self.set_remaining_words(self.possible_words(word,combination))
            word = self.best_word()
            count += 1
        return count
            
def main():
    som = 0
    allowed_words =list()
    for line in open("allowed_words.txt",'r'):
        allowed_words.append(line.rstrip('\n'))
    for word in tqdm(allowed_words[:100]):
        wordle = Wordle("allowed_words.txt")
        wordle.correct_word = word
        score = wordle.score()
        print(word,"---->",score)
        som += score
    print("your score is:",som/len(allowed_words[:100]))

    


if __name__ == "__main__":
    main()

