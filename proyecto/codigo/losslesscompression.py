import matplotlib as mp
from numpy.lib.npyio import genfromtxt
from matplotlib.image import imread
from matplotlib import pyplot
import time
    
#Method that reads the file and saves the data in a list
def createList(file):
    oldmatrix=[] 
    file= open(file,"r")
    #We put the CSV numbers in a new Matrix
    for linea in file:
        oldmatrix.append(linea.split(","))
    file.close()
    return oldmatrix

def writer(list,name):#creates new csv with compressed list
    imagec = open(name,"w")#Creates new file .csv and writes on it

    for i in range(len(list)-1):
        for j in range(len(list[i])):
            if j != (len(list[i])-1):
                imagec.write(str(list[i][j])+",")
            else:
                imagec.write(str(list[i][j])+"\n")
    imagec.close()
    print("One file has been created")
    png(name)

def png(file):
    mydata = genfromtxt(file, delimiter=',')
    mp.image.imsave('{} as output.png'.format(file), mydata, cmap='gray')
    image = imread('{} as output.png'.format(file))
    # plot raw pixel data
    mp.pyplot.imshow(image)
    # show the figure
    mp.pyplot.show()
    print("\nYour image has been {}, please check in your computer files as: \n{} as output.png".format(file[:-4],file))

def lossyCompress(list):#compresses matrix using image interpolation method
    newmatrix = []
    if ((len(list)%2 == 0)and(len(list[0])%2==0)):
        step = 2
    elif((len(list)%2 == 0)and(len(list[0])%2!=0)):
        list.pop()
        step = 3
    elif((len(list)%2 != 0)and(len(list[0])%2==0)):
        list.pop()
        step = 2
    else:
        step = 3
    width, height = len(list[0]), len(list)

    for y in range(0, height, step):
        newrow = []
        for x in range(0, width, step):
            total = 0
            for dy in range(step):
                for dx in range(step):
                    total += int(list[y + dy][x + dx])
            if(step == 3):
                newrow.append(total//6)
            else: #When is odd take 3 divide by 6 and when is even take 2 divide by 4
                newrow.append(total//4)
        newmatrix.append(newrow)

    writer(newmatrix,"lossyCompressed.csv")
    return newmatrix
    
def flatten(matrix):#flattens the matrix
    flatlist = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            flatlist.append(matrix[i][j])
    return flatlist

def listToM(list):#turns a list into a matrix
    m = []
    i = 0
    while i != len(list)-1:
        m.append(list[:431])
        list = list[431:]
    return m
            
def losslessCompress(list):#recieves list returns LZ77 compression result
    searchBuffer = 7
    lookAheadBuffer = 6
    i = 0
    Clist = []
    while i < len(list):
        #finds the longest match starting at i(current position)
        endOfBuffer = min(i + lookAheadBuffer, len(list) + 1)

        matchDistance = -1
        matchLength = -1

        for x in range(i+2, endOfBuffer):
            startIndex = max(0, i - searchBuffer)
            subList = list[i:x]
            for y in range(startIndex, i):
                repetitions = len(subList)//(i-y)
                last = len(subList)%(i-y)

                matchedList = list[y:i] * repetitions + list[y:y+last]

                if matchedList == subList and len(subList)>matchLength:
                    matchDistance = i - y
                    matchLength = len(subList)
        if matchDistance > 0 and matchLength > 0:
            diferentAdded = min(i+matchLength, len(list)-1)
            Clist.append("<" + str(matchDistance) + "," + str(matchLength) + "," + str(list[diferentAdded]) + ">")
            i = i + matchLength+1
        else:
            Clist.append('<0,0,' + str(list[i]) + '>')
            i = i + 1
    return Clist


def losslessDecompress(list):#takes the LZ77 compression and returns a list
    Dlist = []
    i = 0
    while i < len(list):
        element = list[i]
        comma1 = element.find(',')
        comma2 = element.rfind(',')
        if list[i][1:comma1] == '0':
            Dlist.append(list[i][comma2+1:element.find('>')])
            i = i + 1
        else:
            if list[i][comma1+1:comma2] == '1':
                Dlist.append(Dlist[-(int(list[i][1:comma1]))])
                Dlist.append(list[i][comma2+1:element.find('>')])
                i = i + 1
            else:
                appnd= []
                f = -(int(list[i][1:comma1]))
                m = int(list[i][comma1+1:comma2])
                if abs(f) > m:
                    while m > 0:
                        appnd.append(Dlist[f])
                        f = f + 1
                        m = m - 1
                    for item in appnd:
                        Dlist.append(item)
                    Dlist.append(list[i][comma2+1:element.find('>')])
                    i = i + 1
                else:
                    save = m - int(list[i][1:comma1])
                    m = int(list[i][1:comma1])
                    while m > 0:
                        appnd.append(Dlist[f])
                        f = f + 1
                        m = m - 1
                    for item in appnd:
                        Dlist.append(item)
                    while save > 0:
                        Dlist.append(Dlist[-1])
                        save = save - 1
                    Dlist.append(list[i][comma2+1:element.find('>')])
                    i = i + 1
    return Dlist

def main():
    filename=input("Please write your file path:\n")
    oldList = createList(filename)
    lossy = lossyCompress(oldList)
    lossless = losslessCompress(flatten(lossy))
    decompress = losslessDecompress(lossless)
    writer(listToM(decompress),'decompressedImg.csv')
    print("\nLength Old Matrix: \nRows: {} \nColumns: {}".format(len(oldList),len(oldList[0])))
    print("\nLength New Matrix: \nRows: {} \nColumns: {}".format(len(lossy),len(lossy[0])))
    print("\nLength Decompressed Matrix: \nRows: {} \nColumns: {}".format(len(listToM(decompress)),len(listToM(decompress)[0])))

main()

