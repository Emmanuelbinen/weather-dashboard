from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

#Thi is our openweathermap API key
API_KEY = "de2d5eeb5277d4a6e3fe79fb9d6c67ea"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)