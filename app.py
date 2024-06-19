from flask import Flask, request, render_template, redirect, session, jsonify
from db import db, DayOfWeek, User, Objective, Task, TaskSchedule, Activity, Routine, RoutineSchedule, Notification
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from dateutil import parser
from sqlalchemy import and_
from unidecode import unidecode
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AIO.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'TFG_carlos-AIO!2023/2024'  # Clave secreta utilizada por Flask para tareas de seguridad
app.config['OBJECTIVE_IMAGES'] = 'static/images/objectives'
app.config['PROFILE_IMAGES'] = 'static/images/profile'

db.init_app(app)
with app.app_context():
    db.create_all()


# INDEX
@app.route('/')
def index():
    return render_template('index.html')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Recogida de datos del formulario de registro
        image = request.files['imageInput']
        username = request.form['user']
        email = request.form['email']
        phone_country_code = request.form['country_code']
        phone_number = request.form['phone_number']
        password = request.form['password1']
        hashed_password = generate_password_hash(password)

        # Guardar imagen de perfil
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['PROFILE_IMAGES'], filename)
            image.save(image_path)
        else:
            filename = None

        # Error si el nombre de usuario ya está en uso
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            message = "El nombre de usuario ya está en uso por otro usuario."
            return render_template('register.html', message=message)

        if not email:
            email = None
        else:
            # Error si el correo electrónico ya está en uso
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                message = "El correo electrónico ya está en uso por otro usuario."
                return render_template('register.html', message=message)

        if not phone_number:
            phone_number = None
            phone_country_code = None
        else:
            # Error si el teléfono ya está en uso
            existing_phone = User.query.filter_by(phone_country_code=phone_country_code,
                                                  phone_number=phone_number).first()
            if existing_phone:
                message = "El número de teléfono ya está en uso por otro usuario."
                return render_template('register.html', message=message)

        # Se inserta el nuevo usuario en la base de datos
        new_user = User(image=filename, username=username, email=email,
                        phone_country_code=phone_country_code, phone_number=phone_number,
                        password=hashed_password, agenda_color='#2eb19f')
        db.session.add(new_user)
        db.session.commit()

        # Se crea la notificación de bienvenida
        create_notification(new_user.id, "Bienvenido", "Te has registrado exitosamente.")

        session['user_id'] = new_user.id
        return redirect('main')

    return render_template('register.html')


# LOG IN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Recogida de datos del formulario de inicio de sesión
        username = request.form['user']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()  # se busca el nombre de usuario
        user2 = User.query.filter_by(email=username).first()  # se busca el email
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/main')
        elif user2 and check_password_hash(user2.password, password):
            session['user_id'] = user2.id
            return redirect('/main')
        else:
            # Mensaje de error si el nombre de usuario o la contraseña no coinciden
            message = "Nombre de usuario y/o contraseña incorrectos"
            return render_template('login.html', message=message)

    return render_template('login.html')


# MAIN PAGE
@app.route('/main')
def main():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')
    return render_template('main.html', user=user, active_page='main')


# OBJECTIVES
@app.route('/objectives', methods=['GET', 'POST'])
def show_objectives():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')
    objectives = Objective.query.filter_by(user_id=user_id).all()
    return render_template('my_objectives.html', objectives=objectives, active_page='objectives')


@app.route('/objective/<int:objective_id>')
def view_objective(objective_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    objective = Objective.query.get(objective_id)
    if objective:
        return render_template('objective.html', objective=objective, active_page='objectives')
    else:
        return "Objetivo no encontrado", 404


@app.route('/objective_form', methods=['GET', 'POST'])
def objective_form():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if request.method == 'POST':
        # Recogida de datos del formulario de objetivo
        name = request.form['name']
        image = request.files['imageInput']
        color = request.form['color']
        priority = request.form['priority']
        hours = request.form['hours']
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        user_id = session.get('user_id')

        # En caso de añadir una imagen, se almacena
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['OBJECTIVE_IMAGES'], filename)
            image.save(image_path)
        else:
            filename = None

        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = None

        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = None

        # Se inserta el nuevo objetivo en la base de datos
        new_objective = Objective(name=name, image=filename, color=color, priority=priority, hours=hours,
                                  start_date=start_date, end_date=end_date, user_id=user_id)
        db.session.add(new_objective)
        db.session.commit()

        # Se crea la notificación con el mensaje de nuevo objetivo creado
        create_notification(user_id, "Nuevo Objetivo", f"Has creado un nuevo objetivo: {name}.")

        return redirect('/objective/{0}'.format(new_objective.id))

    return render_template('objective_form.html', active_page='objectives')


