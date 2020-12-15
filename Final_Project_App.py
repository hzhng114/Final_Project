from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_results(sort_by, sort_order):
    conn = sqlite3.connect('Steam_Top_300_Games.sqlite')
    cur = conn.cursor()
    
    if sort_by == 'PercentageReview':
        sort_column = 'PercentageReview'
    elif sort_by == 'Price':
        sort_column = 'Price'
    else:
        sort_column = 'NumberofReviews'

    q = f'''
        SELECT Name, {sort_column}, Rank, ReleaseDate, URL
        FROM Games
        WHERE {sort_column} <> 'N/A'
        ORDER BY {sort_column} {sort_order}
        LIMIT 10
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('Menu1.html')

@app.route('/results', methods=['POST'])
def results():
    sort_by = request.form['sort']
    sort_order = request.form['dir']
    results = get_results(sort_by, sort_order)
    return render_template('Results1.html', 
        sort=sort_by, results=results)

if __name__ == '__main__':
    app.run(debug=True)