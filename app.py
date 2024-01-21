from flask import Flask, render_template, redirect, url_for, flash
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_bcrypt import Bcrypt
import mysql.connector
from flask import session
from flask_socketio import join_room, leave_room
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
bcrypt = Bcrypt()
socketio = SocketIO(app)
bcrypt = Bcrypt()
questions_data = [
    # Data Structures
    {
        'questionNumber': 1,
        'question': 'Data structure for efficiently finding the median of a dataset.',
        'options': ['Heap', 'AVL Tree', 'B-tree', 'Skip List'],
        'correct_answer': 'Heap'
    },
    {
        'questionNumber': 2,
        'question': 'Which algorithm is used for finding strongly connected components in a directed graph?',
        'options': ['Dijkstra\'s', 'Kosaraju\'s', 'Prim\'s', 'Bellman-Ford'],
        'correct_answer': 'Kosaraju\'s'
    },
    {
        'questionNumber': 3,
        'question': 'What is the time complexity of the best-known comparison-based sorting algorithm?',
        'options': ['O(n log n)', 'O(n^2)', 'O(n)', 'O(log n)'],
        'correct_answer': 'O(n log n)'
    },
    {
        'questionNumber': 4,
        'question': 'Which data structure is suitable for implementing a LRU (Least Recently Used) cache?',
        'options': ['Queue', 'Stack', 'Hash Table', 'Linked List'],
        'correct_answer': 'Linked List'
    },
    {
        'questionNumber': 5,
        'question': 'What is the purpose of Huffman coding in data compression?',
        'options': ['Error detection', 'Lossless compression', 'Lossy compression', 'Encryption'],
        'correct_answer': 'Lossless compression'
    },

    # Object-Oriented Programming (OOP)
    {
        'questionNumber': 6,
        'question': 'Design pattern that allows an object to alter its behavior when its internal state changes.',
        'options': ['Singleton', 'Observer', 'Strategy', 'State'],
        'correct_answer': 'State'
    },
    {
        'questionNumber': 7,
        'question': 'In OOP, what is the Law of Demeter?',
        'options': ['Objects should be encapsulated', 'A class should not know about the internal details of other classes', 'Objects should communicate through interfaces', 'A class should only talk to its immediate neighbors'],
        'correct_answer': 'A class should only talk to its immediate neighbors'
    },
    {
        'questionNumber': 8,
        'question': 'Which design pattern is used to ensure only one instance of a class is created?',
        'options': ['Factory Method', 'Abstract Factory', 'Singleton', 'Builder'],
        'correct_answer': 'Singleton'
    },
    {
        'questionNumber': 9,
        'question': 'What is the purpose of the Proxy design pattern?',
        'options': ['Provide a surrogate or placeholder for another object', 'Implement distributed systems', 'Ensure object immutability', 'Handle object creation'],
        'correct_answer': 'Provide a surrogate or placeholder for another object'
    },
    {
        'questionNumber': 10,
        'question': 'In OOP, what is the term for allowing a subclass to provide a specific implementation of a method that is already provided by its parent class?',
        'options': ['Polymorphism', 'Encapsulation', 'Inheritance', 'Abstraction'],
        'correct_answer': 'Polymorphism'
    },

    # Networks
    {
        'questionNumber': 11,
        'question': 'In networking, what does the term "MSS" stand for?',
        'options': ['Maximum Segment Size', 'Minimum Session Setup', 'Multiple Switching Systems', 'Master Subnet Synchronization'],
        'correct_answer': 'Maximum Segment Size'
    },
    {
        'questionNumber': 12,
        'question': 'Which network protocol is designed for efficient and reliable file transfer over a TCP/IP network?',
        'options': ['FTP', 'SFTP', 'HTTP', 'SMTP'],
        'correct_answer': 'SFTP'
    },
    {
        'questionNumber': 13,
        'question': 'What is the purpose of the OSI model in networking?',
        'options': ['Defines the architecture of a network', 'Ensures secure connections', 'Manages network traffic', 'Facilitates IP address assignment'],
        'correct_answer': 'Defines the architecture of a network'
    },
    {
        'questionNumber': 14,
        'question': 'What is the key advantage of using a virtual private network (VPN) in networking?',
        'options': ['Improved network performance', 'Secure communication over the internet', 'Dynamic IP address assignment', 'Load balancing'],
        'correct_answer': 'Secure communication over the internet'
    },
    {
        'questionNumber': 15,
        'question': 'Which network topology provides fault tolerance and redundancy?',
        'options': ['Bus', 'Ring', 'Mesh', 'Star'],
        'correct_answer': 'Mesh'
    },

    # Database Management Systems (DBMS)
    {
        'questionNumber': 16,
        'question': 'What is the time complexity of finding an element using a clustered index in a database?',
        'options': ['O(log n)', 'O(n)', 'O(1)', 'O(n^2)'],
        'correct_answer': 'O(log n)'
    },
    {
        'questionNumber': 17,
        'question': 'In DBMS, what is the purpose of a foreign key?',
        'options': ['Ensures uniqueness of records', 'Defines a unique constraint', 'Establishes a link between two tables', 'Specifies default values for a column'],
        'correct_answer': 'Establishes a link between two tables'
    },
    {
        'questionNumber': 18,
        'question': 'What is the role of the query optimizer in a relational database?',
        'options': ['Ensures data consistency', 'Improves query performance', 'Manages database security', 'Handles data replication'],
        'correct_answer': 'Improves query performance'
    },
    {
        'questionNumber': 19,
        'question': 'Which normal form is achieved by eliminating transitive dependencies in a relational database?',
        'options': ['First Normal Form (1NF)', 'Second Normal Form (2NF)', 'Third Normal Form (3NF)', 'Boyce-Codd Normal Form (BCNF)'],
        'correct_answer': 'Third Normal Form (3NF)'
    },
    {
        'questionNumber': 20,
        'question': 'What is the purpose of the COMMIT statement in database transactions?',
        'options': ['Roll back changes', 'Save changes to the database', 'Lock database tables', 'Create a temporary table'],
        'correct_answer': 'Save changes to the database'
    },
    {
        'questionNumber': 21,
        'question': 'What is the purpose of the command scheduler in an operating system?',
        'options': ['To allocate resources to processes', 'To manage file systems', 'To handle user interface interactions', 'To encrypt data'],
        'correct_answer': 'To allocate resources to processes'
    },
    {
        'questionNumber': 22,
        'question': 'Explain the concept of thrashing in virtual memory systems.',
        'options': ['Excessive paging, leading to a decrease in overall system performance', 'Optimal memory allocation', 'Effective file system management', 'Improved multitasking'],
        'correct_answer': 'Excessive paging, leading to a decrease in overall system performance'
    },
    {
        'questionNumber': 23,
        'question': 'What is the purpose of the I/O scheduler in an operating system?',
        'options': ['To manage network connections', 'To schedule input/output operations for efficiency', 'To handle user authentication', 'To optimize CPU usage'],
        'correct_answer': 'To schedule input/output operations for efficiency'
    },
    {
        'questionNumber': 24,
        'question': 'Explain the concept of process synchronization in the context of operating systems.',
        'options': ['Managing multiple processes to avoid conflicts and ensure consistency', 'Optimizing CPU scheduling', 'Ensuring secure connections', 'Handling memory allocation'],
        'correct_answer': 'Managing multiple processes to avoid conflicts and ensure consistency'
    },
    {
        'questionNumber': 25,
        'question': 'What is the role of a device driver in an operating system?',
        'options': ['To manage system memory', 'To translate domain names to IP addresses', 'To communicate with hardware devices', 'To control network traffic'],
        'correct_answer': 'To communicate with hardware devices'
    }
]


