import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
import pandas as pd
from tkinter import*
import tkinter.messagebox
from tkinter import ttk
import time
import datetime
from PIL import ImageTk, Image
import pymysql
import MySQLdb
import warnings
import face_recognition_api
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
from random import shuffle
from sklearn import svm, neighbors
from datetime import date
    
window1 = tk.Tk()
window1.title("attendance management system")
window1.geometry('1350x750+0+0') 
       
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap('AMS.ico')
    sb.title("Enter subject name...")
    sb.geometry('580x320')
    sb.configure(background='snow')

    def err_screen_for_subject():

        def ec_delete():
            ec.destroy()
        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        ec.iconbitmap('AMS.ico')
        ec.title('Warning!!')
        ec.configure(background='snow')
        Label(ec, text='Please enter your subject name!!!', fg='red', bg='white', font=('times', 16, ' bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="black", bg="lawn green", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        ####Creatting csv of attendance

        ##Create table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        global subb
        subb=SUB_ENTRY.get()
        DB_table_name = str(subb + "_" + Date + "_Time_" + Hour + "_" + Minute + "_" + Second)

        import pymysql.connections

        ###Connect to the database
        try:
            global cursor
            connection = pymysql.connect(host='localhost', user='root', password='', db='manual')
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        sql = "CREATE TABLE " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                         ENROLLMENT varchar(100) NOT NULL,
                         NAME VARCHAR(50) NOT NULL,
                         DATE VARCHAR(20) NOT NULL,
                         TIME VARCHAR(20) NOT NULL,
                             PRIMARY KEY (ID)
                             );
                        """


        try:
            cursor.execute(sql)  ##for create a table
        except Exception as ex:
            print(ex)  #

        if subb=='':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap('AMS.ico')
            MFW.title("Manually attendance of "+ str(subb))
            MFW.geometry('880x470')
            MFW.configure(background='snow')

            def del_errsc2():
                errsc2.destroy()
            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                errsc2.iconbitmap('AMS.ico')
                errsc2.title('Warning!!')
                errsc2.configure(background='snow')
                Label(errsc2, text='Please enter Student & Enrollment!!!', fg='red', bg='white',
                      font=('times', 16, ' bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="black", bg="lawn green", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="white", bg="blue2",
                           font=('times', 15, ' bold '))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Student name", width=15, height=2, fg="white", bg="blue2",
                                font=('times', 15, ' bold '))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20,validate='key', bg="yellow", fg="red", font=('times', 23, ' bold '))
            ENR_ENTRY['validatecommand'] = (ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)
            
            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            ####get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT=='':
                    err_screen1()
                elif STUDENT=='':
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + DB_table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLLMENT), str(STUDENT), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

            def create_csv():
                import csv
                cursor.execute("select * from " + DB_table_name + ";")
                csv_name='D:/project/dev/Attendance/Manually Attendance/'+DB_table_name+'.csv'
                with open(csv_name, "w") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([i[0] for i in cursor.description])  # write headers
                    csv_writer.writerows(cursor)
                    O="CSV created Successfully"
                    Notifi.configure(text=O, bg="Green", fg="white", width=33, font=('times', 19, 'bold'))
                    Notifi.place(x=180, y=380)
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + subb)
                root.configure(background='snow')
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=13, height=1, fg="black", font=('times', 13, ' bold '),
                                                  bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="Green", fg="white", width=33,
                                height=2, font=('times', 19, 'bold'))


            c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="black", bg="deep pink", width=10,
                                     height=1,
                                     activebackground="Red", font=('times', 15, ' bold '))
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="black", bg="deep pink", width=10,
                                      height=1,
                                      activebackground="Red", font=('times', 15, ' bold '))
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(MFW, text="Enter Data",command=enter_data_DB, fg="black", bg="lime green", width=20,
                                 height=2,
                                 activebackground="Red", font=('times', 15, ' bold '))
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(MFW, text="Convert to CSV",command=create_csv, fg="black", bg="red", width=20,
                                 height=2,
                                 activebackground="Red", font=('times', 15, ' bold '))
            MAKE_CSV.place(x=570, y=300)

            def attf():
                import subprocess
                subprocess.Popen(r'explorer /select,"D:\project\dev\Attendance\Manually Attendance\-------Check atttendance-------"')

            attf = tk.Button(MFW,  text="Check Sheets",command=attf,fg="black"  ,bg="lawn green"  ,width=12  ,height=1 ,activebackground = "Red" ,font=('times', 14, ' bold '))
            attf.place(x=730, y=410)

            MFW.mainloop()


    SUB = tk.Label(sb, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
    SUB.place(x=30, y=100)
    


    global SUB_ENTRY

    SUB_ENTRY = tk.Entry(sb, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance",command=fill_attendance, fg="white", bg="deep pink", width=20, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()

##For clear textbox
def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)
def del_sc1():
    sc1.destroy()
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='snow')
    Label(sc1,text='Enrollment & Name required!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc1,text='OK',command=del_sc1,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

##Error screen2
def del_sc2():
    sc2.destroy()
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)
######################################IMAGE CAPTURING#################################################################################
def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()            
    else:
        try:
            
            cam = cv2.VideoCapture(0)
            Enrollment = txt.get()
            Name = txt2.get()
            c=txt2.get()+"."+txt.get()
            user_input= "training-images"
            path = user_input
            if not os.path.exists(path):
                os.makedirs(path)
            path = Name
            
            if not os.path.exists(os.path.join(user_input, c)):
                os.makedirs(os.path.join(user_input, c))
            cv2.namedWindow("test")

            sampleNum = 0

            while True:
                ret, frame = cam.read()
                cv2.imshow("test", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)

                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k%256 == 32:
                    # SPACE pressed
                    
                    
                    img_name = ( str(sampleNum) +".png")
                    path = 'D:/project/dev/training-images'
                    new_file_path = os.path.join(path,c)
                    
                    cv2.imwrite(os.path.join(new_file_path,img_name),frame)
                    print("{} written!".format(img_name))
                    sampleNum += 1
                elif sampleNum > 10:
                    break    
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)


#############################################3for choose batch and  subject and fill attendance##########################################
def subjectchoose():
    def Fillattendances():
        sub=tx.get()
        
        if sub == '':
            err_screen1()
        else:
            df = pd.read_csv("StudentDetails\StudentDetails.csv")
            video_capture = cv2.VideoCapture(0)
            fname = 'classifier.pkl'
            if os.path.isfile(fname):
                with open(fname, 'rb') as f:
                    (le, clf) = pickle.load(f)
            else:
                print('\x1b[0;37;43m' + "Classifier '{}' does not exist".format(fname) + '\x1b[0m')
                quit()

            # Initialize some variables
            face_locations = []
            face_encodings = []
            face_names = []
            
            process_this_frame = True
            col_names = ['Enrollment', 'Name', 'Date', 'Time']
            attendance = pd.DataFrame(columns=col_names)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                while True:
                    # Grab a single frame of video
                    ret, frame = video_capture.read()

                    # Resize frame of video to 1/4 size for faster face recognition processing
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    
                    # Only process every other frame of video to save time
                    if process_this_frame:
                        # Find all the faces and face encodings in the current frame of video
                        face_locations = face_recognition_api.face_locations(small_frame)
                        face_encodings = face_recognition_api.face_encodings(small_frame, face_locations)

                        face_names = []
                        predictions = []
                        global Id
                        
                        if len(face_encodings) > 0:
                            closest_distances = clf.kneighbors(face_encodings, n_neighbors=1)

                            is_recognized = [closest_distances[0][i][0] <= 0.5 for i in range(len(face_locations))]
                             
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            
                            # predict classes and cull classifications that are not with high confidence
                            predictions = [(le.inverse_transform(int(pred)).title(), loc) if rec else ("Unknown.person", loc) for pred, loc, rec in
                                           zip(clf.predict(face_encodings), face_locations, is_recognized)]

                        # # Predict the unknown faces in the video frame
                        # for face_encoding in face_encodings:
                        #     face_encoding = face_encoding.reshape(1, -1)
                        #
                        #     # predictions = clf.predict(face_encoding).ravel()
                        #     # person = le.inverse_transform(int(predictions[0]))
                        #
                        #     predictions = clf.predict_proba(face_encoding).ravel()
                        #     maxI = np.argmax(predictions)
                        #     person = le.inverse_transform(maxI)
                        #     confidence = predictions[maxI]
                        #     print(person, confidence)
                        #     if confidence < 0.7:
                        #         person = 'Unknown'
                        #
                        #     face_names.append(person.title())

                    process_this_frame = not process_this_frame

                    reg = 0
                    Name = 0
                    # Display the results
                    for name, (top, right, bottom, left) in predictions:
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4
                        
                        
                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        #while name!='Unknown':
                             
                        
                        # Draw a label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        
                    
                        reg = os.path.split(name)[-1].split(".")[1]
                            
                        Name = os.path.split(name)[-1].split(".")[0]
                        attendance.loc[len(attendance)] = [reg, Name, date, timeStamp]                              
                    # Display the resulting image
                    cv2.imshow('Video', frame)
                    
                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                    
                    #attendance = attendance[attendance.Enrollment == 'person']
                    
                    # Hit 'q' on the keyboard to quit!
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                video_capture.release()
                   
                # Release handle to the webcam
            Batch = ty.get()  
            Subject = tx.get()
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance/" + Batch + "_" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
            attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
            #attendance = attendance[attendance.Enrollment == 'person']
            print(attendance)
            attendance.to_csv(fileName, index=False)

            ##Create table for Attendance
            date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
            DB_Table_name = str(Batch +"_"+ Subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
            import pymysql.connections

            ###Connect to the database
            try:
                global cursor
                connection = pymysql.connect(host='localhost', user='root', password='', db='automatic')
                cursor = connection.cursor()
            except Exception as e:
                print(e)

            sql = "CREATE TABLE " + DB_Table_name + """
            (ID INT NOT NULL AUTO_INCREMENT,
             ENROLLMENT varchar(100) NOT NULL,
             NAME VARCHAR(50) NOT NULL,
             DATE VARCHAR(20) NOT NULL,
             TIME VARCHAR(20) NOT NULL,
                 PRIMARY KEY (ID)
                 );
            """
            ####Now enter attendance in Database
            insert_data =  "INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
            VALUES = (str(reg), str(Name), str(date), str(timeStamp))
            try:
                cursor.execute(sql)  ##for create a table
                cursor.execute(insert_data, VALUES)##For insert data into table
            except Exception as ex:
                print(ex)  #

            M = 'Attendance filled Successfully'
            Notifica.configure(text=M, bg="Green", fg="white", width=33, font=('times', 15, 'bold'))
            Notifica.place(x=20, y=250)

            VideoCapture.release()
            cv2.destroyAllWindows()

            import csv
            import tkinter
            root = tkinter.Tk()
            root.title("Attendance of " + Subject)
            root.configure(background='snow')
            cs = 'D:/project/dev/Attendace managemnt system/' + fileName
            with open(cs, newline="") as file:
                reader = csv.reader(file)
                r = 0

                for col in reader:
                    c = 0
                    for row in col:
                        # i've added some styling
                        label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                              bg="lawn green", text=row, relief=tkinter.RIDGE)
                        label.grid(row=r, column=c)
                        c += 1
                    r += 1
            root.mainloop()
            print(attendance)

    ###windo is frame for subject chooser
    windo = tk.Tk()
    windo.iconbitmap('AMS.ico')
    windo.title("Enter Details...")
    windo.geometry('580x550')
    windo.configure(background='snow')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('times', 15, 'bold'))

    def Attf():
        import subprocess
        subprocess.Popen(r'explorer /select,"D:\project\dev\Attendance\-------Check atttendance-------"')

    attf = tk.Button(windo,  text="Check Sheets",command=Attf,fg="black"  ,bg="lawn green"  ,width=12  ,height=1 ,activebackground = "Red" ,font=('times', 14, ' bold '))
    attf.place(x=430, y=255)

    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)
    batch = tk.Label(windo, text="Enter Batch", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
    batch.place(x=30, y=190)

    tx = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    tx.place(x=250, y=105)
    ty = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    ty.place(x=250, y=185)
    fill_a = tk.Button(windo, text="Take Attendance", fg="white",command=Fillattendances, bg="deep pink", width=20, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=300)
    windo.mainloop()

def admin_panel():
    win = tk.Tk()
    win.iconbitmap('AMS.ico')
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='snow')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'admin' :
            if password == 'admin1234':
                win.destroy()
                
                new = tk.Tk()
                new.iconbitmap('AMS.ico')
                new.title("Add Faculty")
                new.geometry('880x420')
                new.configure(background='snow')
                global usx
                global pdx
                global namex
                name = tk.Label(new,text="Enter Faculty name", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
                name.place(x=30, y=80)
                us = tk.Label(new, text="Enter username", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
                us.place(x=30, y=150)

                pd = tk.Label(new, text="Enter password", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
                pd.place(x=30, y=220)
                namex = tk.Entry(new, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
                namex.place(x=250, y=80)
                usx = tk.Entry(new, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
                usx.place(x=250, y=150)
                pdx = tk.Entry(new, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
                pdx.place(x=250, y=220)
                Login = tk.Button(new, text="Submit", fg="black", bg="lime green", width=20,height=2,activebackground="Red",command=subt, font=('times', 15, ' bold '))
                Login.place(x=290, y=300)
                
                new.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)

        else:
            valid ='Incorrect ID or Password'
            Nt.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)


    Nt = tk.Label(win, text="Attendance filled Successfully", bg="Green", fg="white", width=40,
                  height=2, font=('times', 19, 'bold'))
    # Nt.place(x=120, y=350)
    tx=tk.Label(win, text="Admin login portal",  fg="red",
                   font=('italic', 16, ' bold '))
    tx.place(x=300, y=10)
    un = tk.Label(win, text="Enter username", width=15, height=2, fg="white", bg="blue2",
                   font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password", width=15, height=2, fg="white", bg="blue2",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)
    
    def subt():
                
        import pymysql.connections

        ###Connect to the database
        try:
            global cursor
            connection = pymysql.connect(host='localhost', user='root', password='', db='attendance')
            cursor = connection.cursor()
        except Exception as e:
            print(e)
        name=namex.get()
        us=usx.get()
        pd=pdx.get()
        ####Now enter attendance in Database
        insert_data =  "INSERT INTO login (name,user,pwd) VALUES ( %s, %s, %s)"
        VALUES = (str(name), str(us), str(pd))
        try:
           
            cursor.execute(insert_data, VALUES)##For insert data into table
        except Exception as ex:
            print(ex)  #
        Nt = tk.Label(new, text="Attendance filled Successfully", bg="Green", fg="white", width=40,height=2, font=('times', 19, 'bold'))
        Nt.place(x=120, y=380)
    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20,show="*", bg="yellow", fg="red", font=('times', 23, ' bold '))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="deep pink", width=10, height=1,
                            activebackground="Red", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=c11, fg="black", bg="deep pink", width=10, height=1,
                   activebackground="Red", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="lime green", width=20,
                       height=2,
                       activebackground="Red",command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()


###################################################For train the model#############################################################
def trainimg():
    def _get_training_dirs(training_dir_path):
        return [x[0] for x in os.walk(training_dir_path)][1:]


    def _get_training_labels(training_dir_path):
        return [x[1] for x in os.walk(training_dir_path)][0]


    def _get_each_labels_files(training_dir_path):
        return [x[2] for x in os.walk(training_dir_path)][1:]


    def _filter_image_files(training_dir_path):
        exts = [".jpg", ".jpeg", ".png"]

        training_folder_files_list = []
        #folder with name and id of people
        for list_files in _get_each_labels_files(training_dir_path):
            l = [] #images
            
            for file in list_files:
                imageName, ext = os.path.splitext(file)
                if ext.lower() in exts:
                    l.append(file)
                    
            training_folder_files_list.append(l)
        
        return training_folder_files_list
        


    def _zipped_folders_labels_images(training_dir_path, labels):
        return list(zip(_get_training_dirs(training_dir_path),
                        labels,
                        _filter_image_files(training_dir_path)))


    def create_dataset(training_dir_path, labels):
        X = []
        for i in _zipped_folders_labels_images(training_dir_path, labels):
            for fileName in i[2]:
                file_path = os.path.join(i[0], fileName)
                img = face_recognition_api.load_image_file(file_path)
                imgEncoding = face_recognition_api.face_encodings(img)

                if len(imgEncoding) > 1:
                    print('\x1b[0;37;43m' + 'More than one face found in {}. Only considering the first face.'.format(file_path) + '\x1b[0m')
                if len(imgEncoding) == 0:
                    print('\x1b[0;37;41m' + 'No face found in {}. Ignoring file.'.format(file_path) + '\x1b[0m')
                else:
                    print('Encoded {} successfully.'.format(file_path))
                    X.append(np.append(imgEncoding[0], i[1]))
        return X

    encoding_file_path = './encoded-images-data.csv'
    training_dir_path = './training-images/'
    labels_fName = "labels.pkl"

    # Get the folder names in training-dir as labels
    # Encode them in numerical form for machine learning
    labels = _get_training_labels(training_dir_path)
    le = LabelEncoder().fit(labels)
    labelsNum = le.transform(labels)
    nClasses = len(le.classes_)
    dataset = create_dataset(training_dir_path, labelsNum)
    df = pd.DataFrame(dataset)

    # if file with same name already exists, backup the old file
    if os.path.isfile(encoding_file_path):
        print("{} already exists. Backing up.".format(encoding_file_path))
        os.rename(encoding_file_path, "{}.bak".format(encoding_file_path))

    df.to_csv(encoding_file_path)

    print("{} classes created.".format(nClasses))
    print('\x1b[6;30;42m' + "Saving labels pickle to'{}'".format(labels_fName) + '\x1b[0m')
    with open(labels_fName, 'wb') as f:
        pickle.dump(le, f)
    print('\x1b[6;30;42m' + "Training Image's encodings saved in {}".format(encoding_file_path) + '\x1b[0m')
    encoding_file_path = './encoded-images-data.csv'
    labels_fName = 'labels.pkl'

    if os.path.isfile(encoding_file_path):
        df = pd.read_csv(encoding_file_path)
    else:
        print('\x1b[0;37;41m' + '{} does not exist'.format(encoding_file_path) + '\x1b[0m')
        quit()

    if os.path.isfile(labels_fName):
        with open(labels_fName, 'rb') as f:
            le = pickle.load(f)
    else:
        print('\x1b[0;37;41m' + '{} does not exist'.format(labels_fName) + '\x1b[0m')
        quit()

    # Read the dataframe into a numpy array
    # shuffle the dataset
    full_data = np.array(df.astype(float).values.tolist())
    shuffle(full_data)

    # Extract features and labels
    # remove id column (0th column)
    X = np.array(full_data[:, 1:-1])
    y = np.array(full_data[:, -1:])

    # fit the data into a support vector machine
    # clf = svm.SVC(C=1, kernel='linear', probability=True)
    clf = neighbors.KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree', weights='distance')
    clf.fit(X, y.ravel())


    fName = "./classifier.pkl"
    # if file with same name already exists, backup the old file
    if os.path.isfile(fName):
        print('\x1b[0;37;43m' + "{} already exists. Backing up.".format(fName) + '\x1b[0m')
        os.rename(fName, "{}.bak".format(fName))

    # save the classifier pickle
    with open(fName, 'wb') as f:
        pickle.dump((le, clf), f)
    print('\x1b[6;30;42m' + "Saving classifier to '{}'".format(fName) + '\x1b[0m')


    
    res = "Model Trained"  # +",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)




global tv_username
global tv_pass

image = Image.open("login.png")
img_copy= image.copy()
background_image = ImageTk.PhotoImage(image)
background = Label(window1, image=background_image)    
background.pack()
lb_username = tk.Label(window1, text="USERNAME : ",width=12, height=2, fg="blue", bg="white", font=('times', 12, ' bold '))
lb_username.place(x=40, y=200)
tv_username = tk.Entry(window1,width=30,font=('times', 16, ' bold '))
tv_username.place(x=200, y=200)

lb_pass = tk.Label(window1, text="PASSWORD : ",width=12, height=2, fg="blue", bg="white", font=('times', 12, ' bold '))
lb_pass.place(x=40 , y=300 )
tv_pass = tk.Entry(window1, show="*",width=30,font=('times', 16, ' bold '))
tv_pass.place(x=200, y=300 )
btnLogin = Button(window1, text = 'Login', background = "blue", fg = "white",width =17,command=checkLogin())
btnLogin.pack(fill = BOTH, expand= True)   
     
def checkLogin():
   
    win.destroy()
       
    
          

def  first():
    global txt
    global txt2
    global Notification
    new=tk.Tk()
    new.title("attendance management system")
    new.geometry('1350x750+0+0')
    new.config(bg='light blue')    
    message = tk.Label(new, text="Smart-Attendance-Management-System", bg="cyan", fg="black", width=50,
               height=3, font=('times', 30, 'italic bold'))

    message.place(x=80, y=20)
    Notification = tk.Label(new, text="All things good", bg="Green", fg="white", font=('times', 17, 'bold'))

    lbl = tk.Label(new, text="Enter RegisterNo", width=20, height=2, fg="white", bg="deep pink", font=('times', 15, ' bold '))
    lbl.place(x=150, y=200)
    photo = PhotoImage(file =r"logout.png") 
    photoimage = photo.subsample(3, 3) 
    Button(new, text = 'Click Me !', image = photoimage, 
                compound = LEFT,width=155, height=55).pack(side = TOP) 
                
    txt = tk.Entry(new, validate="key", width=20, bg="white", fg="black", font=('times', 16, ' bold '))

    txt.place(x=500, y=210)

    new.lbl2 = tk.Label(new, text="Enter Name", width=20, fg="black", bg="deep pink", height=2, font=('times', 15, ' bold '))
    new.lbl2.place(x=150, y=300)

    txt2 = tk.Entry(new, width=20, bg="white", fg="black", font=('times', 16, ' bold '))
    txt2.place(x=500, y=310)
    clearButton = tk.Button(new, text="Clear",fg="black"  ,bg="deep pink"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton.place(x=800, y=210)

    clearButton1 = tk.Button(new, text="Clear",fg="black"  ,bg="deep pink"  ,width=10 ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton1.place(x=800, y=310)

    AP = tk.Button(new, text="Add new faculty",fg="black" ,command=admin_panel ,bg="cyan"  ,width=19 ,height=1 ,font=('times', 15, ' bold '))
    AP.place(x=990, y=410)

    takeImg = tk.Button(new, text="Take Images",fg="black",command=take_img ,bg="blue2"  ,width=20  ,height=3,font=('times', 15, ' bold '))
    takeImg.place(x=90, y=500)

    trainImg = tk.Button(new, text="Train Images",fg="black",command=trainimg ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    trainImg.place(x=390, y=500)

    FA = tk.Button(new, text="Automatic Attendace",fg="white",command=subjectchoose  ,bg="blue2"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    FA.place(x=690, y=500)

    quitWindow = tk.Button(new, text="Manually Fill Attendance", command=manually_fill  ,fg="black"  ,bg="lawn green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    quitWindow.place(x=990, y=500)


window1.mainloop()