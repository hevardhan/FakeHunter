#-----------------------------------------------------------------#
# I M P O R T S                                                   #
#-----------------------------------------------------------------#
import tkinter as t
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import pytchat
import pandas as pd
import numpy as np
from chat_downloader import ChatDownloader
import matplotlib.pyplot as plt
import plotly.express as px

# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# obj = SentimentIntensityAnalyzer()

#----------------------------------------------------------------#
# F L A G   W O R D S   L I S T S                                #
#----------------------------------------------------------------#
flag_list_2 = ['loss','ghatta','indicator','buy','sell','telegram','whatsapp','wattsapp','join my','premium','tp','sl','stop','profit','teligram','hit']
flag_list_1 = ['profit','education','risk']

#----------------------------------------------------------------#
# M A I N   C L A S S                                            #
#----------------------------------------------------------------#
class Main:
    #---------------------------#
    # Init Function             #
    #---------------------------#
    def __init__(self): 
        self.flag_positive = 0
        self.flag_negative = 0
        self.flag_neutral  = 0
        self.data = {}
        self.radio = ""
        self.data_number = 0
        self.dict_graph = {}
    
    #---------------------------#
    # Visualization Function    #
    #---------------------------#
    def gen_visual(self):
        listbox_items = mylist.get(0,t.END)
        no_items = len(listbox_items)
        dict_counter = 0
        for item in listbox_items:
            x = item.split("Comment : ")
            comment = x[1]
            msg = comment.lower()
            msg_list = msg.split(" ")
            for word in msg_list:
                if word in flag_list_2:
                    self.flag_negative += 1
                elif word in flag_list_1:
                    self.flag_positive += 1
                else:
                    self.flag_neutral += 1
            self.dict_graph[dict_counter] = {"Comment":comment,
                                             "Positive":self.flag_positive,
                                             "Negative":self.flag_negative,
                                             "Neutral":self.flag_neutral}
            dict_counter += 1

        df_graph = pd.DataFrame(self.dict_graph).transpose()
        df_graph = df_graph.drop("Comment",axis=1)
        df_graph = df_graph.drop("Neutral",axis=1)
        
        fig = px.area(df_graph,color_discrete_sequence=["green", "red"],title="Sentiment Curve")
        fig.show()
        
    
    #----------------------------#
    # Scrape Comment Function    #
    #----------------------------#    
    def scrapeCom(self):
        text = url_f2_entry.get()
        self.radio = v.get()
        key = text.split("=")
        if self.radio == 'Live':
            chat = pytchat.create(video_id=key[1])
            
            for c in chat.get().sync_items():
                msg = c.message.lower().split(" ") #Splits the Comment
                mylist.insert(t.END,f"Comment : {c.message}")
                self.data[self.data_number] = {"message" : c.message,
                                               "timestamp":c.timestamp,
                                               "Author-User Name":c.author.name,
                                               "Author Channel":c.author.channelId,
                                               "message_Id":c.id}
                self.data_number += 1
            # mylist.after(1000,Main.scrapeCom(self)) 
            
            
        elif self.radio == 'Pre-recorded':
            url = text
            chat = ChatDownloader().get_chat(url)       # create a generator
            data_num = 0
            for message in chat:
                # if data_num < 100:                     # iterate over messages
                    self.data[data_num] = message       # print the formatted message
                    data_num +=1
                    msg = message["message"]
                    # self.time.append(message['time_in_seconds'])
                    mylist.insert(t.END,f"Comment : {msg}")

    #----------------------------#
    # Generate Excel Function    #
    #----------------------------#
    def save_xl(self):
        a = fd.asksaveasfilename(initialfile="Untitled.xlsx",defaultextension=".xlsx",filetypes = [('excel files', '*.xlsx'),('All files', '*.*')])
        if self.radio == "Pre-recorded":
            df = pd.DataFrame(data=self.data)
            df = df.transpose()
            df_author = df['author'].to_dict()
            df = df.drop("author",axis=1)
            df_auth = pd.DataFrame(df_author)
            df_auth = df_auth.transpose()
            with pd.ExcelWriter(a) as writer:
                df.to_excel(writer,sheet_name="comment_data")
                df_auth.to_excel(writer,sheet_name="author_data")
        elif self.radio == 'Live':
            df = pd.DataFrame(data = self.data)
            df = df.transpose()
            df.to_excel(a,sheet_name="data")