games = {}

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name', [
        validators.InputRequired(),
        validators.Regexp('^[a-zA-Z ]*$', message='Name should only contain letters and spaces')
    ])
    username = StringField('Username', [
        validators.InputRequired(),
        validators.Regexp('^[a-zA-Z0-9]*$', message='Username should only contain letters and numbers')
    ])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=8, message='Password should be at least 8 characters'),
        validators.Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).*$', 
                          message='Password should contain at least 1 lowercase, 1 uppercase, 1 number, and 1 special character')
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.InputRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    email = StringField('Email', [
        validators.InputRequired(),
        validators.Email(message='Invalid email address'),
        validators.Regexp('^[^@]+@[^@]+\.[^@]+$', message='Invalid email address')
    ])
    phone = StringField('Phone', [
        validators.InputRequired(),
        validators.Regexp('^[0-9]{10}$', message='Phone number should contain only 10 digits')
    ])
    submit = SubmitField('Register')

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abi@ram03",
    database="networks"
)
cursor = db.cursor()

@app.route('/')
@app.route('/home')
def home():
    username = session.get('username')
    # Now you can use the 'username' variable in your template or logic
    return render_template('home.html', username=username)



@app.route('/quiz_lobby', methods=['GET'])
def quiz_lobby():
    username = request.args.get('username', 'Guest')
    print('username',username)
    return render_template('quiz_lobby.html', username=username)

