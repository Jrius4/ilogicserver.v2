from flask import Flask,jsonify,request
import uuid
from faker import Faker
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app,resourses={r'/*':{'origins':"*"}})

#sanity check route
@app.route('/ping',methods=['GET'])
def ping_pong():
    return jsonify('Kazibwe Julius Junior!')

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root@localhost:3306/pyweb'
db = SQLAlchemy(app)
faker = Faker()

    
BOOKS = [
    {
        'id':uuid.uuid4().hex,
        'title': 'Game Of Thrones',
        'author': 'Julius Junior Kazibwe',
        'read': True
    },
    {
        'id':uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id':uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id':uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]
def readOut(x):
    if x%2:
        return True
    else:
        return False


for _ in range(10):
    BOOKS.append({
        'id':uuid.uuid4().hex,
        'title': faker.sentence(),
        'author': faker.name(),
        'read': readOut(_)
    })

@app.route('/')
def index():
    return "Hello, Julius Junior"
@app.route('/books',methods=['GET','POST'])
def all_books():
    response_object = {'status':'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id':uuid.uuid4().hex,
            'title':post_data.get('title'),
            'author':post_data.get('author'),
            'read':post_data.get('read'),
        })
        response_object['message'] = 'Book added!';
    else:
        response_object['books']=BOOKS
    return jsonify(response_object)
@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


if __name__ == "__main__":
    app.run(debug=True)