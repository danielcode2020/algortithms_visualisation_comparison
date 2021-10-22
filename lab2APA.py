# QuickSort
# alege un elemnet pivot
# imparte lista in 2 parti
# elem. stanga < pivot
# elem. dreapta > pivot
# pentru fiecare lista obtinuta alegem iarasi un element pivot si imparte lista
# ....
# pana cand ajungem la lista formata dintrun singur element sau din elemente cu aceeasi valoare

# MergeSort
# gaseste mijlocul
# imparte lista in 2 parti
# apeleaza mergesort pentru prima si a 2 jumate


import random
import time
from timeit import default_timer as timer
from datetime import timedelta
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(10000)

def show(array,c,w):
    c.delete("all")
    y1=200
    y2=200
    for i in range(0,len(array)):  
        y1+=4
        y2+=4
        c.create_line(y1,490,y2,490-array[i]*2)
        c.create_line(y1+1,490,y2+1,490-array[i]*2)
        
    w.after(25) # default 25 
    w.update_idletasks()
    

        
def init_array(array,size): # executa un shuffle pentru valorile din array
    array = []
    count = 0

    while count<size:
        n=random.randint(0,size)
        array.append(n)
        count+=1
    return array

####################################################################################
#functiile de baza pentru sortarea algoritmilor si compararea performantei lor

def partition(arr, low, high,count):
    i = (low-1)         # indexul elementului cu o pozitie mai mica decat pivot
    pivot = arr[high]     # elementul pivot
    for j in range(low, high):
        
        # verificam daca indexul elementului curent este mai mic sau egal cu pivot
        if arr[j] <= pivot:
            count+=1
            i = i+1  # incrementam indexul elementului mai mic
            arr[i], arr[j] = arr[j], arr[i]  # schimbam elementele cu locul
  
    arr[i+1], arr[high] = arr[high], arr[i+1] # elementul schimbat este pus in pozitia finala in array
    return (i+1),count
  

  
def quickSort(arr, low, high,count):
    if len(arr) == 1:
        return arr
    if low < high:
        #comp = inc(comp)
        #pi = este indexul pentru partition
        pi ,res= partition(arr, low, high,count)
        count+=res
        #sortam separat elementele pana si dupa partitie, iar pivotul ramane in mijloc
        quickSort(arr, low, pi-1,count)
        quickSort(arr, pi+1, high,count)
    return count

def mergeSort(arr,count):
    if len(arr) > 1:
        # Gasim mijlocul arrayului
        mid = len(arr)//2 # impartim la 2 lungimea arrayului cu tipul rezultatului int
  
        # Dividem arrayul la stanga de jumate
        L = arr[:mid] # returneaza o copie cu valori de la pozitia 0 pana la mijloc -1
  
        # in dreapta
        R = arr[mid:] #returneaza o copie cu valori de la pozitia mijloc + 1 pana la sfarsitul arrayului
        
        # Sortam prima jumatate 
        mergeSort(L,count)
        
        # Sortam a 2 jumatate
        mergeSort(R,count)
  
        i = j = k = 0
  
        # Copiem valorile din arrayurile temporare L si R in pozitia k al arrayului de baza
        # principiul de baza : valorile mai mici ca la mijlocul se vor afla in partea stanga, mai mari in partea dreapta
        
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                count+=1
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
  
        # Verificam daca vreun element nu a fost lasat sau necomparat
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
  
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return count


def InsSort(arr,start,end,count):
    count=0
    for i in range(start+1,end+1):
        elem = arr[i]
        j = i-1
        while j>=start and elem<arr[j]:
            if elem<arr[j]:
                count+=1
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = elem
    return arr,count

def merge(arr,start,mid,end,count):
    if mid==end:
        count=0
        return arr,count
    count=0
    first = arr[start:mid+1]
    last = arr[mid+1:end+1]
    len1 = mid-start+1
    len2 = end-mid
    ind1 = 0
    ind2 = 0
    ind  = start
     
    while ind1<len1 and ind2<len2:
        if first[ind1]<last[ind2]:
            count+=1
            arr[ind] = first[ind1]
            ind1 += 1
        else:
            arr[ind] = last[ind2]
            ind2 += 1
        ind += 1
     
    while ind1<len1:
        arr[ind] = first[ind1]
        ind1 += 1
        ind += 1
              
    while ind2<len2:
        arr[ind] = last[ind2]
        ind2 += 1
        ind += 1   

    return arr,count