def index():
    return render_template('index.html')
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username and password match the records in the database
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # Username and password are correct, set the user session
            session['user_id'] = user[0]
            
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Validate and process the form data
        name = form.name.data
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data
        phone = form.phone.data

        # Custom validation logic for the name field
        if any(char.isdigit() for char in name):
            flash('Name should only contain letters and spaces. Numbers are not allowed.', 'danger')
            return render_template('register.html', form=form)

        # Custom validation logic for the username field
        if not username.isalnum():
            flash('Username should only contain letters and numbers. Special characters are not allowed.', 'danger')
            return render_template('register.html', form=form)

        # Custom validation logic for the password field
        if not any(char.isupper() for char in password):
            flash('Password should contain at least one uppercase letter.', 'danger')
            return render_template('register.html', form=form)

        # Custom validation logic for the email field
        if not email.endswith('.com'):
            flash('Invalid email address format. Please use a valid email domain (e.g., example@example.com).', 'danger')
            return render_template('register.html', form=form)

        # Custom validation logic for the phone field
        if not phone.isdigit() or len(phone) != 10:
            flash('Phone number should contain only 10 digits.', 'danger')
            return render_template('register.html', form=form)
        query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('register.html', form=form)

        

        # Save the user details to the database (you'll need to implement this logic)
        query = "INSERT INTO User (name, username, password, email, phone) VALUES (%s, %s, %s, %s, %s)"
        values = (name, username, password, email, phone)
        cursor.execute(query, values)
        db.commit()

        flash(f'Account created for {username}!', 'success')
        return render_template('login.html', form=form)
        

    # If the form did not validate, display validation errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {field.capitalize()}: {error}', 'danger')

    return render_template('register.html', form=form)

# ... (rest of the code)



@socketio.on('join_lobby')
def handle_join_lobby(data):
    if 'game_id' in data:
        game_id = data['game_id']
        print(game_id)
        username = data['username']
        print(username)

        if game_id not in games:
            games[game_id] = {'players': []}

        join_room(game_id)
        games[game_id]['players'].append({'username': username, 'current_question_index': 0, 'score': 0})

        socketio.emit('lobby_update', {'players': games[game_id]['players']}, room=game_id)

        if len(games[game_id]['players']) == 2:
            emit_first_question(game_id)
count = 0

@socketio.on('submit_answer')
def handle_submit_answer(data):
    global count  # Declare count as a global variable
    # Process the answer if needed
    game_id = data['game_id']
    username = data['username']
    answer = data['answer']
    print('yes answer submitted')
    count+=1

    player = next((p for p in games[game_id]['players'] if p['username'] == username), None)

    if player:
        current_question = player['current_question_index'] - 1
        if answer == questions_data[current_question]['correct_answer']:
            player['score'] += 1
           
          

        socketio.emit('update_scores', {'players': games[game_id]['players']}, room=game_id)

        if all(player['current_question_index'] == len(questions_data) for player in games[game_id]['players']) and count == 52:
            winner = max(games[game_id]['players'], key=lambda x: x['score'])
            socketio.emit('announce_winner', {'winner': winner}, room=game_id)
        else:
            print('going to emit next question')
            emit_next_question(game_id, username)
    else:
        print('no player found')


@socketio.on('request_next_question')
def handle_request_next_question(data):
    game_id = data['game_id']
    username = data['username']
    emit_next_question(game_id, username)

def emit_first_question(game_id):
    players = games[game_id]['players']

    for player in players:
        current_question_index = player['current_question_index']

        if current_question_index < len(questions_data):
            question = questions_data[current_question_index]
            player['current_question_index'] += 1

            socketio.emit('render_question', {
                'questionNumber': current_question_index + 1,
                'question': question['question'],
                'options': question['options']
            }, room=game_id)
def emit_next_question(game_id, username):
    player = next((p for p in games[game_id]['players'] if p['username'] == username), None)
    print('player',player)

    if player:
        current_question_index = player['current_question_index']

        if current_question_index <len(questions_data):
            question = questions_data[current_question_index]
            player['current_question_index'] += 1
            print('going to emit')

            socketio.emit('ram_q', {
                'username': username,
                'questionNumber': current_question_index + 1,
                'question': question['question'],
                'options': question['options']
            }, room=game_id)  # Emit to the user's room
    else:
        print('no question')


# Add a new event for updating scores
@socketio.on('update_scores_page')
def update_scores_page(data):
    game_id = data['game_id']
    scores = data['scores']

    # Emit the event to the game lobby
    socketio.emit('update_scores_page', {'scores': scores}, room=game_id)



@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5555, debug=True)
