from flask_sqlalchemy import SQLAlchemy
from enum import Enum

# Initialziation of SQLAlchemy
db = SQLAlchemy()

# Enumeration to represent the days of the week
class DayOfWeek(Enum):
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIERCOLES = 'Miércoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    SABADO = 'Sábado'
    DOMINGO = 'Domingo'

# Representation of the application's users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone_country_code = db.Column(db.String(10), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    agenda_color = db.Column(db.String(7), nullable=True)
    objectives = db.relationship('Objective', backref='user', lazy=True, cascade="all, delete-orphan")

# Representation of an objective
class Objective(db.Model):
    __tablename__ = 'objectives'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(7), nullable=True)
    priority = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tasks = db.relationship('Task', backref='objective', lazy=True, cascade="all, delete")

# Representation of a task
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(100), nullable=False)
    min_hours = db.Column(db.Integer, nullable=False)
    max_hours = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    objective_id = db.Column(db.Integer, db.ForeignKey('objectives.id'), nullable=False)
    schedules = db.relationship('TaskSchedule', backref='task', cascade='all, delete-orphan')

# Representation of the schedules of a task
class TaskSchedule(db.Model):
    __tablename__ = 'task_schedules'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)


# Representation of an activity
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(7), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('activities', lazy=True))

# Representation of a routine
class Routine(db.Model):
    __tablename__ = 'routines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(7), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('routines', lazy=True))
    routine_schedules = db.relationship('RoutineSchedule', backref='routine', cascade='all, delete-orphan', lazy=True)


# Representation of the schedules of a routine
class RoutineSchedule(db.Model):
    __tablename__ = 'routine_schedules'
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'), nullable=False)
    day_of_week = db.Column(db.Enum(DayOfWeek), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

# Representation of a notification
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notifications', lazy=True, cascade="all, delete"))

# Representation of a task assigned by the planification algorithm
class AllocatedTask(db.Model):
    __tablename__ = 'allocated_tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    dedicated_hours = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task = db.relationship('Task', backref='allocated_tasks', lazy=True)