@app.route('/edit_objective/<int:objective_id>', methods=['POST'])
def edit_objective(objective_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    objective = Objective.query.filter_by(id=objective_id, user_id=user_id).first()

    if objective:
        # Recogida de datos del formulario de objetivo
        objective.name = request.form['name']
        objective.priority = request.form['priority']
        objective.hours = request.form['hours']
        objective_start_date_str = request.form['start_date']
        objective_end_date_str = request.form['end_date']

        if objective_start_date_str != "":
            objective.start_date = datetime.strptime(objective_start_date_str, '%Y-%m-%d').date()
        else:
            objective.start_date = None

        if objective_end_date_str != "":
            objective.end_date = datetime.strptime(objective_end_date_str, '%Y-%m-%d').date()
        else:
            objective.end_date = None

        db.session.commit()
        return redirect('/objective/{}'.format(objective_id))
    else:
        return "No se pudo encontrar el objetivo para editar", 404


@app.route('/objective/<int:objective_id>/delete_objective', methods=['GET', 'POST'])
def delete_objective(objective_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    objective = Objective.query.filter_by(id=objective_id, user_id=user_id).first()

    if objective:
        Objective.query.filter_by(id=objective.id).delete()
        db.session.delete(objective)
        db.session.commit()
        return redirect('/objectives')
    else:
        return "No se pudo encontrar el objetivo para eliminar", 404


# TASKS
@app.route('/task/<int:task_id>')
def show_task(task_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    task = Task.query.get(task_id)

    if task:
        task_schedules = task.schedules
        return render_template('task.html', task=task, task_schedules=task_schedules, active_page='objectives')
    else:
        return "Tarea no encontrada", 404


@app.route('/<int:objective_id>/task_form', methods=['GET', 'POST'])
def task_form(objective_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if request.method == 'POST':
        name = request.form['name']
        min_hours = request.form['min_hours']
        max_hours = request.form['max_hours']
        location = request.form['location']

        if location == "":
            location = None

        new_task = Task(name=name, min_hours=min_hours, max_hours=max_hours,
                        location=location, objective_id=objective_id)
        db.session.add(new_task)
        db.session.commit()

        day_of_weeks = request.form.getlist('day_of_week[]')
        start_times = request.form.getlist('start_time[]')
        end_times = request.form.getlist('end_time[]')

        for day_of_week, start_time_str, end_time_str in zip(day_of_weeks, start_times, end_times):
            start_time = parser.parse(start_time_str).time()
            end_time = parser.parse(end_time_str).time()

            new_schedule = TaskSchedule(task_id=new_task.id,
                                        day_of_week=DayOfWeek[day_of_week],
                                        start_time=start_time,
                                        end_time=end_time)
            db.session.add(new_schedule)

        db.session.commit()

        return redirect('/objective/{}'.format(objective_id))

    return render_template('task_form.html', objective_id=objective_id, active_page='objectives')


@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    task = Task.query.get(task_id)

    if task:
        task.name = request.form['name']
        task.min_hours = request.form['min_hours']
        task.max_hours = request.form['max_hours']
        location_str = request.form['location']

        if location_str == "":
            task.location = None
        else:
            task.location = location_str

        TaskSchedule.query.filter_by(task_id=task_id).delete()

        day_of_weeks = request.form.getlist('day_of_week[]')
        start_times = request.form.getlist('start_time[]')
        end_times = request.form.getlist('end_time[]')

        for day_of_week, start_time_str, end_time_str in zip(day_of_weeks, start_times, end_times):
            start_time = parser.parse(start_time_str).time()
            end_time = parser.parse(end_time_str).time()

            new_schedule = TaskSchedule(task_id=task_id,
                                        day_of_week=DayOfWeek[day_of_week],
                                        start_time=start_time,
                                        end_time=end_time)
            db.session.add(new_schedule)

        db.session.commit()
    return redirect('/task/{}'.format(task_id))


@app.route('/task/<int:task_id>/delete_task', methods=['GET', 'POST'])
def delete_task(task_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    task = Task.query.filter_by(id=task_id).first()
    objective_id = task.objective_id
    if task:
        Task.query.filter_by(id=task.id).delete()
        db.session.delete(task)
        db.session.commit()

    return redirect('/objective/{}'.format(objective_id))


# AGENDA
@app.route('/agenda')
def agenda():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')
    return render_template('agenda.html', agenda_color=user.agenda_color, active_page='agenda')


@app.route('/activity_form', methods=['GET', 'POST'])
def activity_form():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if request.method == 'POST':
        name = request.form['activity-name']
        date = datetime.strptime(request.form['activity-date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form['activity-startTime'], '%H:%M').time()
        end_time = datetime.strptime(request.form['activity-endTime'], '%H:%M').time()
        description = request.form['activity-description']
        color = request.form['activity-color']
        user_id = session.get('user_id')

        new_activity = Activity(name=name, date=date, start_time=start_time, end_time=end_time,
                                description=description, color=color, user_id=user_id)

        db.session.add(new_activity)
        db.session.commit()

    return redirect('/agenda')


@app.route('/routine_form', methods=['GET', 'POST'])
def routine_form():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if request.method == 'POST':
        name = request.form['routine-name']
        description = request.form['routine-description']
        color = request.form['routine-color']
        user_id = session.get('user_id')

        new_routine = Routine(name=name, description=description, color=color, user_id=user_id)
        db.session.add(new_routine)
        db.session.commit()

        day_of_weeks = request.form.getlist('day_of_week[]')
        start_times = request.form.getlist('start_time[]')
        end_times = request.form.getlist('end_time[]')

        for day_of_week, start_time_str, end_time_str in zip(day_of_weeks, start_times, end_times):
            start_time = parser.parse(start_time_str).time()
            end_time = parser.parse(end_time_str).time()

            new_schedule = RoutineSchedule(routine_id=new_routine.id,
                                           day_of_week=DayOfWeek[day_of_week],
                                           start_time=start_time,
                                           end_time=end_time)
            db.session.add(new_schedule)

        db.session.commit()

    return redirect('/agenda')


@app.route('/get_events', methods=['POST'])
def get_events():
    user_id = session.get('user_id')
    date = request.json.get('date')
    day = request.json.get('day_of_week')
    day_normalized = unidecode(day).upper()

    activities = Activity.query.filter_by(date=date, user_id=user_id).all()

    routines = Routine.query.join(RoutineSchedule).filter(and_(
        Routine.user_id == user_id,
        RoutineSchedule.day_of_week == day_normalized
    )).all()

    events_json = []
    for activity in activities:
        activity_data = {
            'id': activity.id,
            'name': activity.name,
            'start_time': activity.start_time.strftime('%H:%M'),
            'end_time': activity.end_time.strftime('%H:%M'),
            'description': activity.description,
            'color': activity.color,
            'event_type': 'activity'
        }
        events_json.append(activity_data)

    for routine in routines:
        for schedule in routine.routine_schedules:
            day_of_week = str(schedule.day_of_week).split('.')[1]
            if day_of_week == day_normalized:
                routine_data = {
                    'id': routine.id,
                    'name': routine.name,
                    'description': routine.description,
                    'start_time': schedule.start_time.strftime('%H:%M'),
                    'end_time': schedule.end_time.strftime('%H:%M'),
                    'color': routine.color,
                    'event_type': 'routine'
                }
                events_json.append(routine_data)

    return jsonify(sorted(events_json, key=lambda x: x['start_time']))


@app.route('/event/<string:event_type>/<int:event_id>/delete_event', methods=['POST'])
def delete_event(event_type, event_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    print(event_id)
    print(event_type)

    if event_type == 'activity':
        activity = Activity.query.filter_by(id=event_id, user_id=user_id).first()
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return jsonify({'success': 'Activity deleted successfully'}), 200

    elif event_type == 'routine':
        routine = Routine.query.filter_by(id=event_id, user_id=user_id).first()
        if routine:
            db.session.delete(routine)
            db.session.commit()
            return jsonify({'success': 'Routine deleted successfully'}), 200

    return jsonify({'error': 'Activity or Routine not found'}), 404


@app.route('/update_agenda_color', methods=['POST'])
def update_agenda_color():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    new_color = request.json.get('color')
    if new_color:
        user.agenda_color = new_color
        db.session.commit()
        return jsonify({'message': 'Color de agenda actualizado correctamente'})
    else:
        return jsonify({'error': 'No se proporcionó un nuevo color para la agenda'}), 400


# PROGRESS
@app.route('/progress')
def progress():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    return render_template('progress.html', active_page='progress')


# INBOX
@app.route('/inbox')
def inbox():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.date.desc(),
                                                                           Notification.time.desc()).all()
    return render_template('inbox.html', notifications=notifications, active_page='inbox')


@app.route('/inbox/<int:notification_id>/delete_notification', methods=['GET', 'POST'])
def delete_notification(notification_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    notification = Notification.query.filter_by(id=notification_id).first()
    if notification:
        Notification.query.filter_by(id=notification.id).delete()
        db.session.delete(notification)
        db.session.commit()
    return redirect('/inbox')


@app.route('/inbox/delete_all_notifications', methods=['POST'])
def delete_all_notifications():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    Notification.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return redirect('/inbox')


def create_notification(user_id, title, description):
    now = datetime.now()
    new_notification = Notification(
        date=now.date(),
        time=now.time(),
        title=title,
        description=description,
        user_id=user_id
    )
    db.session.add(new_notification)
    db.session.commit()


# PROFILE
@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    return render_template('profile.html', user=user, active_page='profile')


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    username = request.form['username']
    email = request.form['email']
    phone_country_code = request.form['phone_country_code']
    phone_number = request.form['phone_number']

    if email == "":
        email = None

    if phone_number == "":
        phone_number = None

    existing_user = User.query.filter(User.username == username, User.id != user_id).first()
    if existing_user:
        error_message = "No se ha podido actualizar el perfil. El nombre de usuario ya está en uso."
        return render_template('profile.html', user=user, active_page='profile', error_message=error_message)

    existing_email = User.query.filter(User.email == email, User.id != user_id).first()
    if existing_email:
        error_message = "No se ha podido actualizar el perfil. El correo electrónico ya está en uso."
        return render_template('profile.html', user=user, active_page='profile', error_message=error_message)

    existing_phone = User.query.filter(User.phone_country_code == phone_country_code,
                                       User.phone_number == phone_number,
                                       User.id != user_id).first()
    if existing_phone:
        error_message = "No se ha podido actualizar el perfil. El número de teléfono ya está en uso."
        return render_template('profile.html', user=user, active_page='profile', error_message=error_message)

    user.username = username
    user.email = email
    user.phone_country_code = phone_country_code
    user.phone_number = phone_number

    success_message = "Se ha actualizado el perfil correctamente"
    db.session.commit()

    create_notification(user.id, "Perfil Actualizado",
                        '''Se han actualizado los datos en tu perfil:
    nombre de usuario {0} con 
    correo electrónico {1} y 
    teléfono {2} {3}'''.format(username, email, phone_country_code, phone_number))
    return render_template('profile.html', user=user, active_page='profile', success_message=success_message)


@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    session.pop('user_id', None)
    return redirect('/')


@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if user_id:
        user = User.query.get(user_id)
        if user:
            for objective in user.objectives:
                for task in objective.tasks:
                    db.session.delete(task)

            Objective.query.filter_by(user_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()

            session.pop('user_id', None)

            return redirect('/')


# ERROR
@app.route('/error')
def error():
    return render_template('error.html', active_page='error')


@app.errorhandler(Exception)
def handle_exception():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
