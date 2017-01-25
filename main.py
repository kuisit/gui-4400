import pymysql
import sys 
from Tkinter import *
import tkMessageBox
import ttk
import datetime
from functools import partial

class main:

    # self.win = rootWin
    # self.win.geometry("500x500")
    # frame = Frame(rootWin)

    def __init__(self, rootWin):
        self.rootWin = rootWin
        self.win = rootWin
        self.win.geometry("500x500")
        frame = Frame(rootWin)
        self.LoginPage()

    def Connect(self):
        try:
            self.db = pymysql.connect(host = 'academic-mysql.cc.gatech.edu',
            passwd ='jaPcMkDn', user = 'cs4400_Team_83', db='cs4400_Team_83')
            self.cursor = self.db.cursor()
        except:
            raise 
            messagebox.showwarning('Error!','Check your Internet Connection ')

    def LoginPage(self) :
        self.logPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.logPage

        # self.win = rootWin
        self.win.geometry("500x500")
        frame = Frame(self.logPage)

        self.title = Label(self.logPage, text="Login", font=("Arial", 20), fg="gold3")
        self.title.grid(row=0, column=1)

        self.usernameLabel = Label(self.logPage, text="Username")
        self.usernameLabel.grid(row=1, column=0)
        self.usernameEntry = Entry(self.logPage)
        self.usernameEntry.grid(row=1, column=1)

        self.passwordLabel = Label(self.logPage, text="Password")
        self.passwordLabel.grid(row=2, column=0)
        self.passwordEntry = Entry(self.logPage)
        self.passwordEntry.grid(row=2, column=1)

        self.login = Button(self.logPage, text="Login", command=self.checkLogin)
        self.login.grid(row=3, column=1, sticky=W)

        self.register = Button(self.logPage, text="Register", command=self.RegisterPage)
        self.register.grid(row=3, column=1, sticky=E)
    
    def checkLogin(self):
        self.userName = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        print("user: ", self.userName)
        print("password: ", self.password)
        self.Connect()
        self.sql = 'SELECT * FROM USER WHERE Username=(%s) AND Password=(%s)'
        self.validUser = True
        try:
            self.cursor.execute(self.sql,(self.userName, self.password))
            info=self.cursor.fetchone()
            # self.validUser == True
            # if info[0] == None:
            #     tkMessageBox.showwarning("Sorry! You're account is not registered. Please register")
            #     self.validUser = False
            if not info == None:
                self.flag =  info[2]
                self.username = info[0]
                # self.win.withdraw()
                if self.flag:
                    self.Connect()
                    self.sql = 'SELECT Major FROM STUDENT WHERE Username=(%s)'
                    self.cursor.execute(self.sql,(self.userName))
                    self.majorUser = self.cursor.fetchone()
                    self.MainPage()
                else:
                    self.ChooseFunctionalityPage()
                
            else:
                tkMessageBox.showwarning("Sorry! You're account is not register. Please register")
        except:
            raise
            print("went to except")
    
    def RegisterPage(self):
        
        self.registerPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.registerPage
        
        # self.win = rootWin
        self.win.geometry("500x500")
        frame = Frame(self.registerPage)

        self.title = Label(self.registerPage, text="New Student Registration", font=("Arial", 20), fg="gold3")
        self.title.grid(row=0, column=1)

        self.usernameLabel = Label(self.registerPage, text="Username")
        self.usernameLabel.grid(row=1, column=0)
        self.usernameEntry = Entry(self.registerPage)
        self.usernameEntry.grid(row=1, column=1)

        self.emailLabel = Label(self.registerPage, text="GT Email Address")
        self.emailLabel.grid(row=2, column=0)
        self.emailEntry = Entry(self.registerPage)
        self.emailEntry.grid(row=2, column=1)

        self.passwordLabel = Label(self.registerPage, text="Password")
        self.passwordLabel.grid(row=3, column=0)
        self.passwordEntry = Entry(self.registerPage)
        self.passwordEntry.grid(row=3, column=1)

        self.confirmPasswordLabel = Label(self.registerPage, text="Confirm Password")
        self.confirmPasswordLabel.grid(row=4, column=0)
        self.confirmPasswordEntry = Entry(self.registerPage)
        self.confirmPasswordEntry.grid(row=4, column=1)

        self.create = Button(self.registerPage, text="Create", command=self.register)
        self.create.grid(row=5, column=1)

    def register(self):
        self.Connect()
        self.sql = 'SELECT Username, GTEmail from STUDENT'
        self.cursor.execute(self.sql)
        information = self.cursor.fetchall()
        self.db.close()

        self.username = self.usernameEntry.get()
        self.email = self.emailEntry.get()
        self.password = self.passwordEntry.get()
        self.confirmPassword = self.confirmPasswordEntry.get()

        if self.username == "" or self.email == "" or self.password == "" or self.confirmPassword == "":
            tkMessageBox.showwarning('Error!', 'Cannot have empty field')
        elif self.password != self.confirmPassword:
            tkMessageBox.showwarning('Error!', 'Passwords do not match')
        elif '@gatech.edu' not in self.email:
            tkMessageBox.showwarning('Error!', ' Enter a valid GT email')
        else:
            noError = True
            for info in information:
                if self.username in info:
                    tkMessageBox.showwarning('Error!', 'Username already exists')
                    noError = False
                if self.email in info:
                    tkMessageBox.showwarning('Error!', 'Email already exists')
                    noError = False

            if noError:
                self.Connect()
                self.flag = 1.0
                self.sql = 'INSERT INTO USER(Username, Password, StudentFlag) VALUES(%s, %s, 1)'
                self.cursor.execute(self.sql, (self.username, self.password))
                self.sql = 'INSERT INTO STUDENT(Username, Password, Year, GTemail, Major) VALUES(%s, %s, %s, %s, %s)'
                self.cursor.execute(self.sql, (self.username, self.password, "Freshman", self.email, None))
                self.db.commit()
                self.db.close()
                tkMessageBox.showwarning('Successful Registration', "You have now registered!")

    
    
    def EditProfile(self):
        self.editPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.editPage

        self.win.geometry("500x500")
        frame = Frame(self.editPage)

        self.title = Label(self.editPage, text="Edit Profile", font=("Arial", 20), fg="gold3")
        self.title.grid(row=15, column=250)

        self.usernameLabel = Label(self.editPage, text="Major: ")
        self.usernameLabel.grid(row=16, column=0)
#########################################################################     
        #DROP DOWN Menu    
       
        self.Connect()
        self.sql = 'SELECT Majorname FROM MAJOR'
        majorOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            majorOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!, Check your Internet Connection ')
        
        
        self.sql = 'SELECT Major FROM STUDENT Where Username=%s'
        self.cursor.execute(self.sql,(self.username))
        self.majorUser = self.cursor.fetchone()

        
        self.var = StringVar(self.editPage)
       
        
        # set this to whatever user's major is' 
        self.var.set(self.majorUser) # initial value
        self.department = ""
        w = OptionMenu(self.editPage, self.var, *majorOptions, command= self.updateDepartment)
        
        w.pack()

        w.grid(row=16, column=1)

#########################################################################
        
        self.sql = 'SELECT Year FROM STUDENT Where Username=%s'
        self.cursor.execute(self.sql,(self.username))
        self.year = self.cursor.fetchone()
 
        self.yearLabel = Label(self.editPage, text="Year")
        self.yearLabel.grid(row=17, column=0)
        self.var2 = StringVar(self.editPage)
        self.var2.set(self.year)
        yearOptions = ["Freshmen", "Sophomore", "Junior", "Senior"]
       
      
        year = OptionMenu(self.editPage, self.var2, *yearOptions, command= self.updateYear)
        year.pack()
        year.grid(row=17, column=1)
       
########################################################################
        self.departmentLabel = Label(self.editPage, text="Department")
        self.departmentLabel.grid(row=18, column=0)
      
        
        self.sql = "SELECT Department FROM MAJOR WHERE Majorname=%s"
        department = ""
        try:
            self.cursor.execute(self.sql,(self.majorUser))
            info = self.cursor.fetchone()
            department = info
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')
        
        self.departmentEntry = Label(self.editPage, text= department)
        self.departmentEntry.grid(row=18, column=1)

        self.back = Button(self.editPage, text="Back", command=self.MePage)
        self.back.grid(row=19, column=250, sticky=W)

    def updateYear(self, value):
        self.sql = 'UPDATE STUDENT SET Year=%s WHERE Username=%s'
        self.cursor.execute(self.sql, (value,self.username))
        self.db.commit()
    
    def updateDepartment(self, value):
        self.departmentEntry.grid_remove()
        print("it made it")
        print("value: ", value )
        self.departmentLabel = Label(self.win, text="Department")
        self.departmentLabel.grid(row=18, column=0)
        self.sql = "SELECT Department FROM MAJOR WHERE Majorname=%s"
        try:
            self.cursor.execute(self.sql,(value))
            info = self.cursor.fetchone()
            self.department = info
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ') 
        departmentUpdated = True
        print("department: ", self.department)
        self.departmentEntry = Label(self.win, text= self.department)
        self.departmentEntry.grid(row=18, column=1)
        
        self.sql = 'UPDATE STUDENT SET Major=%s WHERE Username=%s'
        self.cursor.execute(self.sql, (value,self.username))
        
        self.db.commit()

    
    def MainPage(self):
        self.mainPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.mainPage
        
        self.win.geometry("700x800")
        frame = Frame(self.mainPage)

        self.title = Label(self.mainPage, text="Main Page", font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=180)

        self.me = Button(self.mainPage, text="ME", command=self.MePage)
        self.me.place(y=10, x=40)

        self.nameLabel = Label(self.mainPage, text="Title:")
        self.nameLabel.place(y=60, x=70)
        self.nameEntry = Entry(self.mainPage, width=50)
        self.nameEntry.place(y=60, x=150)

        self.categoryLabel = Label(self.mainPage, text="Category: ")
        self.categoryLabel.place(y=90, x=70)
        self.categoryEntry = []
        # self.categoryEntry.append(OptionMenu(rootWin, width=50))

        self.Connect()
        self.sql = 'SELECT Categoryname FROM CATEGORY'
        categoryOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            categoryOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.categoryVar = []
        self.categoriesMain = 0
        self.categoryVar.append(StringVar())
        self.categoryEntry.append(OptionMenu(self.mainPage, self.categoryVar[self.categoriesMain], *categoryOptions))
        self.categoryEntry[self.categoriesMain].place(y=90, x=150)

        self.addButton = Button(self.mainPage, text="Add Category", command=self.addCategoryMain)
        self.addButton.place(y=160, x=70)

        # self.coursenumberLabel = Label(rootWin, text="Course Number: ")
        # self.coursenumberLabel.place(y=90, x=60)
        # self.coursenumberEntry = Entry(rootWin, width=50)
        # self.coursenumberEntry.place(y=90, x=150)

        # self.instructorLabel = Label(rootWin, text="Instructor: ")
        # self.instructorLabel.place(y=120, x=70)
        # self.instructorEntry = Entry(rootWin, width=50)
        # self.instructorEntry.place(y=120, x=150)

        self.Connect()
        self.sql = 'SELECT Designationname FROM DESIGNATION'
        designationOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            designationOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.designationLabel = Label(self.mainPage, text="Designation: ")
        self.designationLabel.place(y=190, x=70)
        self.designationVar = StringVar()
        self.designationEntry = OptionMenu(self.mainPage, self.designationVar, *designationOptions)
        self.designationEntry.place(y=190, x=150)

        self.Connect()
        self.sql = 'SELECT Majorname FROM MAJOR'
        majorOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            majorOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.majorLabel = Label(self.mainPage, text="Major: ")
        self.majorLabel.place(y=220, x=80)
        self.majorVar = StringVar()
        self.majorEntry = OptionMenu(self.mainPage, self.majorVar, *majorOptions)
        self.majorEntry.place(y=220, x=150)

        self.yearLabel = Label(self.mainPage, text="Year: ")
        self.yearLabel.place(y=250, x=85)
        self.yearVar = StringVar()
        self.yearEntry = OptionMenu(self.mainPage, self.yearVar, "freshman", "sophomore", "junior", "senior")
        self.yearEntry.place(y=250, x=150)

        # self.numStudentsLabel = Label(rootWin, text="Estimated # of Students: ")
        # self.numStudentsLabel.place(y=290, x=18)
        # self.numStudentsEntry = Entry(rootWin, width=50)
        # self.numStudentsEntry.place(y=290, x=150)

        self.selectOptionVar = StringVar()
        self.selectOption1 = Radiobutton(self.mainPage, text="Course", variable=self.selectOptionVar, value="COURSE")
        self.selectOption2 = Radiobutton(self.mainPage, text="Project", variable=self.selectOptionVar, value="PROJECT")
        self.selectOption3 = Radiobutton(self.mainPage, text="Both", variable=self.selectOptionVar, value="BOTH")
        self.selectOption1.place(y=290, x=120)
        self.selectOption2.place(y=290, x=210)
        self.selectOption3.place(y=290, x=290)
        # for item in ["one", "two", "three", "four"]:
        #     self.selectOption.insert(END, item)
        # self.selectOption.place(y=290, x=150)

        # self.deptReqLabel = Label(rootWin, text="Department Requirement: ")
        # self.deptReqLabel.place(y=460, x=10)
        # deptReqVar = StringVar()
        # self.deptReqEntry = OptionMenu(rootWin, deptReqVar, "Community", "Sustainable Communities")
        # self.deptReqEntry.place(y=460, x=150)

        self.applyfilterButton = Button(self.mainPage, text="Apply Filter", command=self.applyfilter)
        self.applyfilterButton.place(y=320, x=90)

        self.resetfilterButton = Button(self.mainPage, text="Reset Filter", command=self.resetfilter)
        self.resetfilterButton.place(y=320, x=230)

        self.tree = ttk.Treeview(self.win)
        self.treeScroll = ttk.Scrollbar(self.win)
        self.treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.tree.bind("<1>", self.onClick)
        self.tree["columns"] = ("Name", "Type")
        self.tree["show"] = "headings" 
        self.tree.column("Name", width=260)
        self.tree.column("Type", width=80)
        self.tree.heading("Name", text = "Name")
        self.tree.heading("Type", text = "Type")

        self.Connect()
        self.sql = 'SELECT Projectname from PROJECT ORDER BY Projectname DESC'
        self.cursor.execute(self.sql)
        projects = self.cursor.fetchall()
        
        # print("info: ", information)
        self.db.close()
        visited = []
        for project in projects:
            if project not in visited:
                self.tree.insert("", 0, values=(project[0], "Project"))
                visited.append(project)

        self.Connect()
        self.sql = 'SELECT Coursename from COURSE ORDER BY Coursename DESC'
        self.cursor.execute(self.sql)
        courses = self.cursor.fetchall()
        
        # print("info: ", information)
        self.db.close()
        visited = []
        for course in courses:
            if course not in visited:
                self.tree.insert("", 0, values=(course[0], "Course"))
                visited.append(course)

        self.tree.place(y=350, x = 90)
        self.treeScroll.place(y=350, x = 420)

        self.mainLogOutButton = Button(self.mainPage, text="Log out", command = self.LoginPage)
        self.mainLogOutButton.place(y= 590, x = 100)

    def onClick(self, event):
        self.item = self.tree.selection()
        self.clickedValue = self.tree.item(self.item,"value")
        if len(self.clickedValue) > 0:
            print("clicked value ", self.clickedValue)
            self.name = self.clickedValue[0]
            self.type = self.clickedValue[1]
            self.win.withdraw()
            if self.type == "Course":
                self.ViewCourse(self.name)
            else:
                self.ViewProject(self.name)

    def applyfilter(self):
        self.tree = ttk.Treeview(self.win)
        self.treeScroll = ttk.Scrollbar(self.win)
        self.treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.tree.bind("<1>", self.onClick)
        self.tree["columns"] = ("Name", "Type") 
        self.tree["show"] = "headings" 
        self.tree.column("Name", width=260)
        self.tree.column("Type", width=80)
        self.tree.heading("Name", text = "Name")
        self.tree.heading("Type", text = "Type")

        self.Connect()

        self.name = self.nameEntry.get()
        self.filter = self.selectOptionVar.get()
        print self.filter
        # self.sql = []
        # self.equality = []
        # filterProjectResult = []
        # filterCourseResult = []
        if self.filter == "PROJECT" and not self.name == "":
            self.sql = 'SELECT Projectname from PROJECT WHERE Projectname = %s'
            self.cursor.execute(self.sql, self.name)
            filterProjectResult = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            filterCourseResult = tuple((set(projects)).union(set(courses)))
        elif self.filter == "COURSE" and not self.name == "":
            self.sql = 'SELECT Coursename from COURSE WHERE Coursename = %s'
            self.cursor.execute(self.sql, self.name)
            filterCourseResult = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            filterProjectResult = tuple((set(projects)).union(set(courses)))
        elif self.filter == "BOTH" and not self.name == "":
            self.sql = 'SELECT Projectname from PROJECT WHERE Projectname = %s'
            self.cursor.execute(self.sql, self.name)
            filterProjectResult = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            filterProjectResult = tuple((set(filterProjectResult)).union(set(courses)))
            self.sql = 'SELECT Coursename from COURSE WHERE Coursename = %s'
            self.cursor.execute(self.sql, self.name)
            filterCourseResult = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            filterCourseResult = tuple((set(filterCourseResult)).union(set(projects)))
        else:
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            filterProjectResult = tuple((set(projects)).union(set(courses)))
            filterCourseResult = tuple((set(projects)).union(set(courses)))

        # categoryProjectResult = []
        # categoryCourseResult = []
        self.sql = 'SELECT Projectname from PROJECT'
        self.cursor.execute(self.sql)
        projects = self.cursor.fetchall()
        self.sql = 'SELECT Coursename from COURSE'
        self.cursor.execute(self.sql)
        courses = self.cursor.fetchall()
        categoryProjectResult = tuple((set(projects)).union(set(courses)))
        categoryCourseResult = tuple((set(projects)).union(set(courses)))
        for index in range(len(self.categoryEntry)):
            if not self.categoryVar[index].get() == "": 
                category = self.categoryVar[index].get()
                category = category[2: len(category) - 3]
                print category
                if self.filter == "PROJECT":
                    self.sql = 'SELECT Projectname from PROJECT_IS_CATEGORY WHERE Categoryname = %s'
                    self.cursor.execute(self.sql, category)
                    categoryProjectResult = (set(categoryProjectResult)).intersection(set(self.cursor.fetchall()))
                    # self.sql = 'SELECT Projectname from PROJECT'
                    # self.cursor.execute(self.sql)
                    # projects = self.cursor.fetchall()
                    # self.sql = 'SELECT Coursename from COURSE'
                    # self.cursor.execute(self.sql)
                    # courses = self.cursor.fetchall()
                    # categoryCourseResult = tuple((set(projects)).union(set(courses)))
                elif self.filter == "COURSE":
                    self.sql = 'SELECT Coursenumber from COURSE_IS_CATEGORY WHERE Categoryname = %s'
                    self.cursor.execute(self.sql, category)
                    categoryCourse = self.cursor.fetchall()
                    coursenameList = []
                    for course in categoryCourse:
                        self.sql = 'SELECT Coursename from COURSE WHERE Coursenumber = %s'
                        self.cursor.execute(self.sql, course)
                        coursename = self.cursor.fetchone()
                        coursenameList.append(coursename)
                    categoryCourseResult = (set(categoryCourseResult)).intersection(set(coursenameList))
                    # self.sql = 'SELECT Projectname from PROJECT'
                    # self.cursor.execute(self.sql)
                    # projects = self.cursor.fetchall()
                    # self.sql = 'SELECT Coursename from COURSE'
                    # self.cursor.execute(self.sql)
                    # courses = self.cursor.fetchall()
                    # categoryProjectResult = tuple((set(projects)).union(set(courses)))
                elif self.filter == "BOTH":
                    self.sql = 'SELECT Projectname from PROJECT_IS_CATEGORY WHERE Categoryname = %s'
                    self.cursor.execute(self.sql, category)
                    # categoryProject = self.cursor.fetchall()
                    categoryProjectResult = (set(categoryProjectResult)).intersection(set(self.cursor.fetchall()))
                    self.sql = 'SELECT Coursename from COURSE'
                    self.cursor.execute(self.sql)
                    courses = self.cursor.fetchall()
                    # categoryProjectResult = tuple((set(categoryProjectResult)).union(set(courses)))
                    self.sql = 'SELECT Coursenumber from COURSE_IS_CATEGORY WHERE Categoryname = %s'
                    self.cursor.execute(self.sql, category)
                    categoryCourse = self.cursor.fetchall()
                    coursenameList = []
                    for course in categoryCourse:
                        self.sql = 'SELECT Coursename from COURSE WHERE Coursenumber = %s'
                        self.cursor.execute(self.sql, course)
                        coursename = self.cursor.fetchone()
                        coursenameList.append(coursename)
                    categoryCourseResult = ((set(categoryCourseResult)).intersection(set(coursenameList))).union(set(categoryProjectResult))
                    categoryProjectResult = (set(categoryProjectResult)).union(set(categoryCourseResult))
                    # categoryCourseResult = coursenameList
                    # self.sql = 'SELECT Projectname from PROJECT'
                    # self.cursor.execute(self.sql)
                    # projects = self.cursor.fetchall()
                    # categoryCourseResult = tuple((set(categoryCourseResult)).union(set(projects)))
                # else:
                #     self.sql = 'SELECT Projectname from PROJECT'
                #     self.cursor.execute(self.sql)
                #     projects = self.cursor.fetchall()
                #     self.sql = 'SELECT Coursename from COURSE'
                #     self.cursor.execute(self.sql)
                #     courses = self.cursor.fetchall()
                #     categoryProjectResult = tuple((set(projects)).union(set(courses)))
                #     categoryCourseResult = tuple((set(projects)).union(set(courses)))
            # else:
            #     self.sql = 'SELECT Projectname from PROJECT'
            #     self.cursor.execute(self.sql)
            #     projects = self.cursor.fetchall()
            #     self.sql = 'SELECT Coursename from COURSE'
            #     self.cursor.execute(self.sql)
            #     courses = self.cursor.fetchall()
            #     categoryProjectResult = tuple((set(projects)).union(set(courses)))
            #     categoryCourseResult = tuple((set(projects)).union(set(courses)))


        self.designation = self.designationVar.get()
        self.designation = self.designation[2: len(self.designation) - 3]
        if self.filter == "PROJECT" and not self.designation == "":
            self.sql = 'SELECT Projectname from PROJECT WHERE Designation = %s'
            self.cursor.execute(self.sql, self.designation)
            designationProjectResult = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            designationCourseResult = tuple((set(projects)).union(set(courses)))
        elif self.filter == "COURSE" and not self.designation == "":
            self.sql = 'SELECT Coursename from COURSE WHERE Designation = %s'
            self.cursor.execute(self.sql, self.designation)
            designationCourseResult = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            designationProjectResult = tuple((set(projects)).union(set(courses)))
        elif self.filter == "BOTH" and not self.designation == "":
            self.sql = 'SELECT Projectname from PROJECT WHERE Designation = %s'
            self.cursor.execute(self.sql, self.designation)
            designationProjectResult = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            designationProjectResult = tuple((set(designationProjectResult)).union(set(courses)))
            self.sql = 'SELECT Coursename from COURSE WHERE Designation= %s'
            self.cursor.execute(self.sql, self.designation)
            designationCourseResult = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            designationCourseResult = tuple((set(designationCourseResult)).union(set(projects)))
        else: 
            # self.sql = 'SELECT Projectname from PROJECT'
            # self.cursor.execute(self.sql)
            # designationProjectResult = self.cursor.fetchall()
            # self.sql = 'SELECT Coursename from COURSE'
            # self.cursor.execute(self.sql)
            # designationCourseResult = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            designationProjectResult = tuple((set(projects)).union(set(courses)))
            designationCourseResult = tuple((set(projects)).union(set(courses)))
        self.major = self.majorVar.get()
        if self.filter == "PROJECT" and not self.major == "":
            self.sql = 'SELECT Department from MAJOR WHERE Majorname = %s'
            self.cursor.execute(self.sql, self.major[2: len(self.major) - 3])
            self.departmentMajor = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from REQUIREMENT WHERE Requirement = %s or Requirement = %s'
            # print(self.major[2: len(self.major) - 3] + 'students only')
            # print self.major[0]
            self.departmentMajor = self.departmentMajor[0][0]
            self.cursor.execute(self.sql, (self.major[2: len(self.major) - 3] + ' students only', self.departmentMajor + ' students only'))
            majorProjectResult = self.cursor.fetchall()
        elif self.filter == "BOTH" and not self.major == "":
        # self.sql = 'SELECT Department from MAJOR WHERE Majorname = %s'
        # self.cursor.execute(self.sql, self.major[2: len(self.major) - 3])
        # self.departmentMajor = self.cursor.fetchall()
            self.sql = 'SELECT Department from MAJOR WHERE Majorname = %s'
            self.cursor.execute(self.sql, self.major[2: len(self.major) - 3])
            self.departmentMajor = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from REQUIREMENT WHERE Requirement = %s or Requirement = %s'
            # print(self.major[2: len(self.major) - 3] + 'students only'
            self.departmentMajor = self.departmentMajor[0][0]
            self.cursor.execute(self.sql, (self.major[2: len(self.major) - 3] + ' students only', self.departmentMajor + ' students only'))
        # print(self.major[2: len(self.major) - 3] + 'students only')
        # print self.major[0]
        # print self.departmentMajor
            majorProjectResult = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            majorProjectResult = tuple((set(majorProjectResult)).union(set(courses)))
        elif self.filter == "PROJECT" and self.major == "":
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            majorProjectResult = projects
        elif self.filter == "BOTH" and self.major == "":
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            majorProjectResult = tuple((set(projects)).union(set(courses)))
        else:
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            majorProjectResult = courses

        self.year = self.yearVar.get()
        if self.filter == "PROJECT" and not self.year == "":
            self.sql = 'SELECT Projectname from REQUIREMENT WHERE Requirement = %s'
            self.cursor.execute(self.sql, self.year + " students only")
            yearProjectResult = self.cursor.fetchall()
        elif self.filter == "BOTH" and not self.year == "":
        # self.sql = 'SELECT Department from MAJOR WHERE Majorname = %s'
        # self.cursor.execute(self.sql, self.major[2: len(self.major) - 3])
        # self.departmentMajor = self.cursor.fetchall()
            self.sql = 'SELECT Projectname from REQUIREMENT WHERE Requirement = %s'
        # print(self.major[2: len(self.major) - 3] + 'students only')
        # print self.major[0]
        # print self.departmentMajor
            self.cursor.execute(self.sql, self.year + ' students only')
            yearProjectResult = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            yearProjectResult = tuple((set(yearProjectResult)).union(set(courses)))
        elif self.filter == "PROJECT" and self.year == "":
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            yearProjectResult = projects
        elif self.filter == "BOTH" and self.major == "":
            self.sql = 'SELECT Projectname from PROJECT'
            self.cursor.execute(self.sql)
            projects = self.cursor.fetchall()
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            yearProjectResult = tuple((set(projects)).union(set(courses)))
            # self.sql = 'SELECT Projectname from PROJECT'
            # self.cursor.execute(self.sql)
            # projects = self.cursor.fetchall()
            # self.sql = 'SELECT Coursename from COURSE'
            # self.cursor.execute(self.sql)
            # courses = self.cursor.fetchall()
        else:
            self.sql = 'SELECT Coursename from COURSE'
            self.cursor.execute(self.sql)
            courses = self.cursor.fetchall()
            yearProjectResult = courses

        # self.sqlTotal = ""
        # # print self.sql
        # for sqlStatement in self.sql:
        #     self.sqlTotal += sqlStatement + " UNION "
        # print ("FP:", filterProjectResult)
        # print ("FC:", filterCourseResult)
        # print ("CP:", categoryProjectResult)
        # print ("CC:", categoryCourseResult)
        # print ("DP:", designationProjectResult)
        # print ("DC:", designationCourseResult)
        # print ("MP:", majorProjectResult)
        # print ("YP:", yearProjectResult)
        result = (set(filterProjectResult)).intersection(set(filterCourseResult)).intersection(set(categoryProjectResult)).intersection(set(categoryCourseResult)).intersection(set(designationProjectResult)).intersection(set(designationCourseResult)).intersection(set(majorProjectResult)).intersection(set(yearProjectResult))
        # self.sqlTotal = self.sqlTotal[0: len(self.sqlTotal) - 7]
        # print tuple(self.equality)
        # self.cursor.execute(self.sql, tuple(self.equality))
        # result = self.cursor.fetchall()

        # self.name = self.nameEntry.get()
        # self.filter = self.selectOptionVar.get()
        # self.sql = []
        # self.equality = []
        # if self.filter == "PROJECT":
        #     self.sql.append('SELECT Projectname from PROJECT WHERE Projectname = %s')
        #     self.equality.append(self.name)
        # elif self.filter == "COURSE":
        #     self.sql.append('SELECT Coursename from COURSE WHERE Coursename = %s')
        #     self.equality.append(self.name)
        # else:
        #     self.sql.append('SELECT Projectname from PROJECT WHERE Projectname = %s')
        #     self.equality.append(self.name)
        #     self.sql.append('SELECT Coursename from COURSE WHERE Coursename = %s')
        #     self.equality.append(self.name)

        # for index in range(len(self.categoryEntry)):
        #     if not self.categoryVar[index].get() == "": 
        #         category = self.categoryVar[index].get()
        #         category = category[2: len(category) - 3]
        #         if self.filter == "PROJECT":
        #             self.sql.append('SELECT Projectname from PROJECT_IS_CATEGORY WHERE Projectname = %s')
        #             self.equality.append(category)
        #         elif self.filter == "COURSE":
        #             self.sql.append('SELECT Coursename from COURSE_IS_CATEGORY WHERE Coursename = %s')
        #             self.equality.append(category)
        #         else:
        #             self.sql.append('SELECT Projectname from PROJECT_IS_CATEGORY WHERE Projectname = %s')
        #             self.equality.append(category)
        #             self.sql.append('SELECT Coursename from COURSE_IS_CATEGORY WHERE Coursename = %s')
        #             self.equality.append(category)

        # self.designation = self.designationVar.get()
        # if self.filter == "PROJECT":
        #     self.sql.append('SELECT Projectname from PROJECT WHERE Designation = %s')
        #     self.equality.append(self.designation)
        # elif self.filter == "COURSE":
        #     self.sql.append('SELECT Coursename from COURSE WHERE Designation = %s')
        #     self.equality.append(self.designation)
        # else:
        #     self.sql.append('SELECT Projectname from PROJECT WHERE Designation = %s')
        #     self.equality.append(self.designation)
        #     self.sql.append('SELECT Coursename from COURSE WHERE Designation = %s')
        #     self.equality.append(self.designation)

        # self.major = self.majorVar.get()
        # if self.filter == "PROJECT" or self.filter == "BOTH":
        #     self.sql.append('SELECT Projectname from REQUIREMENT WHERE Requirement = %s')
        #     self.equality.append(self.major[2: len(self.major) - 3] + ' students only')
        # self.year = self.yearVar.get()
        # if self.filter == "PROJECT" or self.filter == "BOTH":
        #     self.sql.append('SELECT Projectname from REQUIREMENT WHERE Requirement = %s')
        #     self.equality.append(self.year + " students only")

        # self.sqlTotal = ""
        # # print self.sql
        # for sqlStatement in self.sql:
        #     self.sqlTotal += sqlStatement + " UNION "

        # self.sqlTotal = self.sqlTotal[0: len(self.sqlTotal) - 7]
        # print tuple(self.equality)
        # self.cursor.execute(self.sql, tuple(self.equality))
        # result = self.cursor.fetchall()
        # print(tuple(result))

        # self.tree = ttk.Treeview(self.win)
        # self.treeScroll = ttk.Scrollbar(self.win)
        # self.treeScroll.configure(command=self.tree.yview)
        # self.tree.configure(yscrollcommand=self.treeScroll.set)
        # self.tree.bind("<1>", self.onClick)
        # self.tree["columns"] = ("Name", "Type")
        # self.tree["show"] = "headings"  
        # self.tree.column("Name", width=260)
        # self.tree.column("Type", width=80)
        # self.tree.heading("Name", text = "Name")
        # self.tree.heading("Type", text = "Type")

        self.Connect()
        self.sql = 'SELECT Coursename from COURSE ORDER BY Coursename DESC'
        self.cursor.execute(self.sql)
        courses = self.cursor.fetchall()

        for course in courses:
            if course in result:
                self.tree.insert("", 0, values=(course[0], "Course"))
                #visited.append(course)


        self.Connect()
        self.sql = 'SELECT Projectname from PROJECT ORDER BY Projectname DESC'
        self.cursor.execute(self.sql)
        projects = self.cursor.fetchall()

        for project in projects:
            if project in result:
                self.tree.insert("", 0, values=(project[0], "Project"))
                #visited.append(project)

        self.tree.place(y=350, x = 90)
        self.treeScroll.place(y=350, x = 420)
        # print self.sqlTotal

    def resetfilter(self):
        self.nameEntry.grid_remove()
        print(self.categoriesMain)
        for index in range(self.categoriesMain + 1):
            print index
            self.categoryVar[index].set("")
        self.categoriesMain = 0
        self.designationVar.set("")
        self.majorVar.set("")
        self.yearVar.set("")
        self.selectOption1.grid_remove()
        self.selectOption2.grid_remove()
        self.selectOption3.grid_remove()

        self.nameEntry = Entry(self.mainPage, width=50)
        self.nameEntry.place(y=60, x=150)

        self.categoryLabel = Label(self.mainPage, text="Category: ")
        self.categoryLabel.place(y=90, x=70)
        self.categoryEntry = []
        # self.categoryEntry.append(OptionMenu(rootWin, width=50))

        self.Connect()
        self.sql = 'SELECT Categoryname FROM CATEGORY'
        categoryOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            categoryOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.categoryVar = []
        # self.categoriesMain = 0
        self.categoryVar.append(StringVar())
        self.categoryEntry.append(OptionMenu(self.mainPage, self.categoryVar[self.categoriesMain], *categoryOptions))
        self.categoryEntry[self.categoriesMain].place(y=90, x=150)

        # self.coursenumberLabel = Label(rootWin, text="Course Number: ")
        # self.coursenumberLabel.place(y=90, x=60)
        # self.coursenumberEntry = Entry(rootWin, width=50)
        # self.coursenumberEntry.place(y=90, x=150)

        # self.instructorLabel = Label(rootWin, text="Instructor: ")
        # self.instructorLabel.place(y=120, x=70)
        # self.instructorEntry = Entry(rootWin, width=50)
        # self.instructorEntry.place(y=120, x=150)

        self.Connect()
        self.sql = 'SELECT Designationname FROM DESIGNATION'
        designationOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            designationOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.designationVar = StringVar()
        self.designationEntry = OptionMenu(self.mainPage, self.designationVar, *designationOptions)
        self.designationEntry.place(y=190, x=150)

        self.Connect()
        self.sql = 'SELECT Majorname FROM MAJOR'
        majorOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            majorOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.majorVar = StringVar()
        self.majorEntry = OptionMenu(self.mainPage, self.majorVar, *majorOptions)
        self.majorEntry.place(y=220, x=150)

        self.yearVar = StringVar()
        self.yearEntry = OptionMenu(self.mainPage, self.yearVar, "freshman", "sophomore", "junior", "senior")
        self.yearEntry.place(y=250, x=150)

        # self.numStudentsLabel = Label(rootWin, text="Estimated # of Students: ")
        # self.numStudentsLabel.place(y=290, x=18)
        # self.numStudentsEntry = Entry(rootWin, width=50)
        # self.numStudentsEntry.place(y=290, x=150)

        self.selectOptionVar = StringVar()
        self.selectOption1 = Radiobutton(self.mainPage, text="Course", variable=self.selectOptionVar, value="COURSE")
        self.selectOption2 = Radiobutton(self.mainPage, text="Project", variable=self.selectOptionVar, value="PROJECT")
        self.selectOption3 = Radiobutton(self.mainPage, text="Both", variable=self.selectOptionVar, value="BOTH")
        self.selectOption1.place(y=290, x=120)
        self.selectOption2.place(y=290, x=210)
        self.selectOption3.place(y=290, x=290)
        # for item in ["one", "two", "three", "four"]:
        #     self.selectOption.insert(END, item)
        # self.selectOption.place(y=290, x=150)

        # self.deptReqLabel = Label(rootWin, text="Department Requirement: ")
        # self.deptReqLabel.place(y=460, x=10)
        # deptReqVar = StringVar()
        # self.deptReqEntry = OptionMenu(rootWin, deptReqVar, "Community", "Sustainable Communities")
        # self.deptReqEntry.place(y=460, x=150)

        # self.applyfilter = Button(self.mainPage, text="Apply Filter", command=self.applyfilter)
        # self.applyfilter.place(y=320, x=90)

        # self.resetfilter = Button(self.mainPage, text="Reset Filter", command=self.resetfilter)
        # self.resetfilter.place(y=320, x=230)

        self.tree = ttk.Treeview(self.win)
        self.treeScroll = ttk.Scrollbar(self.win)
        self.treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.tree.bind("<1>", self.onClick)
        self.tree["columns"] = ("Name", "Type")
        self.tree["show"] = "headings" 
        self.tree.column("Name", width=260)
        self.tree.column("Type", width=80)
        self.tree.heading("Name", text = "Name")
        self.tree.heading("Type", text = "Type")

        self.Connect()
        self.sql = 'SELECT Projectname from PROJECT ORDER BY Projectname DESC'
        self.cursor.execute(self.sql)
        projects = self.cursor.fetchall()
        
        # print("info: ", information)
        self.db.close()
        visited = []
        for project in projects:
            if project not in visited:
                self.tree.insert("", 0, values=(project[0], "Project"))
                visited.append(project)

        self.Connect()
        self.sql = 'SELECT Coursename from COURSE ORDER BY Coursename DESC'
        self.cursor.execute(self.sql)
        courses = self.cursor.fetchall()
        
        # print("info: ", information)
        self.db.close()
        visited = []
        for course in courses:
            if course not in visited:
                self.tree.insert("", 0, values=(course[0], "Course"))
                visited.append(course)

        self.tree.place(y=350, x = 90)
        self.treeScroll.place(y=350, x = 420)

    def addCategoryMain(self):
        self.Connect()
        self.sql = 'SELECT Categoryname FROM CATEGORY'
        categoryOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            categoryOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        if self.categoriesMain < 8:
            self.categoriesMain += 1
            self.categoryVar.append(StringVar())
            self.categoryEntry.append(OptionMenu(self.win, self.categoryVar[self.categoriesMain], *categoryOptions))
            if self.categoriesMain < 5:
                self.categoryEntry[self.categoriesMain].place(y=90, x=150 + 60 * self.categoriesMain)
            else: 
                self.categoryEntry[self.categoriesMain].place(y=120, x=150 + 60 * (self.categoriesMain - 5))
    

    def MePage(self):
        self.mePage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.mePage
        self.win.geometry("500x500")
        frame = Frame(self.mePage)

        self.title = Label(self.mePage, text="ME", font=("Arial", 20), fg="gold3")
        self.title.grid(row=15, column=250)


        self.edit = Button(self.mePage, text="Edit Profile", command=self.EditProfile)
        self.edit.grid(row=18, column=250, sticky=W)

        self.myApp = Button(self.mePage, text="My Application", command=self.MyApplicationPage)
        self.myApp.grid(row=20, column=250, sticky=E)

        self.backButton = Button(self.mePage, text="Back", command = self.MainPage)
        self.backButton.grid(row=22, column=250, sticky=E)

    def MyApplicationPage(self):
        self.appPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.appPage

        self.win.geometry("500x500")
        frame = Frame(self.appPage)

        self.title = Label(self.appPage, text="My Application", font=("Arial", 20), fg="gold3")
        self.title.grid(row=15, column=250)

        # TODO: query table of current applications 
        appTree = ttk.Treeview(self.appPage)
        appTree['show'] = 'headings'
        appTree["columns"] = ("Date", "Project Name", "Status")
        appTree.column("Date", width = 80)
        appTree.column("Project Name", width = 200)
        appTree.column("Status", width=200)
        appTree.heading("Date", text = "Date")
        appTree.heading("Project Name", text = "Project Name")
        appTree.heading("Status", text= "Status")
        self.Connect()
        self.sql = 'SELECT Date, Projectname, Status FROM APPLY WHERE Studentname=%s ORDER BY Date, Projectname, Status'
        self.cursor.execute(self.sql,(self.username))
        info = self.cursor.fetchall()
        for i in info:
            appTree.insert("",0,values=(i[0], i[1], i[2]))
        
        appTree.place(y=50, x=50)



        self.back = Button(self.appPage, text="Back", command= self.MePage)
        self.back.grid(row=19, column=250, sticky=W)


    def ChooseFunctionalityPage(self):
        self.funcPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.funcPage

        self.win.geometry("500x500")
        frame = Frame(self.funcPage)

        # self.win.geometry("500x500")
        
        self.title = Label(self.funcPage, text="Choose Functionality", font=("Arial", 20), fg="gold3")
        self.title.grid(row=0, column=1)


        self.viewAppButton = Button(self.funcPage, text="View Applications", command=self.ViewApplicationsPage)
        self.viewAppButton.grid(row = 1, column = 1)

        self.viewPopularProjectReportButton = Button(self.funcPage, text="View popular project Report", command=self.PopularProjectReportPage)
        self.viewPopularProjectReportButton.grid(row = 2, column = 1)

        self.viewAppReportButton = Button(self.funcPage, text="View Application report", command=self.ApplicationReportPage)
        self.viewAppReportButton.grid(row = 3, column = 1)

        self.viewAddProjectButton = Button(self.funcPage, text="Add a Project", command=self.AddProjectPage)
        self.viewAddProjectButton.grid(row = 4, column = 1)

        self.viewAddCourseButton = Button(self.funcPage, text="Add a Course", command=self.AddCoursePage)
        self.viewAddCourseButton.grid(row = 5, column = 1)
        self.viewLogOutButton = Button(self.funcPage, text="Log out", command = self.LoginPage)
        self.viewLogOutButton.grid(row = 6, column = 1)


    def AddCoursePage(self):
        self.addCoursePage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.addCoursePage
        self.win.geometry("500x500")

        self.title = Label(self.addCoursePage, text="Add a Course", font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=180)

        self.title = Label(self.addCoursePage, text="Add a Course", font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=180)

        self.coursenameLabel = Label(self.addCoursePage, text="Course Name:")
        self.coursenameLabel.place(y=60, x=50)
        self.coursenameEntry = Entry(self.addCoursePage, width=20)
        self.coursenameEntry.place(y=60, x=170)

        self.coursenumberLabel = Label(self.addCoursePage, text="Course Number: ")
        self.coursenumberLabel.place(y=90, x=50)
        self.coursenumberEntry = Entry(self.addCoursePage, width=20)
        self.coursenumberEntry.place(y=90, x=170)

        self.instructorLabel = Label(self.addCoursePage, text="Instructor: ")
        self.instructorLabel.place(y=120, x=50)
        self.instructorEntry = Entry(self.addCoursePage, width=20)
        self.instructorEntry.place(y=120, x=170)

        self.Connect()
        self.sql = 'SELECT Designationname FROM DESIGNATION'
        designationOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            designationOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.designationLabel = Label(self.addCoursePage, text="Designation: ")
        self.designationLabel.place(y=150, x=50)
        self.designationVar = StringVar()
        self.designationEntry = OptionMenu(self.addCoursePage, self.designationVar, *designationOptions)
        self.designationEntry.place(y=150, x=150)

        self.Connect()
        self.sql = 'SELECT Categoryname FROM CATEGORY'
        categorynOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            categoryOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.categoryLabel = Label(self.addCoursePage, text="Category: ")
        self.categoryLabel.place(y=190, x=50)
        self.categoryEntry = []
        # self.categoryEntry.append(OptionMenu(self.addCoursePage, width=50))
        self.categoryVar = []
        self.categoriesCourse = 0
        self.categoryVar.append(StringVar())
        self.categoryEntry.append(OptionMenu(self.addCoursePage, self.categoryVar[self.categoriesCourse], *categoryOptions))
        self.categoryEntry[self.categoriesCourse].place(y=190, x=150)

        self.addButton = Button(self.addCoursePage, text="Add Category", command=self.addCategoryCourse)
        self.addButton.place(y=240, x=70)

        self.numStudentsLabel = Label(self.addCoursePage, text="Est. # of Students: ")
        self.numStudentsLabel.place(y=290, x=50)
        self.numStudentsEntry = Entry(self.addCoursePage, width=10)
        self.numStudentsEntry.place(y=290, x=180)

        # self.majorReqLabel = Label(self.addCoursePage, text="Major Requirement: ")
        # self.majorReqLabel.place(y=380, x=40)
        # majorReqVar = StringVar()
        # self.majorReqEntry = OptionMenu(self.addCoursePage, majorReqVar, "Community", "Sustainable Communities")
        # self.majorReqEntry.place(y=380, x=150)

        # self.yearReqLabel = Label(self.addCoursePage, text="Year Requirement: ")
        # self.yearReqLabel.place(y=420, x=45)
        # yearReqVar = StringVar()
        # self.yearReqEntry = OptionMenu(self.addCoursePage, yearReqVar, "Community", "Sustainable Communities")
        # self.yearReqEntry.place(y=420, x=150)

        # self.deptReqLabel = Label(self.addCoursePage, text="Department Requirement: ")
        # self.deptReqLabel.place(y=460, x=10)
        # deptReqVar = StringVar()
        # self.deptReqEntry = OptionMenu(self.addCoursePage, deptReqVar, "Community", "Sustainable Communities")
        # self.deptReqEntry.place(y=460, x=150)

        self.back = Button(self.addCoursePage, text="Back", command=self.ChooseFunctionalityPage)
        self.back.place(y=330, x=90)

        self.submitCourseButton = Button(self.addCoursePage, text="Submit", command=self.submitCourse)
        self.submitCourseButton.place(y=330, x=150)

    # def back(self):
    #     print("Logged in!")
        
    def submitCourse(self):
        self.Connect()
        self.sql = 'SELECT Coursenumber, Coursename from COURSE'
        self.cursor.execute(self.sql)
        information=self.cursor.fetchall()
        self.db.close()

        self.coursename = self.coursenameEntry.get()
        self.coursenumber = self.coursenumberEntry.get()
        self.instructor = self.instructorEntry.get()
        self.numStudents = self.numStudentsEntry.get()

        if self.coursename == "" or self.coursenumber == "" or self.instructor == "" or self.numStudents == "" or self.designationVar.get() == "" or len(self.categoryEntry) == 0:
            tkMessageBox.showwarning('Error!', 'Cannot have empty field')
        # elif self.password != self.confirmPassword:
        #     tkMessageBox.showwarning('Error!', 'Passwords do not match')
        # elif '@gatech.edu' not in self.email:
        #     tkMessageBox.showwarning('Error!', ' Enter a valid GT email')
        else:
            noError = True
            for info in information:
                if self.coursenumber in info:
                    tkMessageBox.showwarning('Error!', 'Course Number already exists')
                    noError = False
                elif self.coursename in info:
                    tkMessageBox.showwarning('Error!', 'Course Name already exists')
                    noError = False

            if noError:
                self.Connect()
                self.sql = 'INSERT INTO COURSE(Coursename, NumberofStudents, Coursenumber, Designation, Instructor) VALUES(%s, %s, %s, %s, %s)'
                self.designation = self.designationVar.get()
                self.designation = self.designation[2: len(self.designation) - 3]
                print(self.designation)
                self.cursor.execute(self.sql, (self.coursename, self.numStudents, self.coursenumber, self.designation, self.instructor))
                for index in range(len(self.categoryEntry)):
                    if not self.categoryVar[index].get() == "": 
                        category = self.categoryVar[index].get()
                        category = category[2: len(category) - 3]
                        self.sql = 'INSERT INTO COURSE_IS_CATEGORY(Categoryname, Coursenumber) VALUES(%s, %s)'
                        self.cursor.execute(self.sql, (category, self.coursenumber))
                self.db.commit()
                self.db.close()
                tkMessageBox.showwarning('Successful!',  'Succcessful Course Addition!')

    def addCategoryCourse(self):
        self.Connect()
        self.sql = 'SELECT Categoryname FROM CATEGORY'
        categoryOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            categoryOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        # self.categoryEntry.append(OptionMenu(rootWin, var, *categoryOptions))
        if self.categoriesCourse < 8:
            self.categoriesCourse += 1
            self.categoryVar.append(StringVar())
            self.categoryEntry.append(OptionMenu(self.win, self.categoryVar[self.categoriesCourse], *categoryOptions))
            if self.categoriesCourse < 5:
                self.categoryEntry[self.categoriesCourse].place(y=190, x=150 + 60 * self.categoriesCourse)
            else: 
                self.categoryEntry[self.categoriesCourse].place(y=220, x=150 + 60 * (self.categoriesCourse - 5))

    def AddProjectPage(self):
        self.addProjectPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.addProjectPage

        self.win.geometry("500x700")

        self.title = Label(self.addProjectPage, text="Add a Project", font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=180)

        self.projectnameLabel = Label(self.addProjectPage, text="Project Name:")
        self.projectnameLabel.place(y=60, x=50)
        self.projectnameEntry = Entry(self.addProjectPage, width=30)
        self.projectnameEntry.place(y=60, x=170)

        self.advisorLabel = Label(self.addProjectPage, text="Advisor: ")
        self.advisorLabel.place(y=90, x=50)
        self.advisorEntry = Entry(self.addProjectPage, width=30)
        self.advisorEntry.place(y=90, x=170)

        self.emailLabel = Label(self.addProjectPage, text="Advisor Email: ")
        self.emailLabel.place(y=120, x=50)
        self.emailEntry = Entry(self.addProjectPage, width=30)
        self.emailEntry.place(y=120, x=170)

        self.descriptionLabel = Label(self.addProjectPage, text="Description: ")
        self.descriptionLabel.place(y=150, x=50)
        self.descriptionEntry = Entry(self.addProjectPage, width=38)
        self.descriptionEntry.place(y=150, x=170)

        self.Connect()
        self.sql = 'SELECT Categoryname FROM CATEGORY'
        categorynOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            categoryOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        # self.categoryLabel = Label(rootWin, text="Category: ")
        # self.categoryLabel.place(y=220, x=70)
        # self.categoryEntry = []
        # # self.categoryEntry.append(OptionMenu(rootWin, width=50))
        # var = StringVar()
        # self.categoryEntry.append(OptionMenu(rootWin, var, *categoryOptions))
        # self.categoriesProject = 0
        # self.categoryEntry[self.categoriesProject].place(y=220, x=150)

        self.categoryLabel = Label(self.addProjectPage, text="Category: ")
        self.categoryLabel.place(y=220, x=50)
        self.categoryEntry = []
        # self.categoryEntry.append(OptionMenu(rootWin, width=50))
        self.categoryVar = []
        self.categoriesProject = 0
        self.categoryVar.append(StringVar())
        self.categoryEntry.append(OptionMenu(self.addProjectPage, self.categoryVar[self.categoriesProject], *categoryOptions))
        self.categoryEntry[self.categoriesProject].place(y=220, x=180)

        self.addButton = Button(self.addProjectPage, text="Add Category", command=self.addCategoryProject)
        self.addButton.place(y=280, x=50)

        self.Connect()
        self.sql = 'SELECT Designationname FROM DESIGNATION'
        designationOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            designationOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')
        
        self.designationLabel = Label(self.addProjectPage, text="Designation: ")
        self.designationLabel.place(y=310, x=50)
        self.designationVar = StringVar()
        self.designationEntry = OptionMenu(self.addProjectPage, self.designationVar, *designationOptions)
        self.designationEntry.place(y=310, x=180)

        self.numStudentsLabel = Label(self.addProjectPage, text="Est. # of Students: ")
        self.numStudentsLabel.place(y=350, x=50)
        self.numStudentsEntry = Entry(self.addProjectPage, width=10)
        self.numStudentsEntry.place(y=350, x=180)

        self.Connect()
        self.sql = 'SELECT Majorname FROM MAJOR'
        majorOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            majorOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.majorReqLabel = Label(self.addProjectPage, text="Major Requirement: ")
        self.majorReqLabel.place(y=380, x=50)
        self.majorReqVar = StringVar()
        self.majorReqEntry = OptionMenu(self.addProjectPage, self.majorReqVar, *majorOptions)
        self.majorReqEntry.place(y=380, x=180)

        self.yearReqLabel = Label(self.addProjectPage, text="Year Requirement: ")
        self.yearReqLabel.place(y=420, x=50)
        self.yearReqVar = StringVar()
        self.yearReqEntry = OptionMenu(self.addProjectPage, self.yearReqVar, "freshman", "sophomore", "junior", "senior")
        self.yearReqEntry.place(y=420, x=180)

        self.Connect()
        self.sql = 'SELECT Departmentname FROM DEPARTMENT'
        departmentOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            departmentOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        self.deptReqLabel = Label(self.addProjectPage, text="Department Requirement: ")
        self.deptReqLabel.place(y=460, x=50)
        self.deptReqVar = StringVar()
        self.deptReqEntry = OptionMenu(self.addProjectPage, self.deptReqVar, *departmentOptions)
        self.deptReqEntry.place(y=460, x=220)

        self.back = Button(self.addProjectPage, text="Back", command=self.ChooseFunctionalityPage)
        self.back.place(y=500, x=90)

        self.submitProjectButton = Button(self.addProjectPage, text="Submit", command=self.submitProject)
        self.submitProjectButton.place(y=500, x=180)

    def submitProject(self):
        self.Connect()
        self.sql = 'SELECT Projectname from PROJECT'
        self.cursor.execute(self.sql)
        information=self.cursor.fetchall()
        self.db.close()

        self.projectname = self.projectnameEntry.get()
        self.advisor = self.advisorEntry.get()
        self.email = self.emailEntry.get()
        # self.description = self.descriptionEntry.get("1.0", END)
        self.description = self.descriptionEntry.get()
        self.numStudents = self.numStudentsEntry.get()

        if self.projectname == "" or self.advisor == "" or self.email == "" or self.numStudents == "" or self.designationVar.get() == "" or len(self.categoryEntry) == 0 or self.description == "":
            tkMessageBox.showwarning('Error!', 'Cannot have empty field')
        # elif self.password != self.confirmPassword:
        #     tkMessageBox.showwarning('Error!', 'Passwords do not match')
        # elif '@gatech.edu' not in self.email:
        #     tkMessageBox.showwarning('Error!', ' Enter a valid GT email')
        else:
            noError = True
            for info in information:
                if self.projectname in info:
                    tkMessageBox.showwarning('Error!', 'Project Name already exists')
                    noError = False
                # if self.coursename in info:
                #     tkMessageBox.showwarning('Error!', 'Course Name already exists')
                #     noError = False

            if noError:
                self.Connect()
                self.sql = 'INSERT INTO PROJECT(Projectname, NumberofStudents, Description, Advisorname, Advisoremail, Designation) VALUES(%s, %s, %s, %s, %s, %s)'
                self.designation = self.designationVar.get()
                self.designation = self.designation[2: len(self.designation) - 3]
                self.cursor.execute(self.sql, (self.projectname, self.numStudents, self.description, self.advisor, self.email, self.designation))
                for index in range(len(self.categoryEntry)):
                    if not self.categoryVar[index].get() == "": 
                        category = self.categoryVar[index].get()
                        category = category[2: len(category) - 3]
                        self.sql = 'INSERT INTO PROJECT_IS_CATEGORY(Categoryname, Projectname) VALUES(%s, %s)'
                        self.cursor.execute(self.sql, (category, self.projectname))
                if self.majorReqVar.get() == "" and self.yearReqVar.get() == "" and self.deptReqVar.get() == "":
                    req = "none"
                    self.sql = 'INSERT INTO REQUIREMENT(Requirement, Projectname) VALUES(%s, %s)'
                    self.cursor.execute(self.sql, (req, self.projectname))
                else:
                    if not self.majorReqVar.get() == "":
                        req = self.majorReqVar.get()
                        req = req[2: len(req) - 3] + " students only"
                        self.sql = 'INSERT INTO REQUIREMENT(Requirement, Projectname) VALUES(%s, %s)'
                        self.cursor.execute(self.sql, (req, self.projectname))
                    if not self.yearReqVar.get() == "":
                        req = self.yearReqVar.get()
                        req = req + " students only"
                        self.sql = 'INSERT INTO REQUIREMENT(Requirement, Projectname) VALUES(%s, %s)'
                        self.cursor.execute(self.sql, (req, self.projectname))    
                    if not self.deptReqVar.get() == "":
                        req = self.deptReqVar.get()
                        req = req[2: len(req) - 3] + " students only"
                        self.sql = 'INSERT INTO REQUIREMENT(Requirement, Projectname) VALUES(%s, %s)'
                        self.cursor.execute(self.sql, (req, self.projectname))
                self.db.commit()
                self.db.close()
                tkMessageBox.showwarning('Successful!',  'Succcessful Project Addition!')

    def addCategoryProject(self):
        self.Connect()
        self.sql = 'SELECT Categoryname FROM CATEGORY'
        categoryOptions = []
        try:
            self.cursor.execute(self.sql)
            info = self.cursor.fetchall()
            categoryOptions = info
            # print("options: ", options)
        except:
            raise
            messagebox.showwarning('Error!','Check your Internet Connection ')

        if self.categoriesProject < 8:
            self.categoriesProject += 1
            self.categoryVar.append(StringVar())
            self.categoryEntry.append(OptionMenu(self.win, self.categoryVar[self.categoriesProject], *categoryOptions))
            if self.categoriesProject < 5:
                self.categoryEntry[self.categoriesProject].place(y=220, x=180 + 60 * self.categoriesProject)
            else: 
                self.categoryEntry[self.categoriesProject].place(y=270, x=180 + 60 * (self.categoriesProject - 5))

    ### FOR POPULAR PROJECT REPORT PAGE ###

    def findNumOfApplicants(self, applications, projectName):
        numOfApplications = 0
        for application in applications:
            if application[0] == projectName:
                numOfApplications = numOfApplications + 1
                
        return numOfApplications

    def PopularProjectReportPage(self):
        self.popularProjectReportPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.popularProjectReportPage

        self.win.geometry("700x500")
        frame = Frame(rootWin)

        self.title = Label(self.popularProjectReportPage, text="Popular Projects", font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=210)

        tree = ttk.Treeview(self.popularProjectReportPage)
        tree['show'] = 'headings'
        tree["columns"] = ("Project", "# of Applicants") 
        tree.column("Project", width=220)
        tree.column("# of Applicants", width=100)
        tree.heading("Project", text = "Project")
        tree.heading("# of Applicants", text = "# of Applicants")

        self.Connect()
        self.sql = 'SELECT Projectname, Numberofstudents from PROJECT'
        self.cursor.execute(self.sql)
        projects = self.cursor.fetchall()
        # print("info: ", information)
        self.db.close()

        for project in projects:
            projectName = project[0]

            self.Connect()
            self.sql = 'SELECT Projectname from APPLY WHERE Projectname = %s'
            self.cursor.execute(self.sql, projectName)
            applications = self.cursor.fetchall()
            self.db.close()

            numOfApplicants = self.findNumOfApplicants(applications, projectName)

            tree.insert("", 0, values=(projectName, numOfApplicants))

        tree.place(y=50, x=100)

        self.back = Button(self.popularProjectReportPage, text="Back", command=self.ChooseFunctionalityPage) # change to ChooseFunctionality
        self.back.place(y=300, x=210)

    ### FOR POPULAR PROJECT REPORT PAGE - UNTIL HERE ###

    ### FOR APPLICATION REPORT PAGE ###

    def findApplicationInfo(self, applications, projectName):
        numOfApplications = 0
        studentsAccepted = 0
        for application in applications:
            if application[0] == projectName:
                numOfApplications = numOfApplications + 1
                if application[1] == "Accepted":
                    studentsAccepted = studentsAccepted + 1
        return (numOfApplications, (str(float(studentsAccepted)/numOfApplications * 100)) + "%")

    def findTop3Majors(self, applications, projectName):

        self.Connect()
        self.sql = 'SELECT Major, COUNT(*) from APPLY JOIN STUDENT ON Studentname=Username WHERE Projectname =%s group by Major ORDER BY COUNT(*) DESC LIMIT 3'
        self.cursor.execute(self.sql, projectName)
        studentInfo = self.cursor.fetchall()
        self.db.close()
        majors = ""
        for major in studentInfo:
            if major[0] is not None:
                if majors is not "":
                    majors = majors + "/" + major[0]
                else:
                    majors = majors + major[0]
        return majors


    def ApplicationReportPage(self):
        
        self.applicationReportPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.applicationReportPage

        self.win.geometry("800x400")
        frame = Frame(rootWin)

        self.title = Label(self.applicationReportPage, text="Application Report", font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=280)

        tree = ttk.Treeview(self.applicationReportPage)
        tree['show'] = 'headings'
        tree["columns"] = ("Project", "# of Applicants", "Acceptance Rate", "Top 3 Majors") 
        tree.column("Project", width=260)
        tree.column("# of Applicants", width=90)
        tree.column("Acceptance Rate", width=90)
        tree.column("Top 3 Majors", width=150)
        tree.heading("Project", text = "Project")
        tree.heading("# of Applicants", text = "# of Applicants")
        tree.heading("Acceptance Rate", text = "Acceptance Rate")
        tree.heading("Top 3 Majors", text = "Top 3 Majors")

        self.Connect()
        self.sql = 'SELECT Projectname, Status, Studentname from APPLY'
        self.cursor.execute(self.sql)
        applications = self.cursor.fetchall()
        
        # print("info: ", information)
        self.db.close()
        visited = []
        for application in applications:
            if application[0] not in visited:
                projectName = application[0]
                status = application[1]
                studentName = application[2]

                applicationInfo = self.findApplicationInfo(applications, projectName)
                top3Majors = self.findTop3Majors(applications, projectName)
                tree.insert("", 0, values=(projectName, applicationInfo[0], applicationInfo[1], top3Majors))
                visited.append(projectName)

        tree.place(y=50, x=50)

        self.back = Button(self.applicationReportPage, text="Back", command=self.ChooseFunctionalityPage)
        self.back.place(y=300, x=210)

    ### APPLICATION REPORT PAGE - UNITL HERE ######


    def ViewCourse(self, coursename):
        self.viewCourse = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.viewCourse
        
        self.win.geometry("500x500")
        frame = Frame(self.viewCourse)

        self.Connect()
        self.sql = 'SELECT * from COURSE WHERE Coursename = %s'
        self.cursor.execute(self.sql, coursename)
        self.courseDetail = self.cursor.fetchone() 

        self.title = Label(self.viewCourse, text=self.courseDetail[2], font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=180)

        self.nameLabel = Label(self.viewCourse, text="Course Name: " + self.courseDetail[0])
        self.nameLabel.place(y=60, x=70)

        self.instructorLabel = Label(self.viewCourse, text="Instructor: " + self.courseDetail[4])
        self.instructorLabel.place(y=90, x=70)

        self.designationLabel = Label(self.viewCourse, text="Designation: " + self.courseDetail[3])
        self.designationLabel.place(y=120, x=70)

        self.Connect()
        self.sql = 'SELECT Categoryname from COURSE_IS_CATEGORY WHERE Coursenumber = %s'
        self.cursor.execute(self.sql, self.courseDetail[2])
        categories = self.cursor.fetchall() 

        print categories
        catStr = ""
        for category in categories:
            catStr += category[0] + ", "

        print catStr

        self.categoriesLabel = Label(self.viewCourse, text="Categories: " + catStr[0: len(catStr) - 2])
        self.categoriesLabel.place(y=150, x=70)

        self.numStudentsLabel = Label(self.viewCourse, text="Estimated Number of students: " + str(self.courseDetail[1]))
        self.numStudentsLabel.place(y=180, x=70)
 
        self.back = Button(self.viewCourse, text="Back", command=self.MainPage)
        self.back.place(y=240, x=90)


    def backCourse(self):
        self.win.withdraw()
        # self.mainPage.win.deiconify()
        # self.mainPage()
    def ViewProject(self, projectname):
        self.viewProject = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.viewProject
        
        self.win.geometry("500x500")
        frame = Frame(self.viewProject)

        self.Connect()
        self.sql = 'SELECT * from PROJECT WHERE Projectname = %s'
        self.cursor.execute(self.sql, projectname)
        self.projectDetail = self.cursor.fetchone() 

        self.title = Label(self.viewProject, text=self.projectDetail[0], font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=180)

        self.advisorLabel = Label(self.viewProject, text="Advisor: " + self.projectDetail[3] + " (" + self.projectDetail[4] +")")
        self.advisorLabel.place(y=60, x=70)

        self.descriptionLabel = Label(self.viewProject, text="Description: " + self.projectDetail[2])
        self.descriptionLabel.place(y=90, x=70)

        self.designationLabel = Label(self.viewProject, text="Designation: " + self.projectDetail[5])
        self.designationLabel.place(y=150, x=70)

        self.Connect()
        self.sql = 'SELECT Categoryname from PROJECT_IS_CATEGORY WHERE Projectname = %s'
        self.cursor.execute(self.sql, self.projectDetail[0])
        categories = self.cursor.fetchall() 

        catStr = ""
        for category in categories:
            catStr += category[0] + ", "

        self.categoriesLabel = Label(self.viewProject, text="Categories: " + catStr[0: len(catStr) - 2])
        self.categoriesLabel.place(y=180, x=70)
       
        self.Connect()
        self.sql = 'SELECT Requirement from REQUIREMENT WHERE Projectname = %s'
        self.cursor.execute(self.sql, self.projectDetail[0])
        self.requirements = self.cursor.fetchall() 

        reqStr = ""
        for requirement in self.requirements:
            reqStr += requirement[0] + ", "

        self.categoriesLabel = Label(self.viewProject, text="Requirements: " + reqStr[0: len(reqStr) - 2])
        self.categoriesLabel.place(y=210, x=70)

        self.numStudentsLabel = Label(self.viewProject, text="Estimated Number of students: " + str(self.projectDetail[1]))
        self.numStudentsLabel.place(y=240, x=70)
 
        self.back = Button(self.viewProject, text="Back", command=self.MainPage)
        self.back.place(y=270, x=90)

        self.applybutton = Button(self.viewProject, text="Apply", command=self.apply)
        self.applybutton.place(y=270, x=260)


    def apply(self):
        self.Connect()
        self.sql = 'SELECT Projectname, Studentname from APPLY'
        self.cursor.execute(self.sql)
        projectApply=self.cursor.fetchall()
        self.db.close()

        noError = True
        print(projectApply)
        print((self.projectDetail[0], self.username))
        self.Connect()
        self.sql = 'SELECT Department from MAJOR WHERE Majorname = %s'
        self.cursor.execute(self.sql, self.majorUser[0])
        self.departmentUser=self.cursor.fetchall()
        self.db.close()
        self.requirementList = []
        for requirement in self.requirements:
            print(requirement[0][0: len(requirement[0]) - 14])
            self.requirementList.append(requirement[0][0: len(requirement[0]) - 14])
        print(self.requirementList)
        print("none" not in self.requirementList)
        print(self.majorUser[0] not in self.requirementList)
        print(self.departmentUser[0][0] not in self.requirementList)
        self.Connect()
        self.sql = 'SELECT Year from STUDENT WHERE Username = %s'
        self.cursor.execute(self.sql, self.username)
        self.year=self.cursor.fetchall()
        self.db.close()
        print((self.year[0][0]).lower())
        print((self.year[0][0]).lower() not in self.requirementList)
        if (self.projectDetail[0], self.username) in projectApply:
            tkMessageBox.showwarning('Error!', 'You have already applied to this project.')
            noError = False
            # if self.coursename in info:
            #     tkMessageBox.showwarning('Error!', 'Course Name already exists')
            #     noError = False
        # print ("Major", self.majorUser[0])
        # print(self.departmentUser[0])
        if self.majorUser[0] == None or "none" not in self.requirements and self.majorUser[0] not in self.requirementList and self.departmentUser[0][0] not in self.requirementList:
            tkMessageBox.showwarning('Error!', 'Major/Department Restriction not satisfied.')
            noError = False
        # elif "none" not in self.requirements and self.departmentUser[0] not in self.requirements:
        #     tkMessageBox.showwarning('Error!', 'Department Restriction not satisfied.')
        #     noError = False
        if "none" not in self.requirementList and (self.year[0][0]).lower() not in self.requirementList:
            tkMessageBox.showwarning('Error!', 'Year Restriction not satisfied.')
            noError = False
        if noError:
            self.Connect()
            self.sql = 'INSERT INTO APPLY(Studentname, Projectname, Status, Date) VALUES(%s, %s, %s, %s)'
            # print self.designationVar.get()
            self.cursor.execute(self.sql, (self.username, self.projectDetail[0], "Pending", datetime.date.today()))
            self.db.commit()
            self.db.close()
            tkMessageBox.showwarning('Successful!',  'Succcessfully Applied!')


    ## FOR VIEW APPLICATIONS PAGE ##

    def accept(self, tree):
        # idd = tree.selection()[0]
        selected = tree.focus()
        application = tree.item(selected)
        status = application["values"][4]
        username = application["values"][1]
        projectName = application["values"][0]

        if status == "Pending":
            self.Connect()
            self.sql = 'UPDATE APPLY SET Status = %s WHERE Studentname = %s and Projectname = %s'
            self.cursor.execute(self.sql, ("Accepted", username, projectName))
            self.db.commit()
            self.db.close()

            tree = ttk.Treeview(self.viewApplicationsPage)
            tree['show'] = 'headings'
            tree["columns"] = ("Project", "Applicant Username", "Applicant Major", "Applicant Year", "Status") 
            tree.column("Project", width=260)
            tree.column("Applicant Username", width=220)
            tree.column("Applicant Major", width=130)
            tree.column("Applicant Year", width=130)
            tree.column("Status", width=120)
            tree.heading("Project", text="Project")
            tree.heading("Applicant Username", text="Applicant Username")
            tree.heading("Applicant Major", text="Applicant Major")
            tree.heading("Applicant Year", text="Applicant Year")
            tree.heading("Status", text="Status")

            self.Connect()
            self.sql = 'SELECT Projectname, Status, Studentname from APPLY'
            self.cursor.execute(self.sql)
            applications = self.cursor.fetchall()
            self.db.close()

            for application in applications:

                projectName = application[0]
                status = application[1]
                studentName = application[2]
                self.Connect()
                self.sql = 'SELECT Username, Major, Year from STUDENT WHERE Username = %s'
                self.cursor.execute(self.sql, studentName)
                student = self.cursor.fetchall()
                self.db.close()
                username = student[0][0]
                major = student[0][1]
                year = student[0][2]
                tree.insert("", 0, values=(projectName, username, major, year, status))

            tree.place(y=50, x=50)
            self.acceptButton = Button(self.viewApplicationsPage, text="Accept", command=partial(self.accept, tree))
            self.acceptButton.place(y=300, x=600)
            self.rejectButton = Button(self.viewApplicationsPage, text="Reject", command=partial(self.reject, tree))
            self.rejectButton.place(y=300, x=700)
        else:
            if status == "Accepted":
                tkMessageBox.showwarning("Already Accepted!", "This application has already been accepted")
            elif status == "Rejected":
                tkMessageBox.showwarning("Already Rejected", "This application has already been rejected")

    def reject(self, tree):
        selected = tree.focus()
        application = tree.item(selected)
        status = application["values"][4]
        username = application["values"][1]
        projectName = application["values"][0]

        if status == "Pending":
            self.Connect()
            self.sql = 'UPDATE APPLY SET Status = %s WHERE Studentname = %s and Projectname = %s'
            self.cursor.execute(self.sql, ("Rejected", username, projectName))
            self.db.commit()
            self.db.close()

            tree = ttk.Treeview(self.viewApplicationsPage)
            tree['show'] = 'headings'
            tree["columns"] = ("Project", "Applicant Username", "Applicant Major", "Applicant Year", "Status") 
            tree.column("Project", width=260)
            tree.column("Applicant Username", width=220)
            tree.column("Applicant Major", width=130)
            tree.column("Applicant Year", width=130)
            tree.column("Status", width=120)
            tree.heading("Project", text="Project")
            tree.heading("Applicant Username", text="Applicant Username")
            tree.heading("Applicant Major", text="Applicant Major")
            tree.heading("Applicant Year", text="Applicant Year")
            tree.heading("Status", text="Status")

            self.Connect()
            self.sql = 'SELECT Projectname, Status, Studentname from APPLY'
            self.cursor.execute(self.sql)
            applications = self.cursor.fetchall()
            self.db.close()

            for application in applications:

                projectName = application[0]
                status = application[1]
                studentName = application[2]
                self.Connect()
                self.sql = 'SELECT Username, Major, Year from STUDENT WHERE Username = %s'
                self.cursor.execute(self.sql, studentName)
                student = self.cursor.fetchall()
                self.db.close()
                username = student[0][0]
                major = student[0][1]
                year = student[0][2]
                tree.insert("", 0, values=(projectName, username, major, year, status))

            tree.place(y=50, x=50)
            self.acceptButton = Button(self.viewApplicationsPage, text="Accept", command=partial(self.accept, tree))
            self.acceptButton.place(y=300, x=600)
            self.rejectButton = Button(self.viewApplicationsPage, text="Reject", command=partial(self.reject, tree))
            self.rejectButton.place(y=300, x=700)
        else:
            if status == "Accepted":
                tkMessageBox.showwarning("Already Accepted!", "This application has already been accepted")
            elif status == "Rejected":
                tkMessageBox.showwarning("Already Rejected", "This application has already been rejected")

    def ViewApplicationsPage(self):

        self.viewApplicationsPage = Toplevel(self.win)
        self.win.withdraw()
        self.win = self.viewApplicationsPage

        # self.win = rootWin
        self.win.geometry("1000x400")

        self.title = Label(self.viewApplicationsPage, text="Application", font=("Arial", 20), fg="gold3")
        self.title.place(y=10, x=280)

        tree = ttk.Treeview(self.viewApplicationsPage)
        tree['show'] = 'headings'
        tree["columns"] = ("Project", "Applicant Username", "Applicant Major", "Applicant Year", "Status") 
        tree.column("Project", width=260)
        tree.column("Applicant Username", width=220)
        tree.column("Applicant Major", width=130)
        tree.column("Applicant Year", width=130)
        tree.column("Status", width=120)
        tree.heading("Project", text="Project")
        tree.heading("Applicant Username", text="Applicant Username")
        tree.heading("Applicant Major", text="Applicant Major")
        tree.heading("Applicant Year", text="Applicant Year")
        tree.heading("Status", text="Status")

        self.Connect()
        self.sql = 'SELECT Projectname, Status, Studentname from APPLY'
        self.cursor.execute(self.sql)
        applications = self.cursor.fetchall()
        self.db.close()

        for application in applications:

            projectName = application[0]
            status = application[1]
            studentName = application[2]
            self.Connect()
            self.sql = 'SELECT Username, Major, Year from STUDENT WHERE Username = %s'
            self.cursor.execute(self.sql, studentName)
            student = self.cursor.fetchall()
            self.db.close()
            username = student[0][0]
            major = student[0][1]
            year = student[0][2]
            tree.insert("", 0, values=(projectName, username, major, year, status))

        tree.place(y=50, x=50)

        self.back = Button(self.viewApplicationsPage, text="Back", command=self.ChooseFunctionalityPage) # change to ChooseFunctionality
        self.back.place(y=300, x=50)

        self.acceptButton = Button(self.viewApplicationsPage, text="Accept", command=partial(self.accept, tree))
        self.acceptButton.place(y=300, x=600)

        self.rejectButton = Button(self.viewApplicationsPage, text="Reject", command=partial(self.reject, tree))
        self.rejectButton.place(y=300, x=700)

    ## VIEW APPLICATIONS PAGE - UNTIL HERE ##

rootWin=Tk()
main=main(rootWin)
rootWin.mainloop()