minrun = 32 # se recomanda intre 32 si 64            
def TimSort(arr,count):
    n = len(arr)

    # in acest bloc de program algoritmul executa insertion sort pentru intervale ale arrayului  a cate 32 de elemente
    # iteratia 1 start == 0,end este valoarea cea mai mica dintre 31 si respectiv 99
    # iar primul interval de sortare este (0,31)
    # la iteratia 2, start == 32, end  == 63, intervalul (32,63)
    
    for start in range(0,n,minrun): # al 3 lea parametru minrun este pasul lui start
        end = min(start+minrun-1,n-1)
        arr ,res= InsSort(arr,start,end,count)
        count+=res
        
    curr_size = minrun
    
    # in acest bloc la fiecare iteratie valoare lui curr_size se mareste de 2 ori
    # pentru intervale a cate 32,64,126... algortimul executa mergeSort
    # iteratia 1, start ==0, mid == 31, end == 63, intervalul (0,63)
    # iteratia 2, start ==64, mid == 95, end == 
    while curr_size<n:
        
        for start in range(0,n,curr_size*2):
            mid = min(n-1,start+curr_size-1)
            end = min(n-1,mid+curr_size)
            arr ,result = merge(arr,start,mid,end,count)
            count+=result
        curr_size *= 2
    return count

###############################################################################
# functiile pentru implementarea sortarii pentru interfata grafica

def spartition(arr, low, high,c,w):
    i = (low-1)         
    pivot = arr[high]    
    show(arr,c,w);
    for j in range(low, high): 
        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)
def squickSort(arr, low, high,c,w):
    if len(arr) == 1:
        return arr
    if low < high:
        pi= spartition(arr, low, high,c,w)
        squickSort(arr, low, pi-1,c,w)
        squickSort(arr, pi+1, high,c,w)
def smergeSort(arr,c,w):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        smergeSort(L,c,w)
        smergeSort(R,c,w)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1 
        show(arr,c,w)
def sInsSort(arr,start,end):
    for i in range(start+1,end+1):
        elem = arr[i]
        j = i-1
        while j>=start and elem<arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = elem
    return arr

def smerge(arr,start,mid,end):
    if mid==end:
        return arr
    first = arr[start:mid+1]
    last = arr[mid+1:end+1]
    len1 = mid-start+1
    len2 = end-mid
    ind1 = 0
    ind2 = 0
    ind  = start
    while ind1<len1 and ind2<len2:
        if first[ind1]<last[ind2]:
            arr[ind] = first[ind1]
            ind1 += 1
        else:
            arr[ind] = last[ind2]
            ind2 += 1
        ind += 1
    while ind1<len1:
        arr[ind] = first[ind1]
        ind1 += 1
        ind += 1
              
    while ind2<len2:
        arr[ind] = last[ind2]
        ind2 += 1
        ind += 1   

    return arr

minrun = 32            
def sTimSort(arr,c,w):
    n = len(arr)
    
    for start in range(0,n,minrun):
        end = min(start+minrun-1,n-1)
        arr= sInsSort(arr,start,end)
        show(arr,c,w)
        
    curr_size = minrun
    while curr_size<n:
        for start in range(0,n,curr_size*2):
            show(arr,c,w)
            mid = min(n-1,start+curr_size-1)
            end = min(n-1,mid+curr_size)
            arr= smerge(arr,start,mid,end)
            #count+=result
        curr_size *= 2
    show(arr,c,w)
############################################################
# functiile pentru afisarea sortarilor
def implementQS(sh):
    arr=[]
    arr = init_array(arr,200)
    nw = tk.Toplevel(root)
    nw.title('QuickSort')
    our_canvas=Canvas(nw,width=1200,height=600,bg="white")
    our_canvas.pack()
    our_canvas.delete("all")
    squickSort(arr,0,len(arr)-1,our_canvas,nw)
    root.after(1000)
    nw.destroy()
    

def implementMS(sh):
    arr=[]
    arr = init_array(arr,200)
    nw = tk.Toplevel(root)
    nw.title('MergeSort')
    our_canvas=Canvas(nw,width=1200,height=600,bg="white")
    our_canvas.pack()
    our_canvas.delete("all")
    smergeSort(arr,our_canvas,nw)
    init_array(arr,len(arr)-1)
    root.after(1000)
    nw.destroy()

def implementTS(sh):
    arr=[]
    arr=init_array(arr,200)
    nw = tk.Toplevel(root)
    nw.title('TimSort')
    our_canvas=Canvas(nw,width=1200,height=600,bg="white")
    our_canvas.pack()
    our_canvas.delete("all")
    sTimSort(arr,our_canvas,nw)
    init_array(arr,len(arr)-1)
    root.after(1000)
    nw.destroy()

