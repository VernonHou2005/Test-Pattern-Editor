import PIL
from PIL import Image
import tkinter as tk
import tkinter.filedialog as fd
import pandas as pd
import os
import tkinter.messagebox
import numpy as np

def openBMPSetting(event):
    initialDir = ''
    fileName = fd.askopenfilename(initialdir=initialDir)
    filePathEntry.delete(0,'end')
    filePathEntry.insert(0,fileName)
    pass

def Cartesian2Polar(x,y):
    X= x- displayCenter_X
    Y= y- displayCenter_Y
    rho= np.sqrt(X**2+ Y**2)
    theta= 0
    if X >= 0 and Y >= 0:
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
def Polar2Cartesian(rho, theta):
    X= rho* np.cos(theta)
    Y= rho* np.sin(theta)
    return X+ displayCenter_X, Y+ displayCenter_Y

def createBMP(event):
    fileFullPath = filePathEntry.get()
    if fileFullPath[-3:] != 'csv':
        tk.messagebox.showerror(message='Configuration File Format error, please use csv')
    else:
        setupDataFrame = pd.read_csv(fileFullPath)

        moduleType= setupDataFrame['Type']
        if moduleType[0] != 'Right Eye':
            tk.messagebox.showerror(message='Wrong Module Type, please make sure you are setting a Right Eye module')
        else:

            dotLocationsX = setupDataFrame['Location-X']
            dotLocationsY = setupDataFrame['Location-Y']
            dotWidth = setupDataFrame['Dot-Width']
            dotHeight = setupDataFrame['Dot-Height']

            dotNum = len(dotLocationsX)
            ### to make sure empty dot list would not cause any problems
            if dotLocationsX[0] == 'NaN' or 'nan':
                dotNum= 0

            imgBackground= setupDataFrame['Background'][0]

            dotR = setupDataFrame['Red']
            dotG = setupDataFrame['Green']
            dotB = setupDataFrame['Blue']

            if dotNum != len(dotLocationsY):
                tk.messagebox.showwarning('Incorrect Dot setting, please correct it before moving forward!')

            else:
                ### Create image with various background colors according to the setup csv
                if imgBackground == 'Red' or imgBackground == 'red':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), (255,0,0))
                elif imgBackground == 'Green' or imgBackground == 'green':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), (0,255,0))
                elif imgBackground == 'Blue' or imgBackground == 'blue':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), (0,0,255))
                elif imgBackground == 'White' or imgBackground == 'white':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), (255,255,255))
                elif imgBackground == 'Black' or imgBackground == 'black':
                    img = Image.new('RGB',(int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())),(0,0,0))
                else:
                    return None
                pixels = img.load()

                ### Rote 21 degree for HMD pattern if the HMDRotateCheck is selected
                if chkHMDRotateValue.get():
                    for i in range(0,dotNum):
                        rho= Cartesian2Polar(dotLocationsX[i],dotLocationsY[i])[0]
                        theta= Cartesian2Polar(dotLocationsX[i],dotLocationsY[i])[1] + 21/180*np.pi
                        dotLocationsX[i]= Polar2Cartesian(rho,theta)[0]
                        dotLocationsY[i]= Polar2Cartesian(rho,theta)[1]

                ### Check pixel value of the image
                #for i in range(0,11):
                    #print(pixels[i,i])
                ### Set pixel value according to the setting in the setup csv
                for i in range(0,dotNum):
                    #print('i= ', i)
                    for m in range(0,int(dotWidth[i])):
                        for n in range (0,int(dotHeight[i])):
                            pixels[int(dotLocationsX[i]) + m,int(dotLocationsY[i]) + n] =(int(dotR[i]),int(dotG[i]),int(dotB[i]))
                            #print('n= ', n)
                        #print ('m= ',m)


                saveName = ''
                ### Draw AB boundarys if ABCircleCheck is selected, display cender is (773,960), radius of A and B are 292 and 890 respectively
                if chkABCircleValue.get():
                    for i in range(0,int(imgWidthSettingEntry.get())):
                        for j in range(0,int(imgHeightSettingEntry.get())):
                            if 290**2 <= (abs(i- displayCenter_X))**2 + (abs(j- displayCenter_Y))**2 < 294**2 or 888**2 <= (abs(i- displayCenter_X))**2 + (abs(j- displayCenter_Y))**2 < 892**2:
                                pixels[i,j]= (0,0,0)
                ### To Flip the image to make a left eye pattern
                if chkLeftValue.get():
                    #print(chkValue.get())
                    img= img.transpose(method= PIL.Image.FLIP_LEFT_RIGHT)
                    saveName = fileFullPath.rstrip(
                        '.csv') + '_' + imgWidthSettingEntry.get() + 'X' + imgHeightSettingEntry.get() + '_Left' + '.bmp'
                elif chkHMDValue.get():
                    imgRight= img
                    imgLeft= imgRight.transpose(method= PIL.Image.FLIP_LEFT_RIGHT)
                    imgHMD= Image.new('RGB',(2* int(imgWidthSettingEntry.get()),int(imgHeightSettingEntry.get())),(0,0,0))
                    imgHMD.paste(imgLeft,(0,0))
                    imgHMD.paste(imgRight,(imgLeft.size[0],0))
                    img= imgHMD
                    saveName= fileFullPath.rstrip(
                        '.csv') + '_' + str(imgHMD.size[0]) + 'X' + str(imgHMD.size[1]) + '_HMD' + '.bmp'
                else:
                    saveName = fileFullPath.rstrip(
                        '.csv') + '_' + imgWidthSettingEntry.get() + 'X' + imgHeightSettingEntry.get() + '_Right' + '.bmp'

                saveFullPath = os.path.join(os.path.abspath(os.getcwd()), saveName)
                img.save(saveFullPath)
                #tk.messagebox.showinfo(message = 'BMP image has been successfully created!')

                img.show() # option title is not working in this function

