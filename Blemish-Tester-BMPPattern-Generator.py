import PIL
from PIL import Image
import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk
import pandas as pd
import os
import tkinter.messagebox
import numpy as np

def openBMPSetting(event):
    initialDir = ''
    fileName = fd.askopenfilename(initialdir=initialDir)
    filePathEntry.delete(0,'end')
    filePathEntry.insert(0,fileName)

def Cartesian2Polar(x,y,center_x,center_y):
    X= x- center_x
    Y= center_y - y
    rho= np.sqrt(X**2+ Y**2)
    theta= 0
    if X == 0:
        if Y >=0:
            theta = np.pi/2
        elif Y < 0:
            theta = np.pi *3/2
    elif X > 0 and Y >= 0:
        theta=np.arctan(Y/X)
    elif X < 0 and Y >=0:
        theta= np.arctan(Y/X)+ np.pi
    elif X <0 and Y < 0:
        theta= np.arctan(Y/X)+ np.pi
    elif X > 0 and Y < 0:
        theta= np.arctan(Y/X)+ np.pi* 2
    else:
        pass
    return rho,theta
def Polar2Cartesian(rho, theta,center_x,center_y):
    X= rho* np.cos(theta)
    Y= rho* np.sin(theta)
    return X + center_x, center_y - Y

### Define the draw circle function, which can be used to draw AB boundaries and also random customer needed circels
def drawCircle(x,y,Radius,image):
    circleCenter_x = x
    circleCenter_y = y
    circleRadius = Radius
    circleWidth = 1
    pixels = image.load()
    imageWidth = image.width
    imageHeight = image.height
    ### Determine the color of the circle according to the background color
    if int(BackgroundREntry.get()) == 0 and int(BackgroundGEntry.get()) == 0 and int(BackgroundBEntry.get()) == 0:
        circle_R = 255
        circle_G = 255
        circle_B = 255
    else:
        circle_R = 0
        circle_G = 0
        circle_B = 0
    for i in range(0, imageWidth):
        for j in range(0, imageHeight):
            if (circleRadius - circleWidth) ** 2 <= (abs(i - circleCenter_x)) ** 2 + (
            abs(j - circleCenter_y)) ** 2 < (circleRadius + circleWidth) ** 2:
                pixels[i, j] = (circle_R, circle_G, circle_B)

### Define the draw dboule side AB circle function, which is a specicial request from SQE team
def drawABCircle(x_left,y_left,x_right,y_right,Radius,image):
    circleRadius = Radius
    circleWidth = 1
    pixels = image.load()
    imageWidth = image.width
    imageHeight = image.height

    ### Determine the color of the circle according to the background color
    if int(BackgroundREntry.get()) == 0 and int(BackgroundGEntry.get()) == 0 and int(BackgroundBEntry.get()) == 0:
        circle_R = 0
        circle_G = 0
        circle_B = 127   #special request by SQE. Circle in Black background should be in (0,0,127)
    else:
        circle_R = 0
        circle_G = 0
        circle_B = 0
    for i in range(0,imageWidth ):
        for j in range(0,imageHeight ):
            if ((circleRadius - circleWidth) ** 2 <= (abs(i - x_left)) ** 2 + (
                abs(j - y_left)) ** 2 < (circleRadius + circleWidth) ** 2) and i <= imageWidth/2:
                pixels[i, j] = (circle_R, circle_G, circle_B)
            elif ((circleRadius - circleWidth) ** 2 <= (abs(i - x_right)) ** 2 + (
                abs(j - y_right)) ** 2 < (circleRadius + circleWidth) ** 2) and i >= imageWidth/2:
                pixels[i, j] = (circle_R, circle_G, circle_B)

