from flask import session
from datetime import datetime, timedelta
from db import db, DayOfWeek, User, Objective, Task, TaskSchedule, Activity, Routine, RoutineSchedule, Notification, AllocatedTask


def calculate_next_sunday(date):
    this_week_sunday = date + timedelta(days=(6 - date.weekday()))
    return this_week_sunday + timedelta(days=7)

start_date = datetime.now().date()
end_date = calculate_next_sunday(start_date)

def algorithm():
    activities, routines, tasks = extract_activities_routines_tasks()
    busy_time = order_busy_time(activities, routines, tasks, start_date, end_date)
    free_time = calculate_free_time(busy_time, start_date, end_date)
    objectives_and_tasks = get_objectives_and_tasks(session.get('user_id'), start_date, end_date)
    allocated_tasks = allocate_tasks(objectives_and_tasks, free_time)
    return allocated_tasks

def extract_activities_routines_tasks():
    user_id = session.get('user_id')
    activities_array = []
    routines_array = []
    tasks_array = []
    activities = (Activity.query.filter_by(user_id=user_id).filter(Activity.date >= start_date, Activity.date <= end_date).all())
    for activity in activities:
        activities_array.append(
            {
                "name": activity.name,
                "date": activity.date,
                "start_time": activity.start_time,
                "end_time": activity.end_time,
                "description": activity.description,
                "color": activity.color,
            }
        )

    routines = Routine.query.filter_by(user_id=user_id).all()
    for routine in routines:
        routines_array.append(
            {
                "name": routine.name,
                "description": routine.description,
                "color": routine.color,
                "schedules": [
                    {
                        "day_of_week": schedule.day_of_week.value,
                        "start_time": schedule.start_time,
                        "end_time": schedule.end_time,
                    }
                    for schedule in routine.routine_schedules
                ],
            }
        )

    tasks = (AllocatedTask.query.filter_by(user_id=user_id).filter(AllocatedTask.date >= start_date, AllocatedTask.date <= end_date).all())
    for task in tasks:
        tasks_array.append(
            {
                "name": task.name,
                "date": task.date,
                "start_time": task.start_time,
                "end_time": task.end_time
            }
        )

    return activities_array, routines_array, tasks_array


def order_busy_time(activities, routines, tasks, start_date, end_date):
    busy_time = []

    for activity in activities:
        busy_time.append([activity['date'], activity['start_time'], activity['end_time']])

    for routine in routines:
        for schedule in routine['schedules']:
            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() == get_weekday_number(schedule['day_of_week']):
                    busy_time.append([current_date, schedule['start_time'], schedule['end_time']])
                current_date += timedelta(days=1)

    for task in tasks:
        busy_time.append([task['date'], task['start_time'], task['end_time']])

    busy_time = sorted(busy_time, key=lambda x: (x[0], x[1]))

    return busy_time


def get_weekday_number(day_name):
    days_of_week = {
        "Lunes": 0,
        "Martes": 1,
        "Miércoles": 2,
        "Jueves": 3,
        "Viernes": 4,
        "Sábado": 5,
        "Domingo": 6,
    }
    return days_of_week[day_name]


def get_objectives_and_tasks(user_id, start_date, end_date):
    objectives_array = []

    objectives = Objective.query.filter_by(user_id=user_id, completed=False).filter(
        Objective.start_date <= end_date,
        Objective.end_date >= start_date
    ).all()

    for objective in objectives:
        tasks_array = []
        tasks = Task.query.filter_by(objective_id=objective.id).all()
        for task in tasks:
            tasks_array.append(
                {
                    "id": task.id,
                    "name": task.name,
                    "priority": task.priority,
                    "min_hours": task.min_hours,
                    "max_hours": task.max_hours,
                    "schedules": [
                        {
                            "day_of_week": schedule.day_of_week,
                            "start_time": schedule.start_time,
                            "end_time": schedule.end_time,
                        }
                        for schedule in task.schedules
                    ]
                }
            )

        objectives_array.append(
            {
                "id": objective.id,
                "name": objective.name,
                "priority": objective.priority,
                "hours": objective.hours,
                "start_date": objective.start_date,
                "end_date": objective.end_date,
                "tasks": tasks_array
            }
        )

    return objectives_array

