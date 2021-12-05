import tkinter as tk
import tkinter.filedialog as fd
import pandas as pd
import os
import tkinter.messagebox


def openCSVFile(event):
    initialDir = ''
    fileName = fd.askopenfilename(initialdir=initialDir)
    CSVFilePathEntry.delete(0,'end')
    CSVFilePathEntry.insert(0,fileName)

def createCSV(event):
    fileFullPath = CSVFilePathEntry.get()
    if fileFullPath[-3:] != 'csv':
        tk.messagebox.showerror(message='Configuration File Format error, please use csv')
    else:
        setupDataFrame = pd.read_csv(fileFullPath)

    dotNumX= int(DotScaleXEntry.get())
    dotNumY= int(DotScaleYEntry.get())
    stepX= int(1800/dotNumX)
    stepY= int(1920/dotNumY)

    dotSizeX= int(DotSizeXEntry.get())
    dotSizeY= int(DotSizeYEntry.get())

    dotColorR= abs(int(DotREntry.get()))
    dotColorG= abs(int(DotGEntry.get()))
    dotColorB= abs(int(DotBEntry.get()))


    if dotColorB > 255 or dotColorG > 255 or dotColorB > 255:
        tk.messagebox('Improper dot color input, please input values smaller than 255!')
        return

    ###
    dataFrameToAdd= pd.DataFrame(columns=['Location-X','Location-Y','Dot-Width','Dot-Height','Red','Green','Blue'])

    for x in range(dotNumX):
        for y in range(dotNumY):
            #dotToAdd= [x*stepX, y*stepY, dotSizeX,dotSizeY,dotColorR,dotColorG,dotColorB]
            dataFrameToAdd= dataFrameToAdd.append({'Location-X': x*stepX, 'Location-Y': y*stepY, 'Dot-Width':dotSizeX,
                                   'Dot-Height':dotSizeY, 'Red':dotColorR, 'Green':dotColorG,'Blue': dotColorB},
                                  ignore_index=True)
    ### Save all the dataframe back to csv
    setupDataFrame= setupDataFrame.append(dataFrameToAdd)
    setupDataFrame.to_csv(fileFullPath,index=False)


window = tk.Tk()
window.geometry('700x100+400+400')

ConfigFileLabel= tk.Label(text = 'Setting File')
ConfigFileLabel.grid(row= 1, column= 1, columnspan= 2 )
CSVFilePathEntry = tk.Entry(width = 50)
CSVFilePathEntry.grid(row= 1, column = 3, columnspan= 9)
CSVFileButton = tk.Button(text = 'Choose CSV')
CSVFileButton.bind('<Button-1>',openCSVFile)
CSVFileButton.grid(row = 1, column = 12)

DotScaleXLabel= tk.Label(text = 'Dot NumberX')
DotScaleXLabel.grid(row= 2, column= 1 )
DotScaleXEntry = tk.Entry(width= 7)
DotScaleXEntry.grid(row= 2, column = 2, columnspan= 2)

DotScaleYLabel= tk.Label(text = 'Dot NumberY')
DotScaleYLabel.grid(row= 2, column= 4 )
DotScaleYEntry = tk.Entry(width= 7)
DotScaleYEntry.grid(row= 2, column = 5, columnspan= 2)

DotRLabel= tk.Label(text = 'R')
DotRLabel.grid(row= 2, column= 7 )
DotREntry = tk.Entry(width= 3)
DotREntry.grid(row= 2, column = 8)
DotGLabel= tk.Label(text = 'G')
DotGLabel.grid(row= 2, column= 9 )
DotGEntry = tk.Entry(width= 3)
DotGEntry.grid(row= 2, column = 10)
DotBLabel= tk.Label(text = 'B')
DotBLabel.grid(row= 2, column= 11 )
DotBEntry = tk.Entry(width= 3)
DotBEntry.grid(row= 2, column = 12)

DotSizeXLabel= tk.Label(text = 'Dot SizeX')
DotSizeXLabel.grid(row= 3, column= 1)
DotSizeXEntry = tk.Entry(width= 7)
DotSizeXEntry.grid(row= 3, column = 2, columnspan= 2)

DotSizeYLabel= tk.Label(text = 'Dot SizeY')
DotSizeYLabel.grid(row= 3, column= 4)
DotSizeYEntry = tk.Entry(width= 7)
DotSizeYEntry.grid(row= 3, column = 5, columnspan= 2)

CreateCSVButton = tk.Button(text = 'Create CSV')
CreateCSVButton.grid(row= 3, column= 12)
CreateCSVButton.bind('<Button-1>',createCSV)

window.mainloop()