def createBMP(event):
    fileFullPath = filePathEntry.get()
    if fileFullPath[-3:] != 'csv':
        tk.messagebox.showerror(message='Configuration File Format error, please use csv')
    else:
        setupDataFrame = pd.read_csv(fileFullPath)

        dotLocationsX = setupDataFrame['Location-X']
        dotLocationsY = setupDataFrame['Location-Y']
        dotWidth = setupDataFrame['Dot-Width']
        dotHeight = setupDataFrame['Dot-Height']

        dotNum = len(dotLocationsX)

        ### to make sure empty dot list would not cause any problems
        ### dataframe.empty has to be used to check a empty dataframe
        if setupDataFrame.empty:
            dotNum = 0
        elif np.isnan(dotLocationsX[0]):
            dotNum= 0

        ### Get RGB value for each dot
        dotR = setupDataFrame['Red']
        dotG = setupDataFrame['Green']
        dotB = setupDataFrame['Blue']

        ### Get background RGB values from User's input
        imgBackgroundR= abs(int(BackgroundREntry.get()))
        imgBackgroundG= abs(int(BackgroundGEntry.get()))
        imgBackgroundB= abs(int(BackgroundBEntry.get()))

        imageWidth = 0
        imageHeight = 0

        opticalCenter_x_left = 0
        opticalCenter_y = 0
        opticalCenter_x_right = 0

        radius_A = 0
        radius_B = 0

        ### determine the image size based on the product
        if productCombobox.get() == 'Seacliff':
            imageWidth = 1800
            imageHeight = 1920

            opticalCenter_x_left = 1027
            opticalCenter_y = 960
            opticalCenter_x_right = 773

            radius_A = 292
            radius_B = 890


        elif productCombobox.get() == 'Eureka':
            imageWidth = 2064
            imageHeight = 2208

            opticalCenter_x_left = 1179
            opticalCenter_y = 1104
            opticalCenter_x_right = 885

            radius_A = 336
            radius_B = 1024
        else:
            pass

        ### If user's input of RGB value is larger than 255, pop up a error message and ask user to re-input
        if imgBackgroundR >255 or imgBackgroundB >255 or imgBackgroundG >255:
            tk.messagebox.showerror(message='Improper background color input, please input values smaller than 255!')
            return

        ### Set the background image based on background RGB setting
        img = Image.new('RGB', (imageWidth, imageHeight),(imgBackgroundR, imgBackgroundG, imgBackgroundB))

        pixels = img.load()

        ### Rote 21 degree for HMD pattern if the HMDRotateCheck is selected
        if chkHMDRotateValue.get():
            for i in range(0,dotNum):
                rho, theta = Cartesian2Polar(dotLocationsX[i],dotLocationsY[i],opticalCenter_x_right,opticalCenter_y)
                theta= theta + 21/180*np.pi
                dotLocationsX[i], dotLocationsY[i] = Polar2Cartesian(rho,theta,opticalCenter_x_right,opticalCenter_y)

        ### Check pixel value of the image
        #for i in range(0,11):
            #print(pixels[i,i])

        ### Set pixel value according to the setting in the setup csv
        for i in range(0,dotNum):
            if dotLocationsX[i] < imageWidth and dotLocationsY[i] < imageHeight:
                #print('i= ', i)
                for m in range(0,int(dotWidth[i])):
                    for n in range (0,int(dotHeight[i])):
                        pixels[int(dotLocationsX[i]) + m,int(dotLocationsY[i]) + n] =(int(dotR[i]),int(dotG[i]),int(dotB[i]))


        ### Draw AB boundarys if ABCircleCheck is selected, display cender is (773,960), radius of A and B are 292 and 890 respectively
        if chkABCircleValue.get():
        ### Normal
            drawCircle(opticalCenter_x_right,opticalCenter_y,radius_A,img)
            drawCircle(opticalCenter_x_right,opticalCenter_y,radius_B,img)

        ### Draw double AB boundarys if ABCircleCheck is selected, display cender is (773,960), radius of A and B are 292 and 890 respectively
        if chkDoubleABCircleValue.get():

            ### double AB circle drawing for Eureka Optical center left: (885,1104); right (1179,1104)
            drawABCircle(opticalCenter_x_left,opticalCenter_y,opticalCenter_x_right,opticalCenter_y,radius_A,img)
            drawABCircle(opticalCenter_x_left,opticalCenter_y,opticalCenter_x_right,opticalCenter_y,radius_B,img)

        #### Draw customized circles according to the location and radius information input in the GUI
        if Circle1CenterEntry_x.get().isnumeric() and Circle1CenterEntry_y.get().isnumeric() and Circle1RadiusEntry.get().isnumeric():
            drawCircle(int(Circle1CenterEntry_x.get()),int(Circle1CenterEntry_y.get()),int(Circle1RadiusEntry.get()),img)
        if Circle2CenterEntry_x.get().isnumeric() and Circle2CenterEntry_y.get().isnumeric() and Circle2RadiusEntry.get().isnumeric():
            drawCircle(int(Circle2CenterEntry_x.get()), int(Circle2CenterEntry_y.get()), int(Circle2RadiusEntry.get()),
                       img)
        if Circle3CenterEntry_x.get().isnumeric() and Circle3CenterEntry_y.get().isnumeric() and Circle3RadiusEntry.get().isnumeric():
            drawCircle(int(Circle3CenterEntry_x.get()), int(Circle3CenterEntry_y.get()), int(Circle3RadiusEntry.get()),
                       img)
        if Circle4CenterEntry_x.get().isnumeric() and Circle4CenterEntry_y.get().isnumeric() and Circle4RadiusEntry.get().isnumeric():
            drawCircle(int(Circle4CenterEntry_x.get()), int(Circle4CenterEntry_y.get()), int(Circle4RadiusEntry.get()),
                       img)

        ### To Flip the image to make a left eye pattern
        if chkLeftValue.get():
            #print(chkValue.get())
            img= img.transpose(method= PIL.Image.FLIP_LEFT_RIGHT)
            saveName = fileFullPath.rstrip(
                '.csv') + '_' + str(imageWidth) + 'X' + str(imageHeight) + '_Left' + '.bmp'
        elif chkHMDValue.get():
            imgRight= img
            imgLeft= imgRight.transpose(method= PIL.Image.FLIP_LEFT_RIGHT)
            imgHMD= Image.new('RGB',(2* imageWidth,imageHeight),(0,0,0))
            imgHMD.paste(imgLeft,(0,0))
            imgHMD.paste(imgRight,(imgLeft.size[0],0))
            img= imgHMD
            saveName= fileFullPath.rstrip(
                '.csv') + '_' + str(imgHMD.size[0]) + 'X' + str(imgHMD.size[1]) + '_HMD' + '.bmp'
        else:
            saveName = fileFullPath.rstrip(
                '.csv') + '_' + str(imageWidth) + 'X' + str(imageHeight) + '_Right' + '.bmp'

        saveFullPath = os.path.join(os.path.abspath(os.getcwd()), saveName)
        img.save(saveFullPath)
        #tk.messagebox.showinfo(message = 'BMP image has been successfully created!')

        img.show() # option title is not working in this function