def calculate_free_time(busy_time, start_date, end_date):
    free_time = []
    current_date = start_date
    current_time = datetime.min.time()
    end_time = datetime.max.time()

    while current_date <= end_date:
        daily_busy = [time for time in busy_time if time[0] == current_date]
        daily_busy = sorted(daily_busy, key=lambda x: x[1])

        last_end_time = current_time
        for busy in daily_busy:
            busy_start_time, busy_end_time = busy[1], busy[2]
            if last_end_time < busy_start_time:
                free_time.append([current_date, last_end_time, busy_start_time])
            last_end_time = max(last_end_time, busy_end_time)

        if last_end_time < end_time:
            free_time.append([current_date, last_end_time, end_time])

        current_date += timedelta(days=1)

    return free_time


def allocate_tasks(objectives, free_time):
    user_id = session.get('user_id')
    allocated_tasks = []
    completed_tasks = AllocatedTask.query.filter_by(user_id=user_id).filter(AllocatedTask.date >= start_date,
                                                                            AllocatedTask.date <= end_date,
                                                                            AllocatedTask.completed == True).all()
    task_hours_by_week = {}

    for completed_task in completed_tasks:
        task_week_number = completed_task.date.isocalendar()[1]
        objective_id = completed_task.task.objective_id

        if task_week_number not in task_hours_by_week:
            task_hours_by_week[task_week_number] = {}

        if objective_id not in task_hours_by_week[task_week_number]:
            task_hours_by_week[task_week_number][objective_id] = 0

        task_hours_by_week[task_week_number][objective_id] += completed_task.dedicated_hours


    free_time_by_week = {}
    for interval in free_time:
        free_date, free_start_time, free_end_time = interval
        week_number = free_date.isocalendar()[1]
        if week_number not in free_time_by_week:
            free_time_by_week[week_number] = []
        free_time_by_week[week_number].append(interval)

    objectives = sorted(objectives, key=lambda objective: int(objective['priority']), reverse=True)
    for objective in objectives:
        weekly_hours = {week: 0 for week in free_time_by_week.keys()}
        for week, objective_hours in task_hours_by_week.items():
            if objective['id'] in objective_hours:
                weekly_hours[week] += objective_hours[objective['id']]

        tasks = sorted(objective['tasks'], key=lambda task: int(task['priority']), reverse=True)

        for task in tasks:
            for task_schedule in task['schedules']:
                day_of_week = get_weekday_number(task_schedule['day_of_week'].value)
                task_start_time = task_schedule['start_time']
                task_end_time = task_schedule['end_time']

                for week, free_intervals in free_time_by_week.items():
                    if weekly_hours[week] >= objective['hours']:
                        continue

                    max_available_hours = objective['hours'] - weekly_hours[week]
                    if max_available_hours <= 0:
                        continue

                    for free_interval in list(free_intervals):
                        free_date, free_start_time, free_end_time = free_interval
                        if free_date.weekday() != day_of_week:
                            continue

                        possible_start_time = max(task_start_time, free_start_time)
                        possible_end_time = min(task_end_time, free_end_time)

                        if possible_start_time >= possible_end_time:
                            continue

                        time_for_task = (datetime.combine(start_date, possible_end_time) - datetime.combine(start_date, possible_start_time)).total_seconds() / 3600

                        dedicated_hours = min(task['max_hours'], max(task['min_hours'], time_for_task), max_available_hours)

                        if dedicated_hours >= task['min_hours']:
                            allocated_task = {
                                'task_id': task['id'],
                                'task_name': task['name'],
                                'day': free_date,
                                'start_time': possible_start_time,
                                'end_time': (datetime.combine(start_date, possible_start_time) + timedelta(hours=dedicated_hours)).time(),
                                'dedicated_hours': dedicated_hours
                            }
                            allocated_tasks.append(allocated_task)
                            weekly_hours[week] += dedicated_hours
                            free_intervals.remove(free_interval)

                            if possible_start_time > free_start_time:
                                free_intervals.append((free_date, free_start_time, possible_start_time))
                            if possible_end_time < free_end_time:
                                free_intervals.append((free_date, possible_end_time, free_end_time))

                            free_intervals.sort(key=lambda x: x[1])
                            break

    return allocated_tasks

