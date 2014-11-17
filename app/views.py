from flask import render_template, request
from app import app
from brewmaster import BrewMaster


# ROUTING/VIEW FUNCTIONS
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    search_term = request.args.get('search_term', None)

    if search_term:
        brew = BrewMaster(search_term)
        results = brew.get_results()
    else:
        results = {'error': 'Please enter a beer or brand'}

    return render_template('index.html', results=results)

@app.route('/author')
def author():
    # Renders author.html.
    return render_template('author.html')
