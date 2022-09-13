import os
import json
import pandas as pd
import codecs
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

with open("anime-offline-database.json", encoding="utf-8") as f:
    data=json.load(f)

genre=0
df=pd.DataFrame(data["data"])
genreset=set()

for index,row in df.iterrows():
    for item in row["tags"]:
        genreset.add(item)
genrelist=sorted(list(genreset))

#auxiliary functions
def check_in_list(string,list):
    for item in list:
        if item==string:
            return True
    return False

def set_things_to_zero( list):
    if genre2 not in list:
        return "0NNNN"
    else:
        return list

def mydiv (i,j):
    if j == 0:
        return 0
    else:
        return i/j

#smoothing functions
def eventual_smoothing_soft(list1):
    for i in range (len(list1)-1):
        list2=list1
        if i==0 or i == len(list1)-1:    
            if i==0:
                list2[i]=(list1[i]+list1[i+1])/2
            if i == len(list1):
                list2[i]=(list1[i]+list1[i-1])/2
        else:
                list2[i]=(list1[i-1]+list1[i]+list1[i+1])/3
    return list2

def eventual_smoothing_hard (list1):
    list2=list1
    for i in range (len(list1)-1):
        try: 
            list2[i]=(list1[i-3]+list1[i-2]+list1[i-1]+list1[i]+list1[i+1]+list1[i+2]+list1[i+3])/7
        except:
            continue
    return list2



#main functions
def printgraph_of_genre_with_reference(genre,smoothing,newcs_relative):
    global genre2
    genre2=genre
    if newcs_relative==2:
        myframe=df
    else:
        myframe=df.copy()
    myframe["tags"]=myframe["tags"].apply(set_things_to_zero)
    myframe=myframe[myframe["tags"]!="0NNNN"]
    k=myframe["animeSeason"]
    yearlist=list(range(1945,2021))
    scorelist=[0]*(len(yearlist))
    for item in k:
        if item["year"]==None or item["year"] >2020 or item["year"]<1945:
            print(item)
        else:
            scorelist[yearlist.index(item["year"])]=scorelist[yearlist.index(item["year"])]+1
    k=df["animeSeason"]
    yearlist2=list(range(1945,2021))
    scorelist2=[0]*(len(yearlist))
    for item in k:
        if item["year"]==None or item["year"] >2020 or item["year"]<1945:
            print(item)
        else:
            scorelist2[yearlist2.index(item["year"])]=scorelist2[yearlist2.index(item["year"])]+1
    if smoothing=="soft":
        scorelist=eventual_smoothing_soft(scorelist)
    if smoothing=="hard":
        scorelist=eventual_smoothing_hard(scorelist)
    if newcs_relative==0:
        plt.figure()
    plt.plot(yearlist,scorelist,label=genre)
    plt.plot(yearlist2,scorelist2,"r--",label="anime releases in general")
    plt.legend()
    plt.show()

def printgraph_of_genre(genre,smoothing,newcs_relative):
    global genre2
    genre2=genre
    if newcs_relative==2:
        myframe=df
    else:
        myframe=df.copy()
    myframe["tags"]=myframe["tags"].apply(set_things_to_zero)
    myframe=myframe[myframe["tags"]!="0NNNN"]
    k=myframe["animeSeason"]
    yearlist=list(range(1900,2021))
    scorelist=[0]*(len(yearlist))
    for item in k:
        if item["year"]==None or item["year"] >2020:
            print(item)
        else:
            scorelist[yearlist.index(item["year"])]=scorelist[yearlist.index(item["year"])]+1
    if smoothing=="soft":
        scorelist=eventual_smoothing_soft(scorelist)
    if smoothing=="hard":
        scorelist=eventual_smoothing_hard(scorelist)
    if newcs_relative==0:
        plt.figure()
    plt.plot(yearlist,scorelist,label=genre)
    plt.legend()
    plt.show()

def printgraph_of_genre_proportional(genre, smoothing,newcs_relative):
    global genre2
    genre2=genre
    if newcs_relative==2:
        myframe=df
    else:
        myframe=df.copy()
    myframe["tags"]=myframe["tags"].apply(set_things_to_zero)
    myframe=myframe[myframe["tags"]!="0NNNN"]
    k=myframe["animeSeason"]
    yearlist=list(range(1945,2021))
    scorelist=[0]*(len(yearlist))
    for item in k:
        if item["year"]==None or item["year"] >2020 or item["year"]<1945:
            print(item)
        else:
            scorelist[yearlist.index(item["year"])]=scorelist[yearlist.index(item["year"])]+1
    k=df["animeSeason"]
    yearlist2=list(range(1945,2021))
    scorelist2=[0]*(len(yearlist))
    for item in k:
        if item["year"]==None or item["year"] >2020 or item["year"]<1945:
            print(item)
        else:
            scorelist2[yearlist2.index(item["year"])]=scorelist2[yearlist2.index(item["year"])]+1
    res = [mydiv(i,j) for i, j in zip(scorelist, scorelist2)] 
    if smoothing=="soft":
        res=eventual_smoothing_soft(res)
    if smoothing=="hard":
        res=eventual_smoothing_hard(res)
    if newcs_relative==0:
        plt.figure()
    plt.plot(yearlist,res,label=genre)
    plt.legend()
    plt.show()



