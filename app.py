from flask import Flask, request, render_template, redirect, session, jsonify
from sqlalchemy import and_
from sqlalchemy.sql import func
from db import *
from algorithm import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from dateutil import parser
from unidecode import unidecode
import os
import locale
import uuid


# Configuration of the application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AIO.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'TFG_carlos-AIO!2024/2025'
app.config['OBJECTIVE_IMAGES'] = 'static/images/objectives'
app.config['PROFILE_IMAGES'] = 'static/images/profile'


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """
    Renders the User Portal.
    """
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Renders the register form and processes its information
    """
    if request.method == 'POST':
        image = request.files['imageInput']
        username = request.form['user']
        email = request.form['email']
        phone_country_code = request.form['country_code']
        phone_number = request.form['phone_number']
        password = request.form['password1']
        hashed_password = generate_password_hash(password)

        if image:
            extension = os.path.splitext(image.filename)[1]
            filename = f"{username}_{uuid.uuid4().hex}{extension}"
            image_path = os.path.join(app.config['PROFILE_IMAGES'], filename)
            image.save(image_path)
        else:
            filename = None

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            message = "El nombre de usuario ya está en uso por otro usuario."
            return render_template('register.html', message=message)

        if not email:
            email = None
        else:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                message = "El correo electrónico ya está en uso por otro usuario."
                return render_template('register.html', message=message)

        if not phone_number:
            phone_number = None
            phone_country_code = None
        else:
            existing_phone = User.query.filter_by(phone_country_code=phone_country_code,
                                                  phone_number=phone_number).first()
            if existing_phone:
                message = "El número de teléfono ya está en uso por otro usuario."
                return render_template('register.html', message=message)

        new_user = User(image=filename, username=username, email=email,
                        phone_country_code=phone_country_code, phone_number=phone_number,
                        password=hashed_password, agenda_color='#2eb19f')
        db.session.add(new_user)
        db.session.commit()

        create_notification(new_user.id, "Bienvenido", "Te has registrado exitosamente.")

        session['user_id'] = new_user.id
        return redirect('objectives')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders the login form and processes its information.
    """
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        user2 = User.query.filter_by(email=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/agenda/0')
        elif user2 and check_password_hash(user2.password, password):
            session['user_id'] = user2.id
            return redirect('/agenda/0')
        else:
            message = "Nombre de usuario y/o contraseña incorrectos"
            return render_template('login.html', message=message)

    return render_template('login.html')



@app.route('/objectives', methods=['GET', 'POST'])
def show_objectives():
    """
    Renders the objectives page, displaying the objectives set by a user
    :return:
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    today = datetime.now().date()

    objectives_current = Objective.query.filter_by(user_id=user_id, completed=False).filter(
        Objective.start_date <= today, (Objective.end_date >= today) | (Objective.end_date == None)).all()

    objectives_completed = Objective.query.filter_by(user_id=user_id, completed=True).all()

    objectives_past = Objective.query.filter_by(user_id=user_id, completed=False).filter(
        Objective.end_date < today).all()

    objectives_future = Objective.query.filter_by(user_id=user_id, completed=False).filter(
        Objective.start_date > today).all()

    return render_template(
        'my_objectives.html',
        objectives_current=objectives_current,
        objectives_completed=objectives_completed,
        objectives_past=objectives_past,
        objectives_future=objectives_future,
        active_page='objectives'
    )


@app.route('/objective/<int:objective_id>')
def view_objective(objective_id):
    """
    Renders the page displaying the information of an objective.
    :param objective_id: Identificator of the objetive to be displayed.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    objective = Objective.query.get(objective_id)
    if objective:
        tasks_sorted = sorted(objective.tasks, key=lambda task: int(task.priority), reverse=True)
        return render_template('objective.html', objective=objective, tasks=tasks_sorted, active_page='objectives')
    else:
        return render_template("error.html", error="Objetivo no encontrado")



@app.route('/objective_form', methods=['GET', 'POST'])
def objective_form():
    """
    Renders the form to create an objective and processes its information.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if request.method == 'POST':
        name = request.form['name']
        image = request.files['imageInput']
        color = request.form['color']
        priority = request.form['priority']
        hours = request.form['hours']
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']
        user_id = session.get('user_id')

        if image:
            extension = os.path.splitext(image.filename)[1]
            filename = f"{name}_{user_id}_{uuid.uuid4().hex}{extension}"
            image_path = os.path.join(app.config['OBJECTIVE_IMAGES'], filename)
            image.save(image_path)
        else:
            filename = None

        if not start_date_str or not end_date_str:
            return render_template('objective_form.html',
                                   error_message="La fecha de inicio y la fecha de finalización son obligatorias.")

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if end_date < start_date:
            return render_template('objective_form.html',
                                   error_message="La fecha de finalización debe ser mayor o igual a la fecha de inicio.")

        new_objective = Objective(name=name, image=filename, color=color, priority=priority, hours=hours,
                                  start_date=start_date, end_date=end_date, user_id=user_id)
        db.session.add(new_objective)
        db.session.commit()

        create_notification(user_id, "Nuevo Objetivo", f"Has creado un nuevo objetivo: {name}.")

        return redirect('/objective/{0}'.format(new_objective.id))

    return render_template('objective_form.html', active_page='objectives')


@app.route('/edit_objective/<int:objective_id>', methods=['POST'])
def edit_objective(objective_id):
    """
    Processes the information provided when an objective is edited in its modal window.
    :param objective_id: Identificator of the objetive to be edited.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    objective = Objective.query.filter_by(id=objective_id, user_id=user_id).first()

    if objective:
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

        objective.completed = 'completed' in request.form

        db.session.commit()
        return redirect('/objective/{}'.format(objective_id))
    else:
        return "No se pudo encontrar el objetivo para editar", 404


@app.route('/objective/<int:objective_id>/delete_objective', methods=['GET', 'POST'])
def delete_objective(objective_id):
    """
    Deletes an objective from the database.
    :param objective_id: Identificator of the objetive to be deleted.
    """
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


@app.route('/task/<int:task_id>')
def show_task(task_id):
    """
    Renders the page showing a task's information.
    :param task_id: Identificator of the task to be displayed.
    """
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
    """
    Renders the form to create a task and processes its information.
    :param objective_id: Identificator of the objective which the task will be associated to.
    :return:
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if request.method == 'POST':
        name = request.form['name']
        priority = request.form['priority']
        min_hours = request.form['min_hours']
        max_hours = request.form['max_hours']
        location = request.form['location']

        if location == "":
            location = None

        new_task = Task(name=name, priority=priority, min_hours=min_hours, max_hours=max_hours,
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
    """
    Processes the information provided when a task is edited in its modal window.
    :param task_id: Identificator of the task to be edited.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    task = Task.query.get(task_id)

    if task:
        task.name = request.form['name']
        task.priority = request.form['priority']
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
    """
    Deletes a task from the database.
    :param task_id: Identificator of the task to be deleted.
    """
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



@app.route('/agenda/<int:offset>', methods=['GET'])
def agenda(offset=0):
    """
    Renders the page displaying the user's agenda.
    :param offset: Value to calculate the week's events that have to be displayed.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))

    today = datetime.now().date()
    start_of_week = today + timedelta(days=offset * 7 - today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    activities = Activity.query.filter(
        Activity.user_id == user_id,
        Activity.date.between(start_of_week, end_of_week)
    ).all()

    routines = RoutineSchedule.query.join(Routine).filter(
        Routine.user_id == user_id
    ).all()

    tasks = AllocatedTask.query.filter(
        AllocatedTask.user_id == user_id,
        AllocatedTask.date.between(start_of_week, end_of_week)
    ).all()

    weekday_to_enum = {
        0: DayOfWeek.LUNES,
        1: DayOfWeek.MARTES,
        2: DayOfWeek.MIERCOLES,
        3: DayOfWeek.JUEVES,
        4: DayOfWeek.VIERNES,
        5: DayOfWeek.SABADO,
        6: DayOfWeek.DOMINGO
    }
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    week_data = {day: [] for day in DayOfWeek}

    for activity in activities:
        day_enum = weekday_to_enum[activity.date.weekday()]
        week_data[day_enum].append({
            'id': activity.id,
            'type': 'activity',
            'name': activity.name,
            'start_time': activity.start_time.strftime('%H:%M'),
            'end_time': activity.end_time.strftime('%H:%M'),
            'description': activity.description,
            'color': activity.color
        })

    for routine in routines:
        week_data[routine.day_of_week].append({
            'id': routine.routine_id,
            'type': 'routine',
            'name': routine.routine.name,
            'start_time': routine.start_time.strftime('%H:%M'),
            'end_time': routine.end_time.strftime('%H:%M'),
            'description': routine.routine.description,
            'color': routine.routine.color
        })

    for task in tasks:
        objective_color = task.task.objective.color if task.task.objective else None
        day_enum = weekday_to_enum[task.date.weekday()]
        week_data[day_enum].append({
            'id': task.id,
            'type': 'task',
            'name': task.name,
            'start_time': task.start_time.strftime('%H:%M'),
            'end_time': task.end_time.strftime('%H:%M'),
            'completed': task.completed,
            'color': objective_color
        })

    for day, events in week_data.items():
        events.sort(key=lambda x: x['start_time'])

    return render_template('agenda.html', week_data=week_data, offset=offset, start_date=start_of_week.strftime('%d de %B'), end_date=end_of_week.strftime('%d de %B de %Y'), active_page='agenda', agenda_color=user.agenda_color)



@app.route('/plan', methods=['GET', 'POST'])
def plan():
    """
    Invokes the algorithm to generate the allocation of tasks in the agenda and store them in the database.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    AllocatedTask.query.filter_by(completed=False).delete()
    db.session.commit()

    allocated_tasks = algorithm()

    for task in allocated_tasks:
        allocated_task = AllocatedTask(
            name=task['task_name'],
            date=task['day'],
            start_time=task['start_time'],
            end_time=task['end_time'],
            dedicated_hours=task['dedicated_hours'],
            task_id=task['task_id'],
            user_id=user_id
        )
        db.session.add(allocated_task)
    db.session.commit()

    return redirect('/agenda/0')


@app.route('/task/<int:task_id>/toggle_completed', methods=['POST'])
def toggle_task_completed(task_id):
    """
    Toggles in the database the actual boolean value of an allocated task in the agenda if a users sets it as
    completed or not.
    :param task_id: Identificator of the allocated task.
    """
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    task = AllocatedTask.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'success': False, 'message': 'Task not found'}), 404

    task.completed = not task.completed
    db.session.commit()

    return jsonify({'success': True, 'message': 'Task updated successfully', 'completed': task.completed}), 200


