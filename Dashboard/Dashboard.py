#imports
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)





#create main window
root=tk.Tk()
root.geometry("1200x650")
root.title('Model Trainer')
root.resizable(False,False)

#global variables
dataframe_global=pd.DataFrame()



#function to create dataset page
def dataset_page():

    
    dataset_frame=tk.Frame(main_frame)
        
    
    dataset_frame=tk.Frame(main_frame)


    label_frame=tk.LabelFrame(dataset_frame,text="Data importation")
    label_frame.configure(width=1000,height=60)
    label_frame.pack(side='top')

    #import button
    import_button=tk.Button(label_frame,text="import dataset",command=lambda: browseFiles())
    import_button.pack()
    import_button.place(x=10,y=5)

    label=tk.Label(label_frame,text='No file selected')
    label.pack()
    label.place(x=500,y=5)

    #data frame
    frame1=tk.LabelFrame(dataset_frame ,text="data displayed")
    frame1.pack(fill='x',expand=True,pady=2)
    frame1.place(height=330,width=1000,rely=.1)
    


    ### Treeview Widget dataset
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
    treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

    #file frame for dataset overview
    label_frame2=tk.LabelFrame(dataset_frame,text="Dataset overview")
    label_frame2.pack()
    label_frame2.place(height=250,width=500,rely=.61,relx=0)

    frame2 = ScrolledText(label_frame2)
    frame2.pack()
    frame2.place(height=210,width=480,rely=0,relx=0)


    #frame to display other details
    frame3 = tk.LabelFrame(dataset_frame, text="Dataset Information")
    frame3.pack()
    frame3.place(height=130, width=500, rely=0.61, relx=.5)


    #Number of instances
    label_instances=tk.Label(frame3,text="Number of instances")
    label_instances.pack()
    label_instances.place(rely=.2,relx=0)

    Label_instances_number=tk.Label(frame3,text="")
    Label_instances_number.pack()
    Label_instances_number.place(relx=.5,rely=.2)

    #Number of null values
    null_values=tk.Label(frame3,text="Number of null values")
    null_values.pack()
    null_values.place(rely=.6,relx=0)

    null_number=tk.Label(frame3,text="")
    null_number.pack()
    null_number.place(relx=.5,rely=.6)

    #frame four proceed to graphs
    frame4 = tk.LabelFrame(dataset_frame, text="Generate graphs")
    frame4.pack()
    frame4.place(height=110, width=500, rely=0.82, relx=.5)

    #button to move to next page and generate graphs
    next_button=tk.Button(frame4,text="Genrate graphs",default='disabled',command=lambda:indicate(graphs_indicate,graphs_page))
    next_button.pack()
    next_button.place(relx=.4,rely=.4)



        
    #function to load dataset to dataframe
    def browseFiles():
       
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Excel files",
                                                            "*.xlsx*"),
                                                        ("csv files",
                                                            "*.csv*")))
        label['text']=filename

        try:
            excel_filename = r"{}".format(filename)
            if excel_filename[-4:] == ".csv":
                df = pd.read_csv(excel_filename)

            
                instances=df.shape[0]
                null=df.isna().sum().sum()
            
                frame2.insert(tk.INSERT,infoOut(df))
                frame2.configure(state='disabled')
                null_number['text']=null
                Label_instances_number['text']=instances
                global dataframe_global
                dataframe_global=df
             
            
                    
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
        return df
    


    def clear_data():
        tv1.delete(*tv1.get_children())
        return None

    #function to print dataset Details
    def infoOut(data,details=False):
        dfInfo = data.columns.to_frame(name='Column')
        dfInfo['Dtype'] = data.dtypes
        dfInfo.reset_index(drop=True,inplace=True)
        if details:
            totalColumns = dfInfo['Column'].count()
            dtypesCount = dfInfo['Dtype'].value_counts()
            return dfInfo, totalColumns, dtypesCount
        
        
        else:
            return dfInfo
        
    

    dataset_frame.pack(expand=True,fill='both')
    dataset_frame.place(height=650)

    


#function to create graphs page
def graphs_page():
   
   
    graphs_frame=tk.Frame(main_frame)
    
    boxplot_frame=tk.LabelFrame(graphs_frame,text='boxplot')
    boxplot_frame.pack()
    boxplot_frame.place(height=300,width=980,relx=0.01,rely=0)

    global dataframe_global
    df=dataframe_global
    plot(df['SAFETY_SCORE'])
    
    def plot(x):
    
            # the figure that will contain the plot
            fig = Figure(figsize = (5, 5),
                        dpi = 100)
        
            # list of squares
            y = x
        
            # adding the subplot
            plot1 = fig.add_subplot(111)
        
            # plotting the graph
            plot1.plot(y)
        
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig,
                                    master = boxplot_frame)  
            canvas.draw()
        
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().pack()
        
            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas,
                                        boxplot_frame)
            toolbar.update()
        
            # placing the toolbar on the Tkinter window
            canvas.get_tk_widget().pack()


   
    
   
    
    graphs_frame.pack(expand=True,fill='both')
    graphs_frame.place(height=650,width=1000)



   
      



#function to create train page
def train_page():
    train_frame=tk.Frame(main_frame)
    #Label
    mainlabel=tk.Label(train_frame,text="Please enter the data to train the model")
   
    mainlabel.pack()





#function to hide all indicators before selection
def hide_indicators():
    dataset_indicate.config(bg='#c3c3c3')
    graphs_indicate.config(bg='#c3c3c3')
    train_indicate.config(bg='#c3c3c3')


#function to remove page contents when next page is loaded
def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()


#functions to indicate current page
def indicate(lb, page):
    hide_indicators()
    lb.config(bg='red')
    delete_pages()
    page()




#options Frame
options_frame=tk.Frame(root, bg='#c3c3c3')
options_frame.pack(side='left')
options_frame.pack_propagate(False)
options_frame.configure(width=200,height=650)

#buttons for differnt options

#button and indicator for dataset
dataset=tk.Button(options_frame,text="Dataset Details",font=('Bold',15), fg='black', bg='white',command=lambda:indicate(dataset_indicate,dataset_page))
dataset.place(x=10,y=10)
dataset.configure(width=15)

dataset_indicate=tk.Label(options_frame,text='',bg='#c3c3c3')
dataset_indicate.place(x=3,y=10,height=40)


#buttons and indicator for graph
graphs=tk.Button(options_frame,text="Graphs",font=('Bold',15), fg='black', bg='white',command=lambda:indicate(graphs_indicate,graphs_page))
graphs.place(x=10,y=110)
graphs.configure(width=15)

graphs_indicate=tk.Label(options_frame,text='',bg='#c3c3c3')
graphs_indicate.place(x=3,y=110,height=40)



#button and indicator for train
train=tk.Button(options_frame,text="Train",state='disabled',font=('Bold',15), fg='black', bg='white',command=lambda:indicate(train_indicate,train_page))
train.place(x=10,y=210)
train.configure(width=15)

train_indicate=tk.Label(options_frame,text='',bg='#c3c3c3')
train_indicate.place(x=3,y=210,height=40)


#main frame
main_frame=tk.Frame(root, highlightbackground='black', highlightthickness=2,height=650, width=1000)
main_frame.pack()






root.mainloop()