def Compare(c):
    timeQ=[]
    timeM=[]
    timeT=[]
    compQ=[]
    compM=[]
    compT=[]
    n=10
    while n<=10000:
        if c=="a":
            cq,cm,ct,tq,tm,tt = time_and_comp_average(n)
            compQ.append(cq)
            compM.append(cm)
            compT.append(ct)
            timeQ.append(tq)
            timeM.append(tm)
            timeT.append(tt)
        if c=="w":
            cq,cm,ct,tq,tm,tt = time_and_comp_worst(n)
            compQ.append(cq)
            compM.append(cm)
            compT.append(ct)
            timeQ.append(tq)
            timeM.append(tm)
            timeT.append(tt)
        if c=="b":
            cq,cm,ct,tq,tm,tt = time_and_comp_best(n)
            compQ.append(cq)
            compM.append(cm)
            compT.append(ct)
            timeQ.append(tq)
            timeM.append(tm)
            timeT.append(tt)
            
        n*=10
    
    print(timeQ)
    print(timeM)
    print(timeT)
    print(compQ)
    print(compM)
    print(compT)
    fig, axs = plt.subplots(2, 1, figsize=(10, 7))
    axs[0].plot(timeQ,label='Quick')
    axs[0].plot(timeM,label="Merge")
    axs[0].plot(timeT,label="Tim")
    axs[0].set_ylabel('miliseconds')
    axs[0].set_title("Time")
    axs[0].legend()
    axs[1].plot(compQ,label="Quick")
    axs[1].plot(compM,label="Merge")
    axs[1].plot(compT,label="Tim")
    axs[1].set_title("Comparisons")
    axs[1].legend()
    plt.show()
    


def time_and_comp_average(n):
    arr=[]
    arr=init_array(arr,n)
    start = timer()
    cq=0
    cq=quickSort(arr,0,len(arr)-1,cq)
    end  = timer()
    tq = timedelta(seconds = end-start).microseconds/1000

    arr=init_array(arr,n)
    start = timer()
    cm=0
    cm=mergeSort(arr,cm)
    end  = timer()
    tm = timedelta(seconds = end-start).microseconds/1000
    
    arr=init_array(arr,n)
    start = timer()
    ct=0
    ct=TimSort(arr,ct)
    end  = timer()
    tt = timedelta(seconds = end-start).microseconds/1000

    return cq,cm,ct,tq,tm,tt
    
def time_and_comp_worst(n):
    # pentru quick arrayul este deja sortat
    arr = []
    for i in range(0,n-1):
        if i==10:
            arr.append(100)
        else:
            arr.append(i)
    start = timer()
    cq=0
    cq=quickSort(arr,0,len(arr)-1,cq)
    end  = timer()
    tq=timedelta(seconds = end-start).microseconds/1000

    # pentru merge arrayul arata in felul urmator : [4,0,6,2,5,1,7,3]
    arr = []
    arr = init_array(arr,n)
    cm=0
    cm=mergeSort(arr,cm)
    end  = timer()
    tm=timedelta(seconds = end-start).microseconds/1000
    
    arr=[]
    for i in range(0,n):
        arr.append(n-i)
    start = timer()
    ct=0
    ct=TimSort(arr,ct)
    end  = timer()
    tt=timedelta(seconds = end-start).microseconds/1000
    return cq,cm,ct,tq,tm,tt
    
def time_and_comp_best(n):
    arr = []
    arr = init_array(arr,n)
    start = timer()
    cq=0
    cq=quickSort(arr,0,len(arr)-2,cq)
    end  = timer()
    tq=timedelta(seconds = end-start).microseconds/1000



    # pentru merge arrayul arata in felul urmator : [4,0,6,2,5,1,7,3]
    arr = []
    i=0
    while (i<=int(n/n)):
        arr.append(int(n/2)+2*i)
        arr.append(2*i)
        i+=1
    i=int(n/n)
    j=0
    while i<=int(n/4):
        arr.append(int(n/2)+2*j+1)
        arr.append(2*j+1)
        j+=1
        i+=1
    
    start = timer()
    cm=0
    cm=mergeSort(arr,cm)
    end  = timer()
    tm=timedelta(seconds = end-start).microseconds/1000
    arr = []
    i=0
    while (i<=int(n/n)):
        arr.append(int(n/2)+2*i)
        arr.append(2*i)
        i+=1
    i=int(n/n)
    j=0
    while i<=int(n/4)-1:
        arr.append(int(n/2)+2*j+1)
        arr.append(2*j+1)
        j+=1
        i+=1
    
    start = timer()
    ct=0
    ct=TimSort(arr,ct)
    end  = timer()
    tt=timedelta(seconds = end-start).microseconds/1000
    
    return cq,cm,ct,tq,tm,tt
    
    

arr = []
arr = init_array(arr,200)

root = Tk()             


root.geometry('170x300')
root.title('Menu')

btn = Button(root, text="QuickSort",command=lambda : implementQS(True))
btn.place(x=30,y=0)
btn1 = Button(root, text="MergeSort",command=lambda : implementMS(True))
btn1.place(x=30,y=50)
btn2 = Button(root, text="TimSort",command = lambda : implementTS(True))
btn2.place(x=30,y=100)
btn3 = Button(root, text="Compare average",command = lambda : Compare("a"))
btn3.place(x=30,y=150)
btn3 = Button(root, text="Compare worst",command = lambda : Compare("w"))
btn3.place(x=30,y=200)
btn3 = Button(root, text="Compare best",command = lambda : Compare("b"))
btn3.place(x=30,y=250)


root.mainloop()