@app.route('/activity_form', methods=['GET', 'POST'])
def activity_form():
    """
    Processes the information introduced in the modal window to add an activity to the agenda.
    """
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

    return redirect('/agenda/0')


@app.route('/routine_form', methods=['GET', 'POST'])
def routine_form():
    """
    Processes the information introduced in the modal window to add a routine to the agenda.
    """
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

    return redirect('/agenda/0')



@app.route('/event/<string:event_type>/<int:event_id>/delete_event', methods=['POST'])
def delete_event(event_type, event_id):
    """
    Deletes from the database an event in the agenda.
    :param event_type: Indicates if the event to be deleted is an activity, a routine or an allocated task.
    :param event_id: Identificator of the event (primary key on its table in the database).
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if event_type == 'activity':
        activity = Activity.query.filter_by(id=event_id, user_id=user_id).first()
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Activity deleted successfully'}), 200

    elif event_type == 'routine':
        routine = Routine.query.filter_by(id=event_id, user_id=user_id).first()
        if routine:
            db.session.delete(routine)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Routine deleted successfully'}), 200

    else:
        task = AllocatedTask.query.filter_by(id=event_id, user_id=user_id).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Task deleted successfully'}), 200

    return jsonify({'success': False, 'message': 'Activity, Routine or Task not found'}), 404




@app.route('/update_agenda_color', methods=['POST'])
def update_agenda_color():
    """
    Updates the user's agenda color in the database.
    :return:
    """
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    new_color = request.json.get('color')
    if new_color:
        user.agenda_color = new_color
        db.session.commit()
        return jsonify({'message': 'Color de agenda actualizado correctamente'})
    else:
        return jsonify({'error': 'No se proporcionó un nuevo color para la agenda'})



@app.route('/progress')
def progress():
    """
    Renders the page to display the progress in tasks and objectives achieved by a user.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    objectives = Objective.query.filter_by(user_id=user_id).all()

    allocated_task_counts = (
        db.session.query(AllocatedTask.task_id, func.count(AllocatedTask.id))
        .filter(AllocatedTask.user_id == user_id, AllocatedTask.completed == True)
        .group_by(AllocatedTask.task_id)
        .all()
    )

    allocated_task_hours = (
        db.session.query(AllocatedTask.task_id, func.sum(AllocatedTask.dedicated_hours))
            .filter(AllocatedTask.user_id == user_id, AllocatedTask.completed == True)
            .group_by(AllocatedTask.task_id)
            .all()
    )

    task_count_map = {task_id: count for task_id, count in allocated_task_counts}
    task_hours_map = {task_id: hours or 0 for task_id, hours in
                      allocated_task_hours}

    objectives_status = {}
    today = datetime.now().date()
    for objective in objectives:
        if objective.completed:
            status = "Objetivo cumplido"
        elif objective.start_date > today:
            days_remaining = (objective.start_date - today).days
            status = f"Días restantes para iniciar el objetivo: {days_remaining}"
        elif objective.end_date < today:
            days_expired = (today - objective.end_date).days
            status = f"El objetivo expiró hace {days_expired} días"
        else:
            status = "Objetivo en curso"

        objectives_status[objective.id] = status

    total_objectives = len(objectives)
    completed_objectives = sum(1 for obj in objectives if obj.completed)
    completed_percentage = (completed_objectives / total_objectives * 100) if total_objectives > 0 else 0

    return render_template(
        'progress.html',
        objectives=objectives,
        task_count_map=task_count_map,
        task_hours_map=task_hours_map,
        objectives_status=objectives_status,
        total_objectives=total_objectives,
        completed_objectives=completed_objectives,
        completed_percentage=completed_percentage,
        active_page='progress'
    )