def HMDActivate():
    if chkHMDValue.get():
        chkLeftValue.set(False)

def leftEyeActivate():
    if chkLeftValue.get():
        chkHMDValue.set(False)


### Define constant
displayCenter_X= 773
displayCenter_Y= 960

window = tk.Tk()
window.geometry('650x70+400+400')   # 2 rows and 12 columns

ConfigFileLabel= tk.Label(text = 'Setting File')
ConfigFileLabel.grid(row= 1, column= 1, columnspan= 2 )
filePathEntry = tk.Entry(width = 50)
filePathEntry.grid(row= 1, column = 3, columnspan= 9)
settingButton = tk.Button(text = 'Setting File')
settingButton.bind('<Button-1>',openBMPSetting)
settingButton.grid(row = 1, column = 12)

imgWidthSettingLabel = tk.Label(text = 'Width')
imgWidthSettingLabel.grid(sticky = 'W', row= 2, column= 2 )
imgWidthSettingEntry = tk.Entry(width = 5)
imgWidthSettingEntry.insert(0, '1824')
imgWidthSettingEntry.grid(sticky = 'W',row= 2, column= 3)
imgHeightSettingLabel = tk.Label(text = 'Height')
imgHeightSettingLabel.grid(row= 2, column= 4)
imgHeightSettingEntry = tk.Entry(width = 5)
imgHeightSettingEntry.insert(0, '1920')
imgHeightSettingEntry.grid(sticky = 'W',row= 2, column= 5)

chkLeftValue = tk.BooleanVar()
chkLeftValue.set(False)
chkHMDValue = tk.BooleanVar()
chkHMDValue.set(False)

leftEyeCheck= tk.Checkbutton(text= 'Left Eye',var= chkLeftValue, command = leftEyeActivate)
leftEyeCheck.grid(row= 2, column= 8, sticky= 'W')

HMDCheck = tk.Checkbutton(text= 'HMD',var=chkHMDValue, command= HMDActivate)
HMDCheck.grid(row= 2, column= 9, sticky= 'W')

chkABCircleValue= tk.BooleanVar()
chkABCircleValue.set(False)

ABCircleCheck= tk.Checkbutton(text= 'A/B', var= chkABCircleValue)
ABCircleCheck.grid(row= 2, column= 10, sticky= 'W')

chkHMDRotateValue= tk.BooleanVar()
chkHMDRotateValue.set(False)

HMDRotateCheck= tk.Checkbutton(text= 'Rotate', var= chkHMDRotateValue)
HMDRotateCheck.grid(row= 2, column= 11, sticky= 'W')

createBMPButton = tk.Button(text = 'Create BMP')
createBMPButton.bind('<Button-1>',createBMP)
createBMPButton.grid(sticky = 'W',row = 2, column = 12)

window.mainloop()