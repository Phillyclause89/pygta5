from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
from models import inception_v3 as googlenet
from getkeys import key_check
# from collections import deque, Counter
# import random
# from statistics import mode, mean
import numpy as np
# import os

GAME_WIDTH = 1920
GAME_HEIGHT = 1080

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 1

w = [1, 0, 0, 0, 0, 0, 0, 0, 0]
s = [0, 1, 0, 0, 0, 0, 0, 0, 0]
a = [0, 0, 1, 0, 0, 0, 0, 0, 0]
d = [0, 0, 0, 1, 0, 0, 0, 0, 0]
wa = [0, 0, 0, 0, 1, 0, 0, 0, 0]
wd = [0, 0, 0, 0, 0, 1, 0, 0, 0]
sa = [0, 0, 0, 0, 0, 0, 1, 0, 0]
sd = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nk = [0, 0, 0, 0, 0, 0, 0, 0, 1]


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output


def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)


def left():
    ReleaseKey(W)
    PressKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
    # ReleaseKey(S)


def right():
    ReleaseKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)


def reverse():
    PressKey(S)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def forward_left():
    PressKey(W)
    PressKey(A)
    ReleaseKey(D)
    ReleaseKey(S)


def forward_right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)


def reverse_left():
    PressKey(S)
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def reverse_right():
    PressKey(S)
    PressKey(D)
    ReleaseKey(W)
    ReleaseKey(A)


def no_keys():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)


model = googlenet((WIDTH * 2), HEIGHT, 3, LR, output=9)
MODEL_NAME = 'models\pygta5-{}-{}-{}-epochs-1-hist_data.model'.format(LR, 'googlenet', EPOCHS)
model.load(MODEL_NAME)

