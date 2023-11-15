from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def getcocktail(name):
    params = {'s': name}
    url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php'
    response = requests.get(url, params=params)
    result= response.json()
    instruction = result["drinks"][0]['strInstructions']
    print(instruction)
    return instruction


@app.route('/', methods = ['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('hello.html', name ='bb')
    else:
        name = request.form.get('name')
        return f'Hello {name}'
    
@app.route('/movies', methods = ['GET', 'POST'])
def movies():
    name = request.form.get('name')
    return f'I like movies {getcocktail(name)}'

if __name__ == '__main__':
    app.run(debug=True)