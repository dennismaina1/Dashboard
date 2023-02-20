#imports
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import filedialog
from methods import *
from tkinter.scrolledtext import ScrolledText


  #create main window
root=tk.Tk()
root.config(background = "white")
root.geometry("1000x650")
root.resizable(False,False)
#logo

#Label
mainlabel=tk.Label(root,text="Please enter the data to train the model")

#arranging the label 
mainlabel.place(height=20,width=1000,relx=0,rely=0)
mainlabel.configure(font="Arial",fg='blue',padx= 50, pady= 20)

file_frame = tk.LabelFrame(root, text="Open File")
file_frame.place(height=100, width=1000, rely=0.05, relx=0)

# Buttons
button1 = tk.Button(file_frame, text="Browse A File", command=lambda: browseFiles())
button1.place(height=20,width=100,relx=0,rely=.4)

# The file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0.4, relx=0.2)




#data frame
frame1=tk.LabelFrame(root ,text="data displayed")
frame1.place(height=250,width=1000,rely=.20,relx=0)


### Treeview Widget dataset
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget



#frame to display dataset details
file_frame2 = tk.LabelFrame(root, text="Dataset Information")
file_frame2.place(height=200, width=500, rely=0.59, relx=0)

frame2 = ScrolledText(file_frame2)
frame2.place(height=170,width=480,rely=0,relx=0)

#frame to display other details
file_frame3 = tk.LabelFrame(root, text="Dataset Information")
file_frame3.place(height=200, width=500, rely=0.59, relx=.5)









#function to load dataset to dataframe
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Excel files",
                                                        "*.xlsx*"),
                                                       ("csv files",
                                                        "*.csv*")))
    label_file['text']=filename

    try:
        excel_filename = r"{}".format(filename)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
            #frame2['text']=infoOut(df)
            
            frame2.insert(tk.INSERT,infoOut(df))
           
        else:
            df = pd.read_excel(excel_filename)

        
    
    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {filename}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None


def clear_data():
    tv1.delete(*tv1.get_children())
    return None

#function to print dataset Details
def infoOut(data,details=False):
    dfInfo = data.columns.to_frame(name='Column')
    dfInfo['Non-Null Count'] = data.notna().sum()
    dfInfo['Dtype'] = data.dtypes
    dfInfo.reset_index(drop=True,inplace=True)
    if details:
        rangeIndex = (dfInfo['Non-Null Count'].min(),dfInfo['Non-Null Count'].min())
        totalColumns = dfInfo['Column'].count()
        dtypesCount = dfInfo['Dtype'].value_counts()
        totalMemory = dfInfo.memory_usage().sum()
        return dfInfo, rangeIndex, totalColumns, dtypesCount, totalMemory
      
    
    else:
        return dfInfo


#run program
root.mainloop()