#--------------------------------------------------------#
# D E V E L O P E R   I N F O   F U N C T I O N          #
#--------------------------------------------------------#
def dev_info():
    info = '''               
    Team FakeHunter
    
    Anupkumar M Bongale
    Jayant Jagtap
    Mayur Gaikwad
    Hevardhan Saravanan
    '''
    messagebox.showinfo("Developer Information",info)

#--------------------------------------------------------#
# H E L P   F U N C T I O N                              #
#--------------------------------------------------------#
def help_info():
    help_in = '''
    Step 1 : Enter the url in the given text box
    Step 2 : Click "Scrape Comments" button to extract all the comments
    Step 3 : Click "Generate Visualization" to get visual analysis of the comments
    Step 4 : Click "Generate Excel" to generate all these data to excel sheet
    '''
    messagebox.showinfo("Help",help_in)
    

###################################################################################################################################

#----------------------------------------#
# U S E R   I N T E R F A C E            #
#----------------------------------------#
win = t.Tk()
win.title("Fake Hunter")

win.geometry("700x500")
win.state("zoomed")

app = Main()

image = Image.open("assets/SIT.png")
pic = image.resize((230,135))
img = ImageTk.PhotoImage(pic)
l1 = t.Label(win, image=img)

info_btn = t.Button(win,text="Developer Info",font=("Lucida Sans",15,"bold"),command=dev_info)
help_btn = t.Button(win,text="Help",font=("Lucida Sans",15,"bold"),command=help_info)


title = t.Label(win,text = "F  A  K  E    H  U  N  T  E  R",font=("Lucida Sans",32,"bold"))


f1 = t.Frame(win,width = 500,height=550,bg="#333333")
f2 = t.Frame(win,width = 850,height=550,bg="#333333")

flag_counter = 0

url_f2 = t.Label(f2, text = "Enter the Youtube URL    : ",font=("Lucida Sans",18,"bold"),bg="#333333",fg = "white")
url_f2_entry = t.Entry(f2,font=("Lucida Sans",18,"bold"))
scrape_btn = t.Button(f2,text = "Scrape Comments",font=("Lucida Sans",18,"bold"),command=app.scrapeCom)
gen_xl_btn = t.Button(f2,text = "Generate Excel",font=("Lucida Sans",18,"bold"),command=app.save_xl)
gen_senti_btn = t.Button(f2,text="Generate Visualization",font=("Lucida Sans",18,"bold"),command=app.gen_visual)

title_f2  = t.Label(f2,text="Choose the type of video :",font=("Lucida Sans",18,"bold"),bg="#333333",fg = "white")
v = t.StringVar()
v.set(None)
r1 = t.Radiobutton(f2, text='Streaming', variable=v,font=("Arial",18),bg="white",value="Live")
r2 = t.Radiobutton(f2, text='Streamed', variable=v,font=("Arial",18),bg="white",value="Pre-recorded")


r1.place(x=400,y=150)
r2.place(x=575,y=150)
title_f2.place(x=50,y=150)

url_f2.place(x = 50,y = 50)
url_f2_entry.place(x=400,y=50)

scrape_btn.place(x=100,y=350)
gen_xl_btn.place(x=500,y=350)
gen_senti_btn.place(x=270,y=450)

scrollbar = t.Scrollbar(f1)
scroll2 = t.Scrollbar(f1,orient='horizontal')
scroll2.pack( side = t.BOTTOM,fill = t.X)
scrollbar.pack( side = t.RIGHT, fill = t.Y )
mylist = t.Listbox(f1, yscrollcommand = scrollbar.set , xscrollcommand=scroll2.set,width= 50, height= 28,font=("Arial",12))

mylist.pack( side = t.LEFT, fill = t.BOTH )
scroll2.config( command=  mylist.xview)
scrollbar.config( command = mylist.yview )

l1.place(x=10,y=10)
info_btn.place(x=1300,y=20)
help_btn.place(x=1300,y=80)
title.place(x=500,y=50)
f1.place(x=1000,y=200)
f2.place(x=50,y=200)
win.mainloop()