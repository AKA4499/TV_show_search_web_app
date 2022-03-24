'''
Blueprint of flask app which contains home page url and some other business logics
'''

from datetime import date
import signal

from flask import Blueprint, render_template, request, flash, jsonify,redirect

# for authentication
from flask_login import login_required, current_user
from .models import Show,Cast,Crew, Date
from . import db
import json
import urllib.request, json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# login required to goto the home page 
@login_required
def home():
    if request.method == 'POST':
        # search based on keyword 
        show = request.form.get('keyword')
        if " " in show:
            show = show.replace(" ","%20")

        if len(show) >= 1:
            # api call with search keyword
            url = "https://api.tvmaze.com/search/shows?q="+show
            response = urllib.request.urlopen(url)
            data = response.read()
            dictionary1 = json.loads(data)
            # print(dictionary1)
            count = 0
            shows = ""
            # for all the information about that keyword extract the important information
            for i in dictionary1 :
                shows = shows + "(" + str(count) +" , "+ str(i['show']['name']) + ", (id - " + str(i['show']['id']) + "))        "
                count += 1
            # print(shows)
            # add the information to the database which will be used to display later
            new_show = Show(data=shows, user_id=current_user.id)
            db.session.add(new_show)
            db.session.commit()
            flash('Search Displayed!', category='success')



        # search for the cast of a show based on the show id 
        cast = request.form.get('cast')
        if len(cast) >= 1 :
            # api call with the show id for cast information of the show
            url1 = "https://api.tvmaze.com/shows/"+str(cast)+"/cast"
            
            response1 = urllib.request.urlopen(url1)
            data1 = response1.read()
            dictionary2 = json.loads(data1)
            
            count = 0
            casts = ""
            # import imformation about the case 
            for i in dictionary2 :
                casts = casts + "(" + str(count) +" , "+ str(i['person']['name']) + " )      "
                count += 1
            

            # store the information in the database
            new_cast = Cast(data=casts, user_id=current_user.id)
            db.session.add(new_cast)
            db.session.commit()
            flash('Cast Displayed!', category='success')


        # search for the crew of the tv show based on show id
        crew = request.form.get('crew')
        if len(crew) >= 1 :
            url2 = "https://api.tvmaze.com/shows/"+str(crew)+"/crew"
            print(url2)
            response2 = urllib.request.urlopen(url2)
            data2 = response2.read()
            dictionary3 = json.loads(data2)
            
            count = 0
            crews = ""
            # important information about the crew
            for i in dictionary3 :
                crews = crews + "(" + str(count) +" , "+ str(i['type']) + " , " + str(i['person']['name']) + " )      "
                count += 1
        
            # store the information in the databse
            new_crew = Crew(data=crews, user_id=current_user.id)
            db.session.add(new_crew)
            db.session.commit()
            flash('Crew Displayed!', category='success')




        # search based on the date
        date = request.form.get('date')
        if len(date) >= 1 :
            # api call to extract information based on the data entered
            url3 = "https://api.tvmaze.com/schedule?country=US&date="+str(date)
            # print(url2)
            response3 = urllib.request.urlopen(url3)
            data3 = response3.read()
            dictionary4 = json.loads(data3)
            
            count = 0
            dates = ""
            # important information abot the shows on that date
            for i in dictionary4 :
                dates = dates + "(" + str(count) +" , "+ str(i["show"]['type']) + " , " + str(i["show"]['name']) + " )     "
                count += 1
                if count == 5:
                    break
            # store the information in the database
            new_date = Date(data=dates, user_id=current_user.id)
            db.session.add(new_date)
            db.session.commit()
            flash('Shows based on date Displayed!', category='success')

        
        


    return render_template("home.html", user=current_user)


# route for deleting the searched results based on keyword
@views.route('/delete-show/<int:id>')
def delete_show(id):
    show = Show.query.get(id)
    if show:
        if show.user_id == current_user.id:
            db.session.delete(show)
            db.session.commit()
            return redirect("/")
    return redirect("/")


# route for deleting the searched results based on show id
@views.route('/delete-cast/<int:id>')
def delete_cast(id):
    cast = Cast.query.get(id)
    if cast:
        if cast.user_id == current_user.id:
            db.session.delete(cast)
            db.session.commit()
            return redirect("/")
    return redirect("/")


# route for deleting the searched results for crew based on show id
@views.route('/delete-crew/<int:id>')
def delete_crew(id):
    crew = Crew.query.get(id)
    if crew:
        if crew.user_id == current_user.id:
            db.session.delete(crew)
            db.session.commit()
            return redirect("/")
    return redirect("/")

# route for deleting the searched results based on date entered
@views.route('/delete-date/<int:id>')
def delete_date(id):
    date = Date.query.get(id)
    if date:
        if date.user_id == current_user.id:
            db.session.delete(date)
            db.session.commit()
            return redirect("/")
    return redirect("/")