def HMDActivate():
    if chkHMDValue.get():
        chkLeftValue.set(False)
        chkDoubleABCircleValue.set(False)

def leftEyeActivated():
    if chkLeftValue.get():
        chkHMDValue.set(False)
        chkDoubleABCircleValue.set(False)

def ABCircleEnabled():
    if chkABCircleValue.get():
        chkDoubleABCircleValue.set(False)

def DoubleCircleEnabled():
    if chkDoubleABCircleValue.get():
        chkLeftValue.set(False)
        chkHMDValue.set(False)
        chkABCircleValue.set(False)
        chkHMDRotateValue.set(False)

def HMDRotateEnabled():
    if chkHMDRotateValue.get():
        chkDoubleABCircleValue.set(False)



window = tk.Tk()
window.title('Display Pattern Generator V1.1')
window.geometry('650x200+400+400')
####### Row 0 ########
ConfigFileLabel= tk.Label(text = 'Setting File')
ConfigFileLabel.grid(sticky= 'W',row= 0, column= 1, columnspan= 2 )
filePathEntry = tk.Entry(width= 48)
filePathEntry.grid(row= 0, column = 3, columnspan= 18)
settingButton = tk.Button(text = 'Setting File')
settingButton.bind('<Button-1>',openBMPSetting)
settingButton.grid(row = 0, column = 21, columnspan= 3)
####### Row 1 ######### manul input the image width and height
# imgWidthSettingLabel = tk.Label(text = 'Width')
# imgWidthSettingLabel.grid( sticky= 'E',row= 1, column= 1 )
# imgWidthSettingEntry = tk.Entry(width= 5)
# imgWidthSettingEntry.insert(0, '1824')
# imgWidthSettingEntry.grid(row= 1, column= 2,columnspan= 2)
# imgHeightSettingLabel = tk.Label(text = 'Height')
# imgHeightSettingLabel.grid(sticky= 'E',row= 1, column= 4)
# imgHeightSettingEntry = tk.Entry(width = 5)
# imgHeightSettingEntry.insert(0, '1920')
# imgHeightSettingEntry.grid(sticky= 'W',row= 1, column= 5, columnspan= 2)

