import sys
import random
import time
from tkinter import *
from functools import partial
import datetime
import collections  


f = open("sentences.txt")
sentences_list = []
for line in f:
    sentence = line.split("\n")[:-1]
    sentences_list.append(sentence)   

def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    return _list

def clearAll(window):
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

def ready():
    clearAll(raam)
    
    Button(raam, text = "Back", font=("Verdana", 12), command = main_menu).place(x=10, y=10, width=115, height=40)

    Label(raam, text="This is a Typing Speed Test. To start the game enter your name and press \"Start\"", font=("Verdana", 15), justify = CENTER, padx = 1, wraplength=450).place(x=200, y=20, width=550)

    name = StringVar()
    Label(raam, text="Name:", font=("Verdana", 15), justify = CENTER, padx = 1, wraplength=400).place(x=120, y=250, width=250)
    ent3 = Entry(raam, textvariable=name, font=("Verdana", 12), width=20).place(x=300, y=250, width=300, height=40)
    random_sentence = random.choice(sentences_list)
    button = Button(raam, text = "Start", font=("Verdana", 16, "bold"), command = partial(play, name))
    button.place(x=350, y=330, width=200, height=50)
    #button.place(x=85, y=250, width=250, height=50)

def play(name):
    global sentences_list
    clearAll(raam)
    
    initial_time = time.time()
    username = name.get()
    
    random_sentence = random.choice(sentences_list)
    sentence = random_sentence[0]
    #print(sentence)
    
    
    Label(raam, text=sentence, font=("Verdana", 20), justify = CENTER, padx = 1,  wraplength=860).place(x=20, y=20, width=860)
    text = StringVar()
    
    ent= Entry(raam, textvariable=text, font=("Verdana", 20), width=20).place(x=20, y=340, width=860, height=40)
    raam.bind('<Return>', (lambda event: result(text, sentence, initial_time, username)))
    

def result(text, sentence, initial_time, username):
    current_time = time.time()
    clearAll(raam)
    Button(raam, text = "Back", font=("Verdana", 12), command = main_menu).place(x=10, y=10, width=115, height=40)
    s = text.get()
    new_s = s.split(" ")
    #print("s: ",s)
    
    filter_object = filter(lambda x: x != "", new_s)
    s_without_empty_strings = list(filter_object)
    #print(s_without_empty_strings)
    
    new_sentence = sentence.split(" ")
    #print("new_sentence: ", new_sentence)

    time_taken = current_time - initial_time
    
    mistakes = len(new_sentence)-len(s_without_empty_strings)
    #print(len(new_sentence))
    for index in range(len(s)):
        try:
            if s_without_empty_strings[index]!=new_sentence[index]:
                mistakes+=1
        except:
            break
    
    
    words = len(new_sentence)
    wpm = round(words/time_taken*60, 2)
    if mistakes>10:
        result_text = "Are you even trying? You have made mistakes in ", mistakes, "words."
        Label(raam, text=result_text, font=("Verdana", 16), justify = CENTER, padx = 1).place(x=20, y=70, width=860)
    else:
        score = wpm-mistakes
        result_text = "Your typing speed is " + str(wpm) + " words per minute,\n you have made mistake(s) in  " + str(mistakes) + " word(s).\nYour total score is " + str(score)
        Label(raam, text=result_text, font=("Verdana", 16), justify = CENTER, padx = 1).place(x=20, y=70, width=860)
        with open('highscore.txt') as f:
            scores=f.readlines()
        highscores = []
        for line in scores:
            highscore=line.strip().split(":")
            highscores.append(highscore)
        for i in range(len(highscores)):
            if score > float(highscores[i][1]):
                now = datetime.datetime.now().strftime("%B %d, %Y")
                highscores.insert(i, [username, str(score), now])
                break
        if len(highscores) == 11:
            highscores.pop(-1)
        with open('highscore.txt', 'w+') as f:
            write_text=''
            for i in highscores:
                write_text+= ":".join(i)+'\n'
            f.write(write_text)
            
def highscore():
    clearAll(raam)
    
    with open('highscore.txt') as f:
        scores=f.readlines()
    
    a=1
    for line in scores:
        score = line.strip().split(':')
        scoretext = str(a) + ". " + score[0] + "\tScore: " + score[1] + "\t" + score[2]
        Label(raam, text=scoretext, font=("Verdana", 14), justify = CENTER, padx = 1).place(x=10, y=50+30*a, width=880)
        a+=1
    
    Button(raam, text = "Back", font=("Verdana", 12), command = main_menu).place(x=10, y=10, width=115, height=40)
    
def main_menu():
    clearAll(raam)

    button = Button (raam, text = "Quit", font=("Verdana", 16, "bold"), command = raam.destroy)
    button.place(x=575, y=200, width=250, height=50)

    button = Button (raam, text = "Play", font=("Verdana", 16, "bold"), command = ready)
    button.place(x=85, y=200, width=250, height=50)

    button = Button (raam, text = "High Scores", font=("Verdana", 16, "bold"), command = highscore)
    button.place(x=325, y=200, width=250, height=50)
    
raam = Tk()
raam.title("project")
raam.geometry("900x400")
raam.resizable(False, False)

main_menu()

raam.mainloop()

    
