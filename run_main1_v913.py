import sys
import Module_readMode_v913 as Mod_R
import Module_gameMode_v913 as Mod_G

import RPi.GPIO as GPIO  # 확인 버튼 활성화
import time
from subprocess import call

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(23 ,GPIO.OUT)  #진동

from time import sleep

value = True

#import subprocess
#subprocess.call(['putty -load dot &'], shell = True)

class SYMBOL_find:  #___읽기모드/게임모드 구분하기 위한 클래스 만들기___ 

    def __init__(self, symbol):
        self.first = symbol

    def find_index(self):  # 인덱스를 만든다

        index_list = list()
        index = -1
        while True:
            
            index = input_text.find(self.first, index + 1)  # index+1 이후에 나오는 첫번째 해당기호 인덱스를 내보낸다
            if index == -1:  # 더 이상 기호가 없으면
                index_list.reverse()  # 앞뒤 반전해서 
                break

            index_list.append(index)

        return index_list  # 기호가 들어있는 인덱스값 반전해서 변환



a = SYMBOL_find('#')  # 객체 정하기
b = SYMBOL_find('!')

Mod_R.all_off()


print("ready")

while True:  #___실행___

     if GPIO.input(21) == False:
          start_main = time.time()
          sleep(0.1)
     
          while True:
               if GPIO.input(21) == True:
                    end_main = time.time()
                    if (end_main-start_main) >= 7:
                         call(["shutdown", "-h", "now"], shell=False)
                         break
                    else:
                         value = False
                         break

        
     if value == False:
          value = True
          print("눌렀어요")

          GPIO.output(23, True)

          sleep(0.1)

          GPIO.output(23, False)


          input_file = open(sys.argv[1], 'r')  #___txt 파일 받아오기___

          for line in input_file.readlines():
               input_text = line

 
          symbol1 = a.find_index()  # 인덱스 리스트 역순
          symbol2 = b.find_index()

          result = list()

          if not symbol1 and not symbol2:  # 어떠한 기호도 없을때
               print('아직 입력되지 않았습니다.')

          elif symbol1 and not symbol2:  # '#'만 있을때

               for i in range(symbol1[1] + 1, symbol1[0]):
                         result.append(input_text[i])

               result = str.join('',result)
               Mod_R.text(result)
               #print(result_R)


          elif not symbol1 and symbol2:  # 'i'만 있을때

               for i in range(symbol2[1] + 1, symbol2[0]):
                         result.append(input_text[i])

               result = str.join('',result)
               Mod_G.text(result)

               #print(result_G)

          else:

               if symbol1[0] > symbol2[0]:  # 둘 다 있을때

                    for i in range(symbol1[1] + 1, symbol1[0]):
                         result.append(input_text[i])

                    result = str.join('',result)
                    Mod_R.text(result)

                    #print(result_R)

               else:

                    for i in range(symbol2[1] + 1, symbol2[0]):
                         result.append(input_text[i])

               result = str.join('',result)
               Mod_G.text(result)
               #print(result_G)  
          #sleep(0.2)
     sleep(0.1)