#### Row 1 ######### image size determination by sellecting the product name
productLabel = tk.Label(text = 'Product')
productLabel.grid(row = 1, column = 1)
productVariable = tk.StringVar()
productCombobox = ttk.Combobox(width = 10, textvariable = productVariable)
productCombobox['value'] = ('Seacliff','Eureka')
productCombobox.grid(row = 1, column = 2, columnspan = 5)


BackgroundSettingLabel = tk.Label(text = 'Background')
BackgroundSettingLabel.grid(sticky= 'E',row= 1, column= 8,columnspan= 4)
BackgroundRSettingLabel = tk.Label(text = 'R')
BackgroundRSettingLabel.grid( sticky= 'E',row= 1, column= 12)
BackgroundREntry = tk.Entry(width = 3)
BackgroundREntry.insert(0, '0')
BackgroundREntry.grid(sticky= 'W',row= 1, column= 13,columnspan= 2)

BackgroundGSettingLabel = tk.Label(text = 'G')
BackgroundGSettingLabel.grid(sticky= 'E',row= 1, column= 15)
BackgroundGEntry = tk.Entry(width = 3)
BackgroundGEntry.insert(0, '0')
BackgroundGEntry.grid(sticky= 'W', row= 1, column= 16,columnspan= 2)

BackgroundBSettingLabel = tk.Label(text = 'B')
BackgroundBSettingLabel.grid(sticky= 'E',row= 1, column= 18)
BackgroundBEntry = tk.Entry(width = 3)
BackgroundBEntry.insert(0, '0')
BackgroundBEntry.grid(sticky= 'W', row= 1, column= 19,columnspan= 2)

chkLeftValue = tk.BooleanVar()
chkLeftValue.set(False)
chkHMDValue = tk.BooleanVar()
chkHMDValue.set(False)
######## Row 2 #########
leftEyeCheck= tk.Checkbutton(text= 'Left Eye',var= chkLeftValue, command = leftEyeActivated)
leftEyeCheck.grid(row= 2, column= 2, columnspan= 3)

HMDCheck = tk.Checkbutton(text= 'HMD',var=chkHMDValue, command= HMDActivate)
HMDCheck.grid(row= 2, column= 5, columnspan= 3 )

chkABCircleValue= tk.BooleanVar()
chkABCircleValue.set(False)

ABCircleCheck= tk.Checkbutton(text= 'A/B', var= chkABCircleValue, command = ABCircleEnabled)
ABCircleCheck.grid(row= 2, column= 8, sticky= 'W',columnspan= 3)

chkDoubleABCircleValue= tk.BooleanVar()
chkDoubleABCircleValue.set(False)

doubleABCircleCheck= tk.Checkbutton(text= 'Double A/B', var= chkDoubleABCircleValue,command = DoubleCircleEnabled)
doubleABCircleCheck.grid(row= 2, column= 11, sticky= 'W',columnspan= 4)


chkHMDRotateValue= tk.BooleanVar()
chkHMDRotateValue.set(False)

HMDRotateCheck= tk.Checkbutton(text= 'Rotate', var= chkHMDRotateValue, command = HMDRotateEnabled)
HMDRotateCheck.grid(row= 2, column= 15, sticky= 'W',columnspan= 3)

createBMPButton = tk.Button(text = 'Create BMP')
createBMPButton.bind('<Button-1>',createBMP)
createBMPButton.grid(sticky = 'W',row = 2, column = 21,columnspan= 3)


