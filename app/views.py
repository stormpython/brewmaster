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
        return render_template('index.html', results=results)

    return render_template('index.html')


# @app.route('/<beer_id>')
# def get_beer_by_id(beer_id):
#     brew = BrewMaster(beer_id, is_id=True)
#     results = brew.get_results()
#     return render_template('index.html', results=results)
#
#
# @app.route('/<search_term>/<style_id>/<abv_range>/<page>', methods=['GET'])
# def get_page(search_term, style_id, abv_range, page):
#
#     brew = BrewMaster(search_term, is_id=False, page=page)
#     results = brew.get_page(style_id, abv_range)
#     return render_template('index.html', results=results)


@app.route('/author')
def author():
    # Renders author.html.
    return render_template('author.html')
