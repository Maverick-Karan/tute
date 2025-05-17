from flask import Flask, render_template, request, redirect, url_for
import requests

frontend_app = Flask(__name__)

# Define the backend URL (change if needed)
backendURL = 'http://localhost:3000'  # This is your actual backend server

@frontend_app.route('/')
def home():
    return render_template('index.html')

@frontend_app.route('/success')
def success():
    return render_template('success.html')

@frontend_app.route('/todo')
def todo():
    return render_template('todo.html')

@frontend_app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = request.form.get('age')

    response = requests.post(f'{backendURL}/submit', json={'name': name, 'age': age})
    
    if response.status_code == 200:
        return redirect(url_for('success'))
    else:
        return render_template('index.html', error="Both name and age are required!")

@frontend_app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    response = requests.post(f'{backendURL}/submittodoitem', json={
        'itemName': item_name,
        'itemDescription': item_description
    })

    if response.status_code == 200:
        return redirect(url_for('success'))
    else:
        return render_template('todo.html', error="Both item name and description are required!")

if __name__ == '__main__':
    frontend_app.run(debug=True, port=5000)
