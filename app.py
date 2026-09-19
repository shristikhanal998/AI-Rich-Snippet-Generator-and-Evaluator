from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('landing.html')


'''@app.route('/signup', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('landing'))

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms_agreed = request.form.get('terms')

        if not username or not email or not password or not confirm_password:
            flash(
                'All fields are required.',
                'danger'
            )

            return redirect(
                url_for('signup')
            )

        if len(password) < 8:
            flash(
                'Password must be at least 8 characters.',
                'danger'
            )

            return redirect(
                url_for('signup')
            )

        if password != confirm_password:
            flash(
                'Passwords do not match.',
                'danger'
            )

            return redirect(
                url_for('signup')
            )

        if not terms_agreed:
            flash(
                'You must agree to the Terms of Service and Privacy Policy.',
                'danger'
            )

            return redirect(
                url_for('signup')
            )

        user_exists = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if user_exists:
            flash(
                'Username or email already exists.',
                'danger'
            )

            return redirect(
                url_for('signup')
            )

        new_user = User(
            username=username,
            email=email
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash(
            'Registration successful! Please login.',
            'success'
        )

        return redirect(
            url_for('login')
        )

    return render_template('signup.html')'''
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        #validations
        if not name or len(name.strip())<2:
            flash('Name must be at least 2 characters long.', 'error')
            return redirect(url_for('signup'))
        
        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('signup'))
        
        #password must be at least 8 characters long and a combination of letters and numbers and special characters
        if len(password)<8 or not any(char.isdigit() for char in password)\
              or not any(char.isalpha() for char in password) or not any(not char.isalnum()\
                                                                          for char in password):
            flash('Password must be at least 8 characters long and contain letters, \
                  numbers, and special characters.', 'error')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        
        #check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('signup'))
        
        #create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name.strip(),
            email=email.strip(),
            password=hashed_password
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('signup'))
        
    return render_template('signup.html')


'''@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('landing'))

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if not email or not password:
            flash(
                'Email and password are required.',
                'danger'
            )

            return redirect(
                url_for('login')
            )

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash(
                'Invalid email or password.',
                'danger'
            )

            return redirect(
                url_for('login')
            )

        login_user(user, remember=bool(remember))

        flash(
            'Logged in successfully!',
            'success'
        )

        return redirect(
            url_for('dashboard')
        )

    return render_template('login.html')'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'You have been logged out.',
        'info'
    )

    return redirect(
        url_for('login')
    )


@app.route('/generate-schema')
@login_required
def select_schema():

    schema_types = [
        {
            'id': 'product',
            'name': 'Product',
            'desc': 'E-commerce products with price and reviews.',
            'icon': 'fa-shopping-cart'
        },
        {
            'id': 'faq',
            'name': 'FAQ',
            'desc': 'Frequently asked questions and answers.',
            'icon': 'fa-question-circle'
        },
        {
            'id': 'course',
            'name': 'Course',
            'desc': 'Educational courses with details and providers.',
            'icon': 'fa-graduation-cap'
        }
    ]

    return render_template(
        'generate.html',
        schema_types=schema_types
    )


@app.route('/generate-schema/<schema_type>')
@login_required
def create_schema(schema_type):

    valid_types = [
        'product',
        'faq',
        'course'
    ]

    if schema_type not in valid_types:

        flash(
            'Invalid schema type selected.',
            'danger'
        )

        return redirect(
            url_for('select_schema')
        )

    return render_template(
        f'forms/{schema_type}.html',
        type=schema_type
    )


from models import db, User, Schema

from utils import (
    generate_product_jsonld,
    generate_faq_jsonld,
    generate_course_jsonld
)

import json


@app.route(
    '/generate_jsonld/<schema_type>',
    methods=['POST']
)
@login_required
def generate_jsonld(schema_type):

    json_result = {}

    name_for_storage = ""

    if schema_type == 'product':

        json_result = generate_product_jsonld(
            request.form
        )

        name_for_storage = (
            f"Product: {request.form.get('name')}"
        )

    elif schema_type == 'faq':

        questions = request.form.getlist(
            'question[]'
        )

        answers = request.form.getlist(
            'answer[]'
        )

        json_result = generate_faq_jsonld(
            questions,
            answers
        )

        name_for_storage = (
            f"FAQ: {questions[0][:50]}..."
            if questions
            else "Empty FAQ"
        )

    elif schema_type == 'course':

        json_result = generate_course_jsonld(
            request.form
        )

        name_for_storage = (
            f"Course: {request.form.get('name')}"
        )

    # Convert dictionary to formatted JSON string
    json_string = json.dumps(
        json_result,
        indent=4
    )

    # Save to Database
    new_schema = Schema(
        schema_type=schema_type,
        schema_name=name_for_storage,
        json_content=json_string,
        user_id=current_user.id
    )

    db.session.add(new_schema)
    db.session.commit()

    return render_template(
        'generate_schema.html',
        json_data=json_string,
        schema_type=schema_type
    )


@app.route('/about')
@login_required
def history():

    user_schemas = Schema.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Schema.created_at.desc()
    ).all()

    return render_template(
        'about.html',
        schemas=user_schemas
    )


'''from rule_engine import validate_schema_rules


@app.route(
    '/validate',
    methods=['GET', 'POST']
)
@login_required
def validate():

    validation_report = None

    input_json = ""

    if request.method == 'POST':

        input_json = request.form.get(
            'json_content'
        )

        try:

            # Step 1: Basic Syntax Check
            parsed_data = json.loads(
                input_json
            )

            # Step 2: Rule-Based Validation
            errors, warnings = validate_schema_rules(
                parsed_data
            )

            if not errors and not warnings:

                validation_report = {
                    'status': 'success',
                    'message': 'Perfect! Everything looks great.',
                    'details': 'Your code is valid JSON and follows Schema.org rules.',
                    'errors': [],
                    'warnings': []
                }

            else:

                validation_report = {
                    'status': 'warning'
                    if not errors
                    else 'error',

                    'message': 'Schema Check Complete',

                    'details':
                        f"Found {len(errors)} errors and "
                        f"{len(warnings)} recommendations.",

                    'errors': errors,
                    'warnings': warnings
                }

        except json.JSONDecodeError as e:

            validation_report = {
                'status': 'error',

                'message': 'Syntax Error Found!',

                'details': f"Error: {str(e)}",

                'errors': [
                    'Invalid JSON format. '
                    'Check for missing commas or quotes.'
                ],

                'warnings': []
            }

    return render_template(
        'validate.html',
        report=validation_report,
        input_json=input_json
    )'''


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )