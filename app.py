from flask import Flask, url_for, request, render_template, flash, redirect
from forms import DrinkForm, LoginForm
from config import Config
import logic.searchDB as sdb
import logic.drinksSqlDb as drinksdb
import logging

logging.basicConfig(level = logging.DEBUG)

app = Flask(__name__)
# import configuration objects for Flask
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template("base.html")

@app.route('/search', methods = ['GET', 'POST'])
def search():
    drinks_list = []
    drink_names = []
    search = DrinkForm(request.form)
    if search.search.data:
        drink_list = [search.search.data]
        drinks_list = sdb.drink_search(drink_list)[0]

    # if drinks_list is populated, iterate through and just pull the name of the drink
    if drinks_list:
        for drink in drinks_list:
            drink_names.append(drink.drink_name.title())

        logging.debug("List of drink names: {}".format(drink_names))
    if request.method == 'POST':
        return render_template('search.html', form=search, drinks_list=drink_names)


    return render_template('search.html', form=search, drinks_list = drinks_list)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login Requested for user {}, remember_me = {}, password = {}'.format(form.username.data, form.remember_me.data, form.password.data))
        print('Login Requested for user {}, remember_me = {}, password = {}'.format(form.username.data, form.remember_me.data, form.password.data))
        return redirect('/')
    return render_template('login.html', title = "Sign In", form=form)

@app.route('/results/<search>')
@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    flash('No results found!')
    return redirect('/search')

@app.route('/ing')
@app.route('/ing/<name>')
def ing(name = None):
    return render_template('search.html', name=name)

@app.route('/user/<username>')
def profile(username):
    return "{}\'s profile".format(username)

@app.route('/drinks/<name>')
def drinks(name):
    logging.debug("Drink name is {}".format(name))

    # only want the drink object, not the full tuple with the session object
    d_obj = drinksdb.query_drink_first(name)[0]
    logging.debug("Drink object from query is {}".format(d_obj))

    if d_obj:
        recipe = drinksdb.get_formatted_ingredients(d_obj)
        logging.debug("Recipe for {} is {}".format(name, recipe))
        return render_template("drinks.html", drink_name=name, ing_list=recipe)

    return render_template("drinks.html", drink_name = name, ing_list = ["No recipe found"])

if __name__ == '__main__':
    app.run()
