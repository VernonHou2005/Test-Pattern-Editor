import PIL
from PIL import Image
import tkinter as tk
import tkinter.filedialog as fd
import pandas as pd
import os
import tkinter.messagebox

def openBMPSetting(event):
    initialdir = '/Volumes/Samsung_T5/Code-Repository/Lab-PC/PycharmProjects/Test-Pattern-Creator'
    fileName = fd.askopenfilename(initialdir=initialdir)
    filePathEntry.delete(0,'end')
    filePathEntry.insert(0,fileName)
    pass

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

            imgBackground= setupDataFrame['Background'][0]

            dotR = setupDataFrame['Red']
            dotG = setupDataFrame['Green']
            dotB = setupDataFrame['Blue']

            if dotNum != len(dotLocationsY):
                tk.messagebox.showwarning('Incorrect Dot setting, please correct it before moving forward!')

            else:
                ### Create image with various background colors according to the setup csv
                if imgBackground == 'Red' or imgBackground == 'red':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), 'red')
                elif imgBackground == 'Green' or imgBackground == 'green':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), 'green')
                elif imgBackground == 'Blue' or imgBackground == 'blue':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), 'blue')
                elif imgBackground == 'White' or imgBackground == 'white':
                    img = Image.new('RGB', (int(imgWidthSettingEntry.get()), int(imgHeightSettingEntry.get())), 'white')
                else:
                    return None
                pixels = img.load()
                # Set pixel value according to the setting in the setup csv
                for i in range(0,dotNum):
                    for m in range(1,dotWidth[i]):
                        for n in range (1,dotHeight[i]):
                            pixels[dotLocationsX[i] + m - 1,dotLocationsY[i] + n - 1] =(dotR[i],dotG[i],dotB[i])

                saveName = ''
                ### To Flip the image to make a left eye pattern
                if chkValue.get():
                    #print(chkValue.get())
                    img= img.transpose(method= PIL.Image.FLIP_LEFT_RIGHT)
                    saveName = fileFullPath.rstrip(
                        '.csv') + '_' + imgWidthSettingEntry.get() + 'X' + imgHeightSettingEntry.get() + '_Left' + '.bmp'
                else:
                    saveName = fileFullPath.rstrip(
                        '.csv') + '_' + imgWidthSettingEntry.get() + 'X' + imgHeightSettingEntry.get() + '_Right' + '.bmp'

                saveFullPath = os.path.join(os.path.abspath(os.getcwd()), saveName)
                img.save(saveFullPath)
                tk.messagebox.showinfo(message = 'BMP image has been successfully created!')

                img.show()
window = tk.Tk()
window.geometry('600x70+400+400')

ConfigFileLabel= tk.Label(text = 'Setting File')
ConfigFileLabel.grid(row= 1, column= 1, columnspan= 2 )
filePathEntry = tk.Entry(width = 40)
filePathEntry.grid(row= 1, column = 3, columnspan= 8)
settingButton = tk.Button(text = 'Setting File')
settingButton.bind('<Button-1>',openBMPSetting)
settingButton.grid(row = 1, column = 11)

imgWidthSettingLabel = tk.Label(text = 'Width')
imgWidthSettingLabel.grid(sticky = 'W', row= 2, column= 2 )
imgWidthSettingEntry = tk.Entry(width = 5)
imgWidthSettingEntry.insert(0, '1800')
imgWidthSettingEntry.grid(sticky = 'W',row= 2, column= 3)
imgHeightSettingLabel = tk.Label(text = 'Height')
imgHeightSettingLabel.grid(row= 2, column= 4)
imgHeightSettingEntry = tk.Entry(width = 5)
imgHeightSettingEntry.insert(0, '1920')
imgHeightSettingEntry.grid(sticky = 'W',row= 2, column= 5)

chkValue = tk.BooleanVar()
chkValue.set(False)
leftEyeCheck= tk.Checkbutton(text= 'Left Eye',var= chkValue)
leftEyeCheck.grid(row= 2, column= 10, sticky= 'W')
createBMPButton = tk.Button(text = 'Create BMP')
createBMPButton.bind('<Button-1>',createBMP)
createBMPButton.grid(sticky = 'W',row = 2, column = 11)

window.mainloop()