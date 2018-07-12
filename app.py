from flask import Flask, url_for, request, render_template, flash, redirect
# from flask_bootstrap import Bootstrap
from forms import DrinkForm, LoginForm
from config import Config
import logic.searchDB as sdb
import logic.drinksSqlDb as drinksdb
import logging

logging.basicConfig(level = logging.DEBUG)

app = Flask(__name__)
# Bootstrap(app)
# import configuration objects for Flask
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/search/', methods = ['GET', 'POST'])
def search():
    drinks_list = []
    drink_names = []
    search = DrinkForm(request.form)
    if search.search.data:
        # drink_search() expects a list of drink names. Will consider adding multiple submission fields to website in the future
        drink_list = [search.search.data]
        drinks_list = sdb.drink_search(drink_list)[0]

    # if drinks_list is populated, iterate through and just pull the name of the drink
    if drinks_list:
        for drink in drinks_list:
            drink_names.append(drink.drink_name.title())

        logging.debug("List of drink names: {}".format(drink_names))
    if request.method == 'POST':
        if not drinks_list:
            flash('No results found!')
        return render_template('search.html', form=search, drinks_list=drink_names)

    # Why am I returning this with the drink object here? I guess this is rendering just the search form since there was no "POST" action
    return render_template('search.html', form=search, drinks_list = drinks_list)

@app.route('/search/ing/', methods = ['GET', 'POST'])
def ingsearch():
    drink_names = []
    search = DrinkForm(request.form)
    if search.search.data:
        # Send the ingredient name searched by user to ing_search()
        # Get back a list of drink names (These are not Drink objects)
        drink_names = sdb.ing_search(search.search.data)
        logging.debug("Ingredient {} is used in {}".format(search.search.data, drink_names))

    if request.method == 'POST':
        if not drink_names:
            flash('No results found!')
        return render_template('ingsearch.html', form = search, ing_name = search.search.data, drinks_list = drink_names)

    return render_template('ingsearch.html', form = search, ing_name = None, drinks_list = None)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login Requested for user {}, remember_me = {}'.format(form.username.data, form.remember_me.data))

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
    source = d_obj.source
    logging.debug("Drink object from query is {}".format(d_obj))

    if d_obj:
        recipe = drinksdb.get_formatted_ingredients(d_obj)
        logging.debug("Recipe for {} is {}".format(name, recipe))
        return render_template("drinks.html", drink_name=name, ing_list=recipe, source = source)

    return render_template("drinks.html", drink_name = name, ing_list = ["No recipe found"])

if __name__ == '__main__':
    app.run()