print('We have loaded a previous model!!!!')


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    mode_choice = 0
    test_data = []
    test_data_2 = []
    test_data_3 = []

    while (True):


        if not paused:

            if len(test_data) == 0:
                screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
                screen = cv2.resize(screen, (WIDTH, HEIGHT))
                keys = key_check()
                output = keys_to_output(keys)
                test_data = [screen, output]
            elif len(test_data_2) == 0:
                screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
                screen = cv2.resize(screen, (WIDTH, HEIGHT))
                keys = key_check()
                output = keys_to_output(keys)
                test_data_2 = test_data
                test_data = [screen, output]
            elif len(test_data_3) == 0:
                screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
                screen = cv2.resize(screen, (WIDTH, HEIGHT))
                keys = key_check()
                output = keys_to_output(keys)
                test_data_3 = test_data_2
                test_data_2 = test_data
                test_data = [screen, output]
            else:
                screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
                screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
                screen = cv2.resize(screen, (WIDTH, HEIGHT))

                img1 = screen
                img2 = test_data[0]
                img3 = test_data_2[0]
                img4 = test_data_3[0]
                last_input = test_data[1]
                _2nd_last_input = test_data_2[1]
                _3rd_last_input = test_data_3[1]

                font = cv2.FONT_HERSHEY_SIMPLEX
                last = []
                if last_input == [1, 0, 0, 0, 0, 0, 0, 0, 0]:
                    last = 'W'
                elif last_input == [0, 1, 0, 0, 0, 0, 0, 0, 0]:
                    last = 'SS'
                elif last_input == [0, 0, 1, 0, 0, 0, 0, 0, 0]:
                    last = 'AAA'
                elif last_input == [0, 0, 0, 1, 0, 0, 0, 0, 0]:
                    last = 'DDDD'
                elif last_input == [0, 0, 0, 0, 1, 0, 0, 0, 0]:
                    last = 'WAWAWA'
                elif last_input == [0, 0, 0, 0, 0, 1, 0, 0, 0]:
                    last = 'WDWDWDWD'
                elif last_input == [0, 0, 0, 0, 0, 0, 1, 0, 0]:
                    last = 'SASASASASA'
                elif last_input == [0, 0, 0, 0, 0, 0, 0, 1, 0]:
                    last = 'SDSDSDSDSDSD'
                elif last_input == [0, 0, 0, 0, 0, 0, 0, 0, 1]:
                    last = 'NKNKNKNKNKNKNK'
                cv2.putText(img2, str(last), (10, 10), font, 1, (0, 0, 255), 3, cv2.LINE_AA)

                if _2nd_last_input == [1, 0, 0, 0, 0, 0, 0, 0, 0]:
                    last = 'W'
                elif _2nd_last_input == [0, 1, 0, 0, 0, 0, 0, 0, 0]:
                    last = 'SS'
                elif _2nd_last_input == [0, 0, 1, 0, 0, 0, 0, 0, 0]:
                    last = 'AAA'
                elif _2nd_last_input == [0, 0, 0, 1, 0, 0, 0, 0, 0]:
                    last = 'DDDD'
                elif _2nd_last_input == [0, 0, 0, 0, 1, 0, 0, 0, 0]:
                    last = 'WAWAWA'
                elif _2nd_last_input == [0, 0, 0, 0, 0, 1, 0, 0, 0]:
                    last = 'WDWDWDWD'
                elif _2nd_last_input == [0, 0, 0, 0, 0, 0, 1, 0, 0]:
                    last = 'SASASASASA'
                elif _2nd_last_input == [0, 0, 0, 0, 0, 0, 0, 1, 0]:
                    last = 'SDSDSDSDSDSD'
                elif _2nd_last_input == [0, 0, 0, 0, 0, 0, 0, 0, 1]:
                    last = 'NKNKNKNKNKNKNK'
                cv2.putText(img3, str(last), (10, 10), font, 1, (0, 0, 255), 3, cv2.LINE_AA)

                if _3rd_last_input == [1, 0, 0, 0, 0, 0, 0, 0, 0]:
                    last = 'W'
                elif _3rd_last_input == [0, 1, 0, 0, 0, 0, 0, 0, 0]:
                    last = 'SS'
                elif _3rd_last_input == [0, 0, 1, 0, 0, 0, 0, 0, 0]:
                    last = 'AAA'
                elif _3rd_last_input == [0, 0, 0, 1, 0, 0, 0, 0, 0]:
                    last = 'DDDD'
                elif _3rd_last_input == [0, 0, 0, 0, 1, 0, 0, 0, 0]:
                    last = 'WAWAWA'
                elif _3rd_last_input == [0, 0, 0, 0, 0, 1, 0, 0, 0]:
                    last = 'WDWDWDWD'
                elif _3rd_last_input == [0, 0, 0, 0, 0, 0, 1, 0, 0]:
                    last = 'SASASASASA'
                elif _3rd_last_input == [0, 0, 0, 0, 0, 0, 0, 1, 0]:
                    last = 'SDSDSDSDSDSD'
                elif _3rd_last_input == [0, 0, 0, 0, 0, 0, 0, 0, 1]:
                    last = 'NKNKNKNKNKNKNK'
                cv2.putText(img4, str(last), (10, 10), font, 1, (0, 0, 255), 3, cv2.LINE_AA)

                vis0 = np.concatenate((img1, img2), axis=1)
                vis1 = np.concatenate((img3, img4), axis=1)
                final_vis = np.concatenate((vis0, vis1), axis=0)
                final_vis = cv2.resize(final_vis, (480, 270))

                prediction = model.predict([final_vis.reshape(WIDTH, HEIGHT, 3)])[0]
                prediction = np.array(prediction)  # * np.array([1.12, 1, 1, 1, 1, 1, 1, 1, 0.2])
                print(prediction)
                # div = 4
                # wplus = prediction[0] + (prediction[4] / div) + (prediction[5] / div)
                # print(wplus)
                # splus = prediction[1] + (prediction[6] / div) + (prediction[7] / div)
                # print(splus)
                # aplus = prediction[2] + (prediction[6] / div) + (prediction[4] / div)
                # print(aplus)
                # dplus = prediction[3] + (prediction[5] / div) + (prediction[7] / div)
                # print(dplus)
                # waplus = prediction[4] + (prediction[0] / div) + (prediction[2] / div)
                # print(waplus)
                # wdplus = prediction[5] + (prediction[0] / div) + (prediction[3] / div)
                # print(wdplus)
                # saplus = prediction[6] + (prediction[2] / div) + (prediction[1] / div)
                # print(saplus)
                # sdplus = prediction[7] + (prediction[1] / div) + (prediction[3] / div)
                # print(sdplus)
                #
                # mode_choice_v2 = np.argmax([wplus, splus, aplus, dplus, waplus, wdplus, saplus, sdplus])
                # print(mode_choice_v2)

                mode_choice = np.argmax(prediction)
                print(mode_choice)

                if mode_choice == 0:
                    straight()
                    choice_picked = 'straight'
                    print(choice_picked)

                elif mode_choice == 1:
                    reverse()
                    choice_picked = 'reverse'
                    print(choice_picked)

                elif mode_choice == 2:
                    left()
                    choice_picked = 'left'
                    print(choice_picked)

                elif mode_choice == 3:
                    right()
                    choice_picked = 'right'
                    print(choice_picked)

                elif mode_choice == 4:
                    forward_left()
                    choice_picked = 'forward+left'
                    print(choice_picked)

                elif mode_choice == 5:
                    forward_right()
                    choice_picked = 'forward+right'
                    print(choice_picked)

                elif mode_choice == 6:
                    reverse_left()
                    choice_picked = 'reverse+left'
                    print(choice_picked)

                elif mode_choice == 7:
                    reverse_right()
                    choice_picked = 'reverse+right'
                    print(choice_picked)

                elif mode_choice == 8:
                    no_keys()
                    choice_picked = 'nokeys'
                    print(choice_picked)
                keys = key_check()
                output = keys_to_output(keys)
                test_data_3 = test_data_2
                test_data_2 = test_data
                test_data = [screen, output]
        keys = key_check()

        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
                print("Unpaused")
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)
                print("Paused")


main()
