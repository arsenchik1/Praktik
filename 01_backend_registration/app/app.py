import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Настройка логирования
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/registration.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

# Инициализация базы данных
def init_db():
    db.create_all()
    
    # Тестовые пользователи
    test_users = [
        {'name': 'Иван Иванов', 'email': 'ivan@example.com'},
        {'name': 'Петр Петров', 'email': 'petr@example.com'},
        {'name': 'Сидор Сидоров', 'email': 'sidor@example.com'}
    ]
    
    for user_data in test_users:
        if not User.query.filter_by(email=user_data['email']).first():
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=generate_password_hash('password123')
            )
            db.session.add(user)
    
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        email = data.get('email', '')
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        
        # Валидация
        errors = []
        
        if '@' not in email:
            errors.append('Email должен содержать символ @')
        
        if password != confirm_password:
            errors.append('Пароли не совпадают')
        
        if len(password) < 6:
            errors.append('Пароль должен быть не менее 6 символов')
        
        # Проверка существующего пользователя
        existing_user = User.query.filter_by(email=email).first()
        
        # Логирование
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'email': email,
            'validation_errors': errors,
            'user_exists': existing_user is not None,
            'user_data': existing_user.to_dict() if existing_user else None
        }
        
        logging.info(json.dumps(log_data, ensure_ascii=False))
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        if existing_user:
            return jsonify({
                'success': False,
                'errors': ['Пользователь с таким email уже зарегистрирован']
            }), 400
        
        # Успешная регистрация
        full_name = f"{first_name} {last_name}".strip()
        
        return jsonify({
            'success': True,
            'message': f'Поздравляем, {full_name}! Регистрация прошла успешно.'
        })
        
    except Exception as e:
        logging.error(f"Ошибка: {str(e)}")
        return jsonify({
            'success': False,
            'errors': ['Произошла внутренняя ошибка сервера']
        }), 500

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)