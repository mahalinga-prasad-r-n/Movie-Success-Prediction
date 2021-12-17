from imdb import IMDb
import numpy as np
from tkinter.scrolledtext import ScrolledText
import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import io
import base64
from urllib.request import urlopen
import webbrowser
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

year_list = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
genre_list = ['Action','Adventure','Animation','Comedy','Drama','Family', 'Fantasy', 'Horror','Thriller', 'Romance','Sci-Fi']

ia = IMDb()

def find_rating_over_years(movie_list, year_list):
    print("find_rating_over_years")
    m = {}
    y = []
    rating = {}
    for z in movie_list:
        if z.get('year') in year_list:
            movieID = z.getID()
            m = ia.get_movie(movieID)
            if z.get('year') in rating.keys():
                y = rating[z.get('year')]
            else:
                y = []
            if m.get('rating') is not None:
                y.append(m.get('rating'))
                rating[z.get('year')] = y
    return rating

def find_average_rating(rating, year_list):
    avg_rating = {}
    for key in year_list:
        if key in rating.keys():
            avg_rating[key] = str(round(np.mean(rating[key]), 2))
        else:
            avg_rating[key] = 0
    return avg_rating

def getMovieList(full_person, category):
    print("inside movielist")
    movies = full_person.get("filmography")
    print(movies)
    movie_list = []
    for i in range (len(movies)):
        for key in movies.keys():
            if 'actress' in  movies.keys():
                movie_list = movies['actress']
            if(key == category):
                movie_list = movies[category]
                    
    return movie_list

def getGenreRate(movie_list):
    print("getGenreRate")
    rate  = {}
    rating = []
    for movieID in movie_list:
        if movieID.get('year') in year_list:
            mID = movieID.getID()
            details = ia.get_movie(mID)
            if details.get('rating') is not None:
                for genre in details.get('genres'):
                    if genre in rate.keys():
                        rating = rate[genre]
                    else:
                        rating = []
                    rating.append(details.get('rating'))
                    rate[genre] = rating
    return rate

def getAvgGenre(rate):
    genre_rate = {}
    for key, values in rate.items():
        if (key in genre_list):
            genre_rate[key] = (str(round(np.mean(values), 2))) 
    return genre_rate

def getURL(full_person):
    photo = full_person.get('full-size headshot')
    name = full_person.get('name')
    URL = ia.get_imdbURL(actor[0])
    return ([photo,name,URL])

def getSuccessRate(full_person, category):
    print("inside getsucessrate1")
    #calculate the success rate of actor
    movie_list = getMovieList(full_person, category)
    rating = find_rating_over_years(movie_list, year_list)
    rate = getGenreRate(movie_list)
    return ([rating,rate])

def getSuccess(full_person, category):
    print("inside getsucessrate1")
    #calculate the success rate of actor
    movie_list = getMovieList(full_person, category)
    rate = getGenreRate(movie_list)
    return (rate)

def getAverage(rating,rate):
    avg_rating = find_average_rating(rating, year_list)
    genre_rate = getAvgGenre(rate)
    print (genre_rate)
    print (avg_rating)
    return ([avg_rating,genre_rate])

def getMoviePrediction(genre, actor1, actor2, director):
    genre_movies = {'Action': [31, 250],'Adventure': [52, 250],'Animation': [20, 250],'Comedy': [43, 250],'Drama': [185, 250],'Family': [23, 250],'Fantasy': [30, 250],'Horror': [5, 250],'Romance': [28, 250],'Sci-Fi': [30, 250], 'Thriller': [63, 250]}
    #Uncomment following line to get latest list
    #genre_movies = get_genre_movie_list()
    if actor2 == "":
        e2 = 1
        e2o = 1
    else:
        actor2 = ia.search_person(actor2)
        full_person2 = ia.get_person(actor2[0].getID(), info=["filmography"])
        genreA2 = getSuccess(full_person2,'actor')
        totalA2,successA2, gSuccessA2 = getRating(genreA2, genre)
        gMovieA2 = len(genreA2[genre])
        print (totalA2,successA2,gSuccessA2, gMovieA2)
        if gSuccessA2 == 0 or successA2 == 0 or totalA2 == 0:
            if successA2 == 0:                
                e2 = 0.5
            if gSuccessA2 == 0:
                e20 = 0.5
        else:
            e2 = successA2/totalA2
            e2o = gSuccessA2/gMovieA2
            
    actor1 = ia.search_person(actor1)
    full_person1 = ia.get_person(actor1[0].getID(), info=["filmography"])
    genreA1 = getSuccess(full_person1,'actor')
    totalA1,successA1, gSuccessA1 = getRating(genreA1, genre)
    gMovieA1 = len(genreA1[genre])
    print (totalA1,successA1,gSuccessA1, gMovieA1)
    if gSuccessA1 == 0 or successA1 == 0 or totalA1 == 0:
        if successA1 == 0:                
            e1 = 0.5
        if gSuccessA1 == 0:
            e10 = 0.5
    else:
        e1 = successA1/totalA1
        e1o = gSuccessA1/gMovieA1
      
    director = ia.search_person(director)
    full_person3 = ia.get_person(director[0].getID(), info=["filmography"])
    genreD = getSuccess(full_person3,'director')
    print (genreD)
    totalD,successD, gSuccessD = getRating(genreD, genre)
    gMovieD = len(genreD[genre])
    print (totalD,successD, gSuccessD,gMovieD)
    if gSuccessD == 0 or successD == 0 or totalD == 0:
        if successD == 0:                
            eD = 0.5
        if gSuccessD == 0:
            eDo = 0.5
    else:
        eD = successD/totalD
        eDo = gSuccessD/gMovieD
    
    Po = (e1o* e2o* eDo)/ (e1* e2*eD)
    genreS = genre_movies[genre]
    Po = Po * (genreS[0]/genreS[1]) *100
    if Po > 100:
        Po = 70
    print (e1, e1o, e2,e2o, eD,eDo, Po)
    return Po

def getRating(genreList, genre):
    total = 0
    success = 0
    genreSuccess = 0
    for key,value in genreList.items():
        total = total + len(value)
        for v in value:
            if float(v) >= 7.0 :
                success = success + 1
                if key == genre:
                    genreSuccess = genreSuccess + 1
    return([total,success, genreSuccess])

def get_genre_movie_list():
    m2 = ia.get_top250_movies()
    genre_movies_all  = {}
    movies_all = []
    for movieID in m2:
        mID = movieID.getID()
        details = ia.get_movie(mID)
        for genre in details.get('genres'):
            if genre in genre_movies_all.keys():
                movies_all = genre_movies_all[genre]
            else:
                movies_all = []
            movies_all.append(movieID)
            genre_movies_all[genre] = movies_all
    genre_movies = {}
    for key in genre_movies_all.keys():
        if (key in genre_list):
            genre_movies[key] = [len(genre_movies_all[key]), 250]
    return genre_movies

year_list = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
genre_list = ['Action','Adventure','Animation','Comedy','Drama','Family', 'Fantasy', 'Horror','Thriller', 'Romance','Sci-Fi']
name = 'keanu Reeves'
actor = ia.search_person(name)
full_person = ia.get_person(actor[0].getID(), info=["filmography"])
    
photo,name,URL = getURL(full_person)
rating,rate = getSuccessRate(full_person,'actor')
avg_rating,genre_rate = getAverage(rating,rate)
print(rating)

getMoviePrediction("Drama", "Reese witherspoon", "emma stone", "Glenn Ficarra")

def callback(event):
   webbrowser.open_new(event.widget.cget("text"))

def functionHelloCallBack(res):
       
    actor = ia.search_person(res)
    full_person = ia.get_person(actor[0].getID(), info=["filmography"])
    photo = full_person.get('full-size headshot')
    name = full_person.get('name')
    URL = ia.get_imdbURL(actor[0])
    print(name)
    print(URL)
   
    lbl.configure(text=name)
    lbl1.configure(text=URL)
    lbl2.configure(text=photo)
    print("after label")
        
    rating,rate = getSuccessRate(full_person,'actor')
    print(rating)
    print(rate)
    avg_rating,genre_rate = getAverage(rating,rate)
    #movie_list = getMovieList(full_person)
    #rating = find_rating_over_years(movie_list, year_list)
    #avg_rating = find_average_rating(rating, year_list)
    
    print(avg_rating)
    years = list(avg_rating.keys())  
    ratings = list(avg_rating.values())
    
    graph_year = tkinter.Tk()
    graph_year.title('SUCCESS GRAPH OVER YEARS')
    
    
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(years,ratings)
    
    canvas = FigureCanvasTkAgg(f,graph_year)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    toolbar = NavigationToolbar2Tk(canvas, graph_year)
    toolbar.update()
    canvas._tkcanvas.pack()
    
  
    #genre_rate = getGenreRate(movie_list)
    print(genre_rate)
    genre = list(genre_rate.keys())          
    ratings = list(genre_rate.values())
    
    graph_genre = tk.Toplevel(top)
    graph_genre.title('SUCCESS GRAPH FOR GENRE')
    
    
    f1 = Figure(figsize=(8,5), dpi=100)
    a1 = f1.add_subplot(111)
    a1.bar(genre,ratings,align='center')
    
    
    canvas1 = FigureCanvasTkAgg(f1,graph_genre)
    canvas1.draw()
    canvas1.get_tk_widget().pack()
    
    toolbar = NavigationToolbar2Tk(canvas1, graph_genre)
    toolbar.update()
    canvas1._tkcanvas.pack()
    print("You clicked the button !")
    
    
        
    if len(entry.get()) == 0:
        print("sorry")
        lbl1.configure(text=" ")
        lbl2.configure(text=" ")
        lbl.configure(text="please enter a name")
    else:
        print("here")
        res =  entry.get()
        print(res)
        var = res.replace(" ", "")
        if(var.isalpha()):
            functionHelloCallBack(res)
        else:
            lbl.configure(text="please enter a name without numbers and special character")
            print("sorry")
            
    
    
    #image_url = "http://i46.tinypic.com/r9oh0j.gif"
    #image_byt = urlopen(image_url).read()
    #image_b64 = base64.encodebytes(image_byt)
    #photo = tk.PhotoImage(data=image_b64)
    
    #cv = tk.Canvas(top,bg='black')
   
    #cv.create_image(10, 10, image=photo, anchor='nw')
    #cv.pack(side='top', fill='both', expand='yes')

def count():
    a=10
    b=90
    
    return a

def movie_Predict():
    actor1 = entry4.get()
   # genre = entry3.get()
    director = entry6.get()
    actor = entry5.get()
    print(variable.get()) 
    
    if (entry4.get() and entry6.get()):
        # the user entered data in the mandatory entry: proceed to next step
        print("next step")
        labels = 'SUCCESS', 'FAILURE'
        sizes = [78,22]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
        
        list2=getMoviePrediction(variable.get(), actor, actor1,director)
        print(list2)

        
        b = 100-list2
        a=[]
        a=[list2,b]
    
        pie_success = tk.Toplevel(top)
        pie_success.title('PIE OF PREDICTION')
    
        f1 = Figure(figsize=(8,5), dpi=100)
        a1 = f1.add_subplot(111)
        a1.pie(a, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    
    
        canvas1 = FigureCanvasTkAgg(f1,pie_success)
        canvas1.draw()
        canvas1.get_tk_widget().pack()
    
        toolbar = NavigationToolbar2Tk(canvas1, pie_success)
        toolbar.update()
        canvas1._tkcanvas.pack()
        #root.destroy()
    else:
        # the mandatory field is empty
        print("mandatory data missing")
        if (len(entry4.get())==0):
            lbl7.configure(text="Please enter actor1..")
        else:
            lbl7.configure(text="Please enter directors..")
            
def helloCallBack():
    
    print("You clicked the button !")
    
    
        
    if len(entry.get()) == 0:
        print("sorry")
        lbl1.configure(text=" ")
        lbl2.configure(text=" ")
        lbl.configure(text="please enter a name")
    else:
        print("here")
        res =  entry.get()
        print(res)
        var = res.replace(" ", "")
        if(var.isalpha()):
            functionHelloCallBack(res)
        else:
            lbl.configure(text="please enter a name without numbers and special character")
            print("sorry")
            
    
    
    #image_url = "http://i46.tinypic.com/r9oh0j.gif"
    #image_byt = urlopen(image_url).read()
    #image_b64 = base64.encodebytes(image_byt)
    #photo = tk.PhotoImage(data=image_b64)
    
    #cv = tk.Canvas(top,bg='black')
   
    #cv.create_image(10, 10, image=photo, anchor='nw')
    #cv.pack(side='top', fill='both', expand='yes')         
    
top = tkinter.Tk()
top.title('Movie success prediction ')
top.geometry("500x300")
top.configure(bg="black")

var = StringVar()
label = Label( top, textvariable=var, relief=RAISED )
var.set("SOCIAL MEDIA AND DATA MINING")
label.pack()

var = StringVar()
label = Label( top, textvariable=var, relief=RAISED )
var.set("ANALYSING SUCCESS RATE OF AN ACTOR")
label.pack()

nb = ttk.Notebook(top)

page1 = Frame(nb)
page2 = ttk.Frame(nb)

#frame = Frame(top, width=200, height=200,bg="blue")
#frame.pack()

#text = ScrolledText(page1)
#text.pack(expand=1, fill="both")
label = Label(page1, text="Please enter name")
label.pack()

entry = Entry(page1, bd =5)
entry.pack()

B = tkinter.Button(page1, text ="ANALYSE", command = helloCallBack)
B.pack()

lbl = Label(page1,text="")
lbl.pack()
lbl.bind("<Button-1>", callback)

lbl1 = Label(page1,text="")
lbl1.pack()
lbl1.bind("<Button-1>", callback)

lbl2 = Label(page1,text="")
lbl2.pack()
lbl2.bind("<Button-1>", callback)

# PAGE TWO STARTS.

lbl5 = Label(page2,text="Genre*")
lbl5.pack()
OPTIONS = [
'Action','Adventure','Animation','Comedy','Drama','Family', 'Fantasy', 'Horror','Thriller', 'Romance','Sci-Fi'
] 
variable = StringVar(page2)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(page2, variable, *OPTIONS)
w.pack()

#entry3 = Entry(page2, bd =5)
#entry3.pack()

lbl4 = Label(page2,text="Actor1*")
lbl4.pack()
entry4 = Entry(page2, bd =5)
entry4.pack()

lbl5 = Label(page2,text="Actor")
lbl5.pack()
entry5 = Entry(page2, bd =5)
entry5.pack()

lbl6 = Label(page2,text="Director*")
lbl6.pack()
entry6 = Entry(page2, bd =5)
entry6.pack()

lbl7 = Label(page2,text="")
lbl7.pack()

B = tkinter.Button(page2, text ="PREDICT", command = movie_Predict)
B.pack()

nb.add(page1, text='Actor_success')
nb.add(page2, text='Movie_success_prediction')
nb.pack(expand=1, fill="both")

top.mainloop()