@app.route('/inbox')
def inbox():
    """
    Renders the page to display the inbox with all the notifications sent to a user.
    :return:
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.date.desc(),
                                                                           Notification.time.desc()).all()
    return render_template('inbox.html', notifications=notifications, active_page='inbox')


@app.route('/inbox/<int:notification_id>/delete_notification', methods=['GET', 'POST'])
def delete_notification(notification_id):
    """
    Deletes a notification from the database.
    :param notification_id: Identificator of the notificaition.
    """
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
    """
    Deletes all the notifications of a user from the database.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    Notification.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return redirect('/inbox')


def create_notification(user_id, title, description):
    """
    Creates a new notification in the database.
    :param user_id: Identificator of the user to who the notification corresponds.
    :param title: Title of the notification.
    :param description: Description of the notification.
    """
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


@app.route('/profile')
def profile():
    """
    Renders the page to display the user's profile.
    :return:
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    return render_template('profile.html', user=user, active_page='profile')


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    """
    Updates the user's information in the database based on the information provided in the window modal to edit
    the profile.
    """
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
    """
    Closes the user active session in the device and displays the User Portal.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    session.pop('user_id', None)
    return redirect('/')


@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    """
    Deletes all the information from the database related to the user with the active session in the device.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return render_template('login.html')

    if user_id:
        user = User.query.get(user_id)
        if user:
            Activity.query.filter_by(user_id=user_id).delete()
            for routine in user.routines:
                for schedule in routine.routine_schedules:
                    db.session.delete(schedule)
                db.session.delete(routine)
            for objective in user.objectives:
                for task in objective.tasks:
                    AllocatedTask.query.filter_by(task_id=task.id).delete()
                    db.session.delete(task)


            Objective.query.filter_by(user_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()

            session.pop('user_id', None)

            return redirect('/')


@app.route('/help')
def help():
    """
    Renders the page with the help information.
    """
    return render_template('help.html', active_page='help')

@app.route('/legal')
def legal():
    """
    Renders the page with the Legal Notice.
    """
    return render_template('legal.html', active_page='legal')

@app.route('/privacy_policy')
def privacy_policy():
    """
    Renders the page with the Privacy Policy.
    """
    return render_template('privacy_policy.html', active_page='privacy-policy')


@app.route('/error')
def error():
    """
    Renders the page informing of an error or exception.
    :return:
    """
    return render_template('error.html', active_page='error')


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Renders the error page when an exception or error happens in the application.
    :param e: Description of the exception.
    """
    return render_template("error.html", error=e)




if __name__ == '__main__':
    app.run(debug=True)