#I/O resp. GUI

def plotaction ():
    mylist=["None","soft","hard"]
    genre=comboeingabe.get()
    smoothingnumber=v.get()
    modenotvar=mode.get()
    smoothing=mylist[smoothingnumber]
    newcs_relative=w.get()
    if modenotvar==0:
        printgraph_of_genre_proportional(genre=genre,smoothing=smoothing,newcs_relative=newcs_relative)
    if modenotvar==1:
        printgraph_of_genre(genre=genre,smoothing=smoothing,newcs_relative=newcs_relative)
    if modenotvar==2:
        printgraph_of_genre_with_reference(genre=genre,smoothing=smoothing,newcs_relative=newcs_relative)





fenster=Tk()
fenster.title("Anime-plotting")
v=IntVar()
w=IntVar()
mode=IntVar()
smoothinglist=[("no smoothing",0,3,2),("low smoothing (3)",1,4,2),("hard smoothing (7)",2,5,2)]
modelist=[("proportional to general anime releases",0 ,2 ,1),("only the anime releases",1 ,2 ,2), ("anime releases with reference graph",2 ,2 ,3)]
labels=[("same coordinate system or new",1),("mode",2)]
for txt, x in labels:
    Label(fenster,text=txt).grid(column=0,row=x)


for name, value ,row, col in smoothinglist:
    Radiobutton(fenster,text=name,padx=50,variable=v, value=value).grid(row=row,column=col)

for name,value , row , col in modelist:
    Radiobutton(fenster,text=name,padx=20,variable=mode,value=value,indicatoron=0,width=30).grid(row=row,column=col)

seqoffbutton=Radiobutton(fenster,text="new coordinate system",padx=20,variable=w,value=0,indicatoron=0,width=30).grid(row=1,column=1)
seqonbutton=Radiobutton(fenster,text="in the same coordinate system",padx=20,variable=w,value=1,indicatoron=0,width=30).grid(row=1,column=2)
seqplusbutton=Radiobutton(fenster,text="relative to previous results",padx=20,variable=w,value=2,indicatoron=0,width=30).grid(row=1,column=3)   


plot_button=Button(fenster,text="plot",command=plotaction)
end_button=Button(fenster,text="beenden",command=fenster.quit)
eingabefeld = Entry(fenster, bd=5, width=40)
comboeingabe=ttk.Combobox(fenster,values=genrelist)
comboeingabe.grid(row=0,columnspan=5,column=0)



plot_button.grid(row=6,column=2)
end_button.grid(row=7,column=2)
#eingabefeld.grid(row=0,columnspan=5,column=0)


fenster.mainloop()
































# printgraph_of_genre_proportional("shounen","hard")
# print(type(df["animeSeason"][1]))   
# print(df.columns.values)




# def printgraph_of_genre_proportional_correlationmode(genre, smoothing):
#     global genre2
#     genre2=genre
#     myframe=df
#     myframe["tags"]=myframe["tags"].apply(set_things_to_zero)
#     myframe=myframe[myframe["tags"]!="0NNNN"]
#     k=myframe["animeSeason"]
#     yearlist=list(range(1945,2021))
#     scorelist=[0]*(len(yearlist))
#     for item in k:
#         if item["year"]==None or item["year"] >2020 or item["year"]<1945:
#             print(item)
#         else:
#             scorelist[yearlist.index(item["year"])]=scorelist[yearlist.index(item["year"])]+1
#     k=df["animeSeason"]
#     yearlist2=list(range(1945,2021))
#     scorelist2=[0]*(len(yearlist))
#     for item in k:
#         if item["year"]==None or item["year"] >2020 or item["year"]<1945:
#             print(item)
#         else:
#             scorelist2[yearlist2.index(item["year"])]=scorelist2[yearlist2.index(item["year"])]+1
#     res = [mydiv(i,j) for i, j in zip(scorelist, scorelist2)] 
#     if smoothing=="soft":
#         res=eventual_smoothing_soft(res)
#     if smoothing=="hard":
#         res=eventual_smoothing_hard(res)
#     plt.plot(yearlist,res,label=genre)
#     plt.legend()
#     plt.show()


