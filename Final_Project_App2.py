from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_results(group_by, sort_order):
    conn = sqlite3.connect('Steam_Top_300_Games.sqlite')
    cur = conn.cursor()
    
    if group_by == 'Main_Genre':
        group_column = 'Main_Genre'
    elif group_by == 'Developer':
        group_column = 'Developer'
    elif group_by == 'Publisher':
        group_column = 'Publisher'
    else:
        group_column = 'Franchise'

    q = f'''
        SELECT {group_column}, COUNT(Name)
        FROM Games_Details
        WHERE Name <> 'N/A'
        GROUP BY {group_column}
        ORDER BY COUNT(Name) {sort_order}
        LIMIT 10
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('Menu2.html')

@app.route('/results', methods=['POST'])
def results():
    group_by = request.form['group']
    sort_order = request.form['dir']
    results = get_results(group_by, sort_order)
    return render_template('Results2.html', 
        group=group_by, results=results)

if __name__ == '__main__':
    app.run(debug=True)