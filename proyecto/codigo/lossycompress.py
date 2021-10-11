import matplotlib as mp
from numpy.lib.npyio import genfromtxt
from matplotlib.image import imread
from matplotlib import pyplot
oldmatrix=[] #We create an empty list

filename=input("Please write your file path:\n")
#We read the file
file= open(filename,"r")
#We put the CSV numbers in a new Matrix
cont = 0
for linea in file:
    oldmatrix.append(linea.split(","))
    
file.close()

newmatrix = []#we create the new matrix
#then we create some if's for the possible steps depending on the length of the matrix
if ((len(oldmatrix)%2 == 0)and(len(oldmatrix[0])%2==0)):
    step = 2
elif((len(oldmatrix)%2 == 0)and(len(oldmatrix[0])%2!=0)):
    oldmatrix.pop()
    step = 3
elif((len(oldmatrix)%2 != 0)and(len(oldmatrix[0])%2==0)):
    oldmatrix.pop()
    step = 2
else:
    step = 3
#We sum the first two or three (dependig on the steps) elements of a row with the elements in the same position of the row below
width, height = len(oldmatrix[0]), len(oldmatrix)

for y in range(0, height, step):
    newrow = []
    for x in range(0, width, step):
        # now sum the region starting at top-left cornmer (x,y)
        total = 0
        for dy in range(step):
            for dx in range(step):
                total += int(oldmatrix[y + dy][x + dx])
        if(step == 3):
            newrow.append(total//6)
        else: #When is odd take 3 divide by 6 and when is even take 2 divide by 4
            newrow.append(total//4)
    newmatrix.append(newrow)
    
print(newmatrix)
print("\nLenght Old Matrix: \nRows: {} \nColumns: {} ".format(len(oldmatrix),len(oldmatrix[0])))
print("\nLenght New Matrix: \nRows: {} \nColumns: {}".format(len(newmatrix),len(newmatrix[0])))

imagenc = open("compressedImg.csv","w")#Creates new file .csv and writes on it, remember to remove the file created each time you execute the code.

for i in range(len(newmatrix)):
    for j in range(len(newmatrix[0])):
        if j != (len(newmatrix[0])-1):
            imagenc.write(str(newmatrix[i][j])+",")
        else:
            imagenc.write(str(newmatrix[i][j])+"\n")
imagenc.close()

my_data = genfromtxt(filename, delimiter=',')
mp.image.imsave('{} as output.png'.format(filename), my_data, cmap='gray')
image_1 = imread('{} as output.png'.format(filename))
# plot raw pixel data
mp.pyplot.imshow(image_1)
# show the figure
mp.pyplot.show()

my_data1 = genfromtxt('compressedImg.csv', delimiter=',')
mp.image.imsave('compressedImg.csv as output.png', my_data1, cmap='gray')
image_2 = imread('compressedImg.csv as output.png')
# plot raw pixel data
mp.pyplot.imshow(image_2)
# show the figure
mp.pyplot.show()

print("\nYour image has been compressed, please check in your computer files as: \n{} as output.png".format("compressedImg.csv"))