######## Row 3&4 #########
Circle1CenterLabel = tk.Label(text = 'Circle1 at')
Circle1CenterLabel.grid(row= 3, column= 1,columnspan= 2)
Circle1CenterEntry_x = tk.Entry(width = 4)
Circle1CenterEntry_x.insert(0, 'x')
Circle1CenterEntry_x.grid(sticky= 'W',row= 3, column= 3,columnspan= 2)
Circle1CenterEntry_y = tk.Entry(width = 4)
Circle1CenterEntry_y.insert(0, 'y')
Circle1CenterEntry_y.grid(sticky= 'W',row= 4, column= 3,columnspan= 2)

Circle1RadiusLabel = tk.Label(text= 'Radius')
Circle1RadiusLabel.grid(row= 3, column= 4,columnspan= 3)
Circle1RadiusEntry = tk.Entry(width = 4)
Circle1RadiusEntry.insert(0, '0')
Circle1RadiusEntry.grid(sticky= 'W', row= 3, column= 6,columnspan= 2)

Circle2CenterLabel = tk.Label(text = 'Circle2 at')
Circle2CenterLabel.grid(sticky= 'E',row= 3, column= 10,columnspan= 3)
Circle2CenterEntry_x = tk.Entry(width = 4)
Circle2CenterEntry_x.insert(0, 'x')
Circle2CenterEntry_x.grid(sticky= 'W', row= 3, column= 14,columnspan= 2)
Circle2CenterEntry_y = tk.Entry(width = 4)
Circle2CenterEntry_y.insert(0, 'y')
Circle2CenterEntry_y.grid(sticky= 'W', row= 4, column= 14,columnspan= 2)

Circle2RadiusLabel = tk.Label(text= 'Radius')
Circle2RadiusLabel.grid(row= 3, column= 16,columnspan= 2)
Circle2RadiusEntry = tk.Entry(width = 4)
Circle2RadiusEntry.insert(0, '0')
Circle2RadiusEntry.grid( row= 3, column=18,columnspan= 2)


######## Row 5&6 #########
Circle3CenterLabel = tk.Label(text = 'Circle3 at')
Circle3CenterLabel.grid(row= 5, column= 1,columnspan= 2)
Circle3CenterEntry_x = tk.Entry(width = 4)
Circle3CenterEntry_x.insert(0, 'x')
Circle3CenterEntry_x.grid(sticky= 'W',row= 5, column= 3,columnspan= 2)
Circle3CenterEntry_y = tk.Entry(width = 4)
Circle3CenterEntry_y.insert(0, 'y')
Circle3CenterEntry_y.grid(sticky= 'W',row= 6, column= 3,columnspan= 2)

Circle3RadiusLabel = tk.Label(text= 'Radius')
Circle3RadiusLabel.grid(row= 5, column= 4,columnspan= 3)
Circle3RadiusEntry = tk.Entry(width = 4)
Circle3RadiusEntry.insert(0, '0')
Circle3RadiusEntry.grid(sticky= 'W', row= 5, column= 6,columnspan= 2)

Circle4CenterLabel = tk.Label(text = 'Circle4 at')
Circle4CenterLabel.grid(sticky= 'E',row= 5, column= 10,columnspan= 3)
Circle4CenterEntry_x = tk.Entry(width = 4)
Circle4CenterEntry_x.insert(0, 'x')
Circle4CenterEntry_x.grid(sticky= 'W', row= 5, column= 14,columnspan= 2)
Circle4CenterEntry_y = tk.Entry(width = 4)
Circle4CenterEntry_y.insert(0, 'y')
Circle4CenterEntry_y.grid(sticky= 'W', row= 6, column= 14,columnspan= 2)

Circle4RadiusLabel = tk.Label(text= 'Radius')
Circle4RadiusLabel.grid(row= 5, column= 16,columnspan= 2)
Circle4RadiusEntry = tk.Entry(width = 4)
Circle4RadiusEntry.insert(0, '0')
Circle4RadiusEntry.grid( row= 5, column=18,columnspan= 2)


window.mainloop()