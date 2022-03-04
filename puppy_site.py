#adoption_site.py
import os
import pandas as pd
from forms import AddForm,DelForm
from flask import Flask, render_template,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

######################################################
### SQL DATABASE SECTION ##################
###################################

basedir = os.path.abspath(os.path.dirname(__file__))
#OLD SQLITE DATABASE
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
#NEW MYSQL DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Maria0729123@localhost/our_puppies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

###################################################
##### MODELS##################
###############################################
class Puppy(db.Model):

    __tablename__ = 'puppies'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    color = db.Column(db.Text)
    height = db.Column(db.Text)
    breed = db.Column(db.Text)



    def __init__(self,name, color, height, breed):
        self.name = name
        self.color = color
        self.height = height
        self.breed = breed


    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name} and owner is {self.owner.name}"
        else:
            return f"Puppy name is {self.name} and has no owner yet!"


class Owner(db.Model):

    __tablename__ = 'Owners'

    id = db.Column(db.Integer, primary_key = True)


    name = db.Column(db.Text)

    def __init__(self,name):#,puppy_id):

        self.name = name
        #self.puppy_id = puppy_id

########################################



##########################################



########################################
### VIEW FUNCTIONS -- HAVE FORMS ####
####################################################

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods = ['GET', 'POST'])
def add_pup():

    form = AddForm()


    if form.validate_on_submit():

        pup_name = form.pup_name.data
        owner_name = form.owner_name.data
        pup_color = form.pup_color.data
        pup_height = form.pup_height.data
        pup_breed = form.pup_breed.data

        new_pup = Puppy(pup_name, pup_color, pup_height, pup_breed)
        new_owner = Owner(owner_name,)


        db.session.add(new_pup)
        db.session.add(new_owner)

        db.session.commit()

        return redirect(url_for('list_pup'))

    return render_template('add.html', form=form)

@app.route('/list')
def list_pup():

    puppies = Puppy.query.all()
    #owners = Owner.query.all()
    return render_template('list.html', puppies = puppies)



@app.route('/delete', methods = ['GET', 'POST'])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():

        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('delete.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)
