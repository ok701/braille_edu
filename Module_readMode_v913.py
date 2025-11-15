import RPi.GPIO as GPIO
import time
import shift_register as Mod_shft
from subprocess import call

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)


# GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback7)
# 인터럽트로 쓰고싶으면 활성화
GPIO.setup(23 ,GPIO.OUT)  #진동


import hgtk
import numpy as np
from numpy.lib.shape_base import vsplit
import re
from time import sleep

#import keyboard  #___ 실사용할떄는 주석처리 필요___

MATCH_H2B_CHO = {

    u'ㄱ': np.array([0,0,0,1,0,0]),
    u'ㄴ': np.array([1,0,0,1,0,0]),
    u'ㄷ': np.array([0,1,0,1,0,0]),
    u'ㄹ': np.array([0,0,0,0,1,0]),
    u'ㅁ': np.array([1,0,0,0,1,0]),
    u'ㅂ': np.array([0,0,0,1,1,0]),
    u'ㅅ': np.array([0,0,0,0,0,1]),
    u'ㅇ': np.array([1,1,0,1,1,0]),
    u'ㅈ': np.array([0,0,0,1,0,1]),
    u'ㅊ': np.array([0,0,0,0,1,1]),
    u'ㅋ': np.array([1,1,0,1,0,0]),
    u'ㅌ': np.array([1,1,0,0,1,0]),
    u'ㅍ': np.array([1,0,0,1,1,0]),
    u'ㅎ': np.array([0,1,0,1,1,0]),

    u'ㄲ': np.array([0,0,0,0,0,1,0,0,0,1,0,0]),
    u'ㄸ': np.array([0,0,0,0,0,1,0,1,0,1,0,0]),
    u'ㅃ': np.array([0,0,0,0,0,1,0,0,0,1,1,0]),
    u'ㅆ': np.array([0,0,0,0,0,1,0,0,0,0,0,1]),
    u'ㅉ': np.array([0,0,0,0,0,1,0,0,0,1,0,1]),
}


MATCH_H2B_JOONG = {

    u'ㅏ': np.array([1,1,0,0,0,1]),
    u'ㅑ': np.array([0,0,1,1,1,0]),
    u'ㅓ': np.array([0,1,1,1,0,0]),
    u'ㅕ': np.array([1,0,0,0,1,1]),
    u'ㅗ': np.array([1,0,1,0,0,1]),
    u'ㅛ': np.array([0,0,1,1,0,1]),
    u'ㅜ': np.array([1,0,1,1,0,0]),
    u'ㅠ': np.array([1,0,0,1,0,1]),
    u'ㅡ': np.array([0,1,0,1,0,1]),
    u'ㅣ': np.array([1,0,1,0,1,0]),
    u'ㅐ': np.array([1,1,1,0,1,0]),
    u'ㅔ': np.array([1,0,1,1,1,0]),
    u'ㅒ': np.array([0,0,1,1,1,0,1,1,1,0,1,0]),
    u'ㅖ': np.array([0,0,1,1,0,0]),
    u'ㅘ': np.array([1,1,1,0,0,1]),
    u'ㅙ': np.array([1,1,1,0,0,1,1,1,1,0,1,0]),
    u'ㅚ': np.array([1,0,1,1,1,1]),
    u'ㅝ': np.array([1,1,1,1,0,0]),
    u'ㅞ': np.array([1,1,1,1,0,0,1,1,1,0,1,0]),
    u'ㅟ': np.array([1,0,1,1,0,0,1,1,1,0,1,0]),
    u'ㅢ': np.array([0,1,0,1,1,1]),
}


MATCH_H2B_JONG = {

    u'ㄱ': np.array([1,0,0,0,0,0]),
    u'ㄴ': np.array([0,1,0,0,1,0]),
    u'ㄷ': np.array([0,0,1,0,1,0]),
    u'ㄹ': np.array([0,1,0,0,0,0]),
    u'ㅁ': np.array([0,1,0,0,0,1]),
    u'ㅂ': np.array([1,1,0,0,0,0]),
    u'ㅅ': np.array([0,0,1,0,0,0]),
    u'ㅇ': np.array([0,1,1,0,1,1]),
    u'ㅈ': np.array([1,0,1,0,0,0]),
    u'ㅊ': np.array([0,1,1,0,0,0]),
    u'ㅋ': np.array([0,1,1,0,1,0]),
    u'ㅌ': np.array([0,1,1,0,0,1]),
    u'ㅍ': np.array([0,1,0,0,1,1]),
    u'ㅎ': np.array([0,0,1,0,1,1]),

    u'ㄲ': np.array([1,0,0,0,0,0,1,0,0,0,0,0]),
    u'ㄳ': np.array([1,0,0,0,0,0,0,0,1,0,0,0]),
    u'ㄵ': np.array([0,1,0,0,1,0,1,0,1,0,0,0]),
    u'ㄶ': np.array([0,1,0,0,1,0,0,0,1,0,1,1]),
    u'ㄺ': np.array([0,1,0,0,0,0,1,0,0,0,0,0]),
    u'ㄻ': np.array([0,1,0,0,0,0,0,1,0,0,0,1]),
    u'ㄼ': np.array([0,1,0,0,0,0,1,1,0,0,0,0]),
    u'ㄽ': np.array([0,1,0,0,0,0,0,0,1,0,0,0]),
    u'ㄾ': np.array([0,1,0,0,0,0,0,1,1,0,0,1]),
    u'ㄿ': np.array([0,1,0,0,0,0,0,1,0,0,1,1]),
    u'ㅀ': np.array([0,1,0,0,0,0,0,0,1,0,1,1]),
    u'ㅄ': np.array([1,1,0,0,0,0,0,0,1,0,0,0]),
    u'ㅆ': np.array([0,0,1,1,0,0]),
}



MATCH_H2B_ALPHABET = {

    'a': np.array([1,0,0,0,0,0]),
    'b': np.array([1,1,0,0,0,0]),
    'c': np.array([1,0,0,1,0,0]),
    'd': np.array([1,0,0,1,1,0]),
    'e': np.array([1,0,0,0,1,0]),
    'f': np.array([1,1,0,1,0,0]),
    'g': np.array([1,1,0,1,1,0]),
    'h': np.array([1,1,0,0,1,0]),
    'i': np.array([0,1,0,1,0,0]),
    'j': np.array([0,1,0,1,1,0]),
    'k': np.array([1,0,1,0,0,0]),
    'l': np.array([1,1,1,0,0,0]),
    'm': np.array([1,0,1,1,0,0]),
    'n': np.array([1,0,1,1,1,0]),
    'o': np.array([1,0,1,0,1,0]),
    'p': np.array([1,1,1,1,0,0]),
    'q': np.array([1,1,1,1,1,0]),
    'r': np.array([1,1,1,0,1,0]),
    's': np.array([0,1,1,1,0,0]),
    't': np.array([0,1,1,1,1,0]),
    'u': np.array([1,0,1,0,0,1]),
    'v': np.array([1,1,1,0,0,1]),
    'w': np.array([0,1,1,1,1,1]),
    'x': np.array([1,0,1,1,0,1]),
    'y': np.array([1,0,1,1,1,1]),
    'z': np.array([1,0,1,0,1,1]),

    'A': np.array([0,0,0,0,0,1,1,0,0,0,0,0]),
    'B': np.array([0,0,0,0,0,1,1,1,0,0,0,0]),
    'C': np.array([0,0,0,0,0,1,1,0,0,1,0,0]),
    'D': np.array([0,0,0,0,0,1,1,0,0,1,1,0]),
    'E': np.array([0,0,0,0,0,1,1,0,0,0,1,0]),
    'F': np.array([0,0,0,0,0,1,1,1,0,1,0,0]),
    'G': np.array([0,0,0,0,0,1,1,1,0,1,1,0]),
    'H': np.array([0,0,0,0,0,1,1,1,0,0,1,0]),
    'I': np.array([0,0,0,0,0,1,0,1,0,1,0,0]),
    'J': np.array([0,0,0,0,0,1,0,1,0,1,1,0]),
    'K': np.array([0,0,0,0,0,1,1,0,1,0,0,0]),
    'L': np.array([0,0,0,0,0,1,1,1,1,0,0,0]),
    'M': np.array([0,0,0,0,0,1,1,0,1,1,0,0]),
    'N': np.array([0,0,0,0,0,1,1,0,1,1,1,0]),
    'O': np.array([0,0,0,0,0,1,1,0,1,0,1,0]),
    'P': np.array([0,0,0,0,0,1,1,1,1,1,0,0]),
    'Q': np.array([0,0,0,0,0,1,1,1,1,1,1,0]),
    'R': np.array([0,0,0,0,0,1,1,1,1,0,1,0]),
    'S': np.array([0,0,0,0,0,1,0,1,1,1,0,0]),
    'T': np.array([0,0,0,0,0,1,0,1,1,1,1,0]),
    'U': np.array([0,0,0,0,0,1,1,0,1,0,0,1]),
    'V': np.array([0,0,0,0,0,1,1,1,1,0,0,1]),
    'W': np.array([0,0,0,0,0,1,0,1,1,1,1,1]),
    'X': np.array([0,0,0,0,0,1,1,0,1,1,0,1]),
    'Y': np.array([0,0,0,0,0,1,1,0,1,1,1,1]),
    'Z': np.array([0,0,0,0,0,1,1,0,1,0,1,1]),

    '1': np.array([0,0,1,1,1,1,1,0,0,0,0,0]),
    '2': np.array([0,0,1,1,1,1,1,1,0,0,0,0]),
    '3': np.array([0,0,1,1,1,1,1,0,0,1,0,0]),
    '4': np.array([0,0,1,1,1,1,1,0,0,1,1,0]),
    '5': np.array([0,0,1,1,1,1,1,0,0,0,1,0]),
    '6': np.array([0,0,1,1,1,1,1,1,0,1,0,0]),
    '7': np.array([0,0,1,1,1,1,1,1,0,1,1,0]),
    '8': np.array([0,0,1,1,1,1,1,1,0,0,1,0]),
    '9': np.array([0,0,1,1,1,1,0,1,0,1,0,0]),
    '0': np.array([0,0,1,1,1,1,0,1,0,1,1,0]),

    ',': np.array([0,1,0,0,0,0]),
    '.': np.array([0,1,0,0,1,1]),
    '-': np.array([0,1,0,0,1,0]),
    '?': np.array([0,1,1,0,0,1]),
    '_': np.array([0,0,1,0,0,1]),
    '!': np.array([0,1,1,0,1,0]),
}


# 아래 3개는 '0'들의 배열로 용도는 아래에서 설명
zerotwo = np.zeros(2)
zerosix = np.zeros(6)
zerotwv = np.zeros(12)
zeroeigth = np.zeros(18)


def letter(hangul_letter):
   
    Notxt = np.array([])
    hangul_decomposed = hgtk.text.decompose(hangul_letter[0])
    hangul_decomposed = hangul_decomposed.replace(hgtk.text.DEFAULT_COMPOSE_CODE, '')

    index1 = 0
    index2 = 0
    index3 = 0 #종성은 없을수도 있기 때문에 초기값 설정해준다

    if len(Notxt) == 0:       #######################띄어쓰기##############################
        # 띄어쓰기의 경우에는 아무일 없도록
        Notxt = Notxt


    for i in range(len(hangul_decomposed)):

        hangul = hangul_decomposed[i]       

        if i == 0 and hangul in MATCH_H2B_CHO:         #######################초성##############################
            # print("초성ok")
            Notxt = np.hstack((Notxt,(MATCH_H2B_CHO[hangul])))
            index1 = len(MATCH_H2B_CHO[hangul])


        if i == 1 and hangul in MATCH_H2B_JOONG:       #######################중성##############################

            Notxt = np.hstack((Notxt,(MATCH_H2B_JOONG[hangul])))

            index2 = len(MATCH_H2B_JOONG[hangul])


        if i == 2 and hangul in MATCH_H2B_JONG:         #######################종성##############################

            Notxt = np.hstack((Notxt,(MATCH_H2B_JONG[hangul])))

            index3 = len(MATCH_H2B_JONG[hangul])

  
    # 4개의 셀에 표기를 해야하기 때문에 셀이 남는 글자인 경우에는 빈칸(0)으로 채워줘야 한다.
    # 아래에 표기된 zerosix,zerotwv,zeroeight는 '0'이 각각 6,12,18개씩 글자의 종류에 따라 다르게 배열 뒤에 붙도록 설정한것

    if (index1+index2+index3) == 12: #2개
        Notxt = np.hstack((Notxt,zerotwv))

    elif (index1+index2+index3) == 18: #3개
        Notxt = np.hstack((Notxt,zerosix))

    if index1==6 and index2==12 and index3==12: #122
        Notxt = np.insert(Notxt,index1+index2,zerosix)
        Notxt = np.hstack((Notxt,zerotwv))

    elif index1==12 and index2==6 and index3==12: #212
        Notxt = np.insert(Notxt,index1+index2,zerotwv)
        Notxt = np.hstack((Notxt,zerosix))

    elif index1==12 and index2==12 and index3==6: #221
        Notxt = np.hstack((Notxt,zeroeigth))

    elif index1==12 and index2==12 and index3==12: #222
        Notxt = np.hstack((Notxt,zerotwv))

    return Notxt



zerotwofour = np.zeros(24)

def all_off():  # 전부 끄기
    Mod_shft.send_byte(zerotwofour)


def text(hangul_sentence):

    index4 = 0
    index5 = 0

    result = np.array([])

    for hangul_letter in hangul_sentence:
        result = np.hstack((result,letter(hangul_letter)))

    row = int(len(result)/24)
    index5 = int(len(result)/6)
    index6 = int(len(result))
    print(index6)

    # testarr1=np.array([0,1,0,1,0,1,0,1])
    ledResult = result

    # kingarr = np.array([])
    ledResult = np.reshape(ledResult,(row,24)) #24갠데 32개로 수정해야된다.

    # 6개씩 나누고 각 행에 00 붙힌다.
    # for ray in range(index5):
    #     kingarr = np.hstack((kingarr, np.hstack((zerotwo,ledResult[ray]))))
    # print(kingarr)

    # kingarr = np.reshape(kingarr,(int(len(kingarr)/8),8))

    print(ledResult)
    print(row) 

    #___LED 출력하기___
    # row = len(result) # 총 행의 개수
    #i = 0 # led GPIO 순서
    a = 0 # 행 값
    init = True
    rax = 0
  

    while True:

        if init == True or GPIO.input(21) == False: # 스위치를 누르면 진행
            #if init == False:
            all_off()
            #수정 
            start = time.time()
            sleep(0.05)
            if a == row: # 모든 행 수행 했다면
                break
            while True:
                
                if GPIO.input(21) == True:
                    end = time.time()
       
                    if (end-start) >= 7:
                        call(["shutdown", "-h", "now"], shell=False)
                        break
                    else:
                        GPIO.output(23, True)
                        sleep(0.1)
                        GPIO.output(23, False)

                        #if a == row: # 모든 행 수행 했다면
                            #break

                        Mod_shft.send_byte(ledResult[a])
                        print(ledResult[a])

                        a = a + 1
                      
                        break
        
        init = False
        sleep(0.1)

    all_off()

    print('done')