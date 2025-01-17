function initMap() {
    var input1 = document.getElementById('location1');
    var autocomplete = new google.maps.places.Autocomplete(input1);

    var input2 = document.getElementById('location2');
    var autocomplete = new google.maps.places.Autocomplete(input2);
}

window.onload = function() {
    initMap();
};

function validateHours() {
    var min_hours = parseInt(document.getElementById('min_hours').value);
    var max_hours = parseInt(document.getElementById('max_hours').value);

    if (min_hours > max_hours) {
        alert("Las horas mínimas no pueden ser mayores que las horas máximas.");
        return false;
    }

    return true;
}

var deleteTaskModal = document.getElementById('deleteTaskModal');
var btnOpenDeleteTask = document.getElementById("deleteTask");
var btnConfirmDelete = document.getElementById("confirmDelete");
var btnCancelDelete = document.getElementById("cancelDelete");
var editTaskModal = document.getElementById('editTaskModal');
var btnOpenEditTask = document.getElementById("editTask");

btnOpenDeleteTask.onclick = function() {
    deleteTaskModal.style.display = "block";
}

btnOpenEditTask.onclick = function() {
    editTaskModal.style.display = "block";
}

btnConfirmDelete.onclick = function() {
    var taskId = document.getElementById('deleteTask').getAttribute('data-task-id');
    window.location.href = "/task/" + taskId + "/delete_task";
}

btnCancelDelete.onclick = function() {
    deleteTaskModal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == deleteTaskModal) {
        deleteTaskModal.style.display = "none";
    }

    if (event.target == editTaskModal) {
        editTaskModal.style.display = "none";
    }
}


function addSchedule() {
    var scheduleDiv = document.createElement('div');
    scheduleDiv.className = 'schedule';

    var dayLabel = document.createElement('label');
    dayLabel.setAttribute('for', 'day_of_week');
    dayLabel.innerHTML = 'Día de la semana:';
    scheduleDiv.appendChild(dayLabel);

    var daySelect = document.createElement('select');
    daySelect.name = 'day_of_week[]';
    var days = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'];
    for (var day of days) {
        var option = document.createElement('option');
        option.value = day;
        option.innerHTML = day.charAt(0) + day.slice(1).toLowerCase();
        daySelect.appendChild(option);
    }
    scheduleDiv.appendChild(daySelect);

    var startLabel = document.createElement('label');
    startLabel.setAttribute('for', 'start_time');
    startLabel.innerHTML = 'Horario: ';
    scheduleDiv.appendChild(startLabel);

    var startTime = document.createElement('input');
    startTime.type = 'time';
    startTime.name = 'start_time[]';
    startTime.required = true;
    scheduleDiv.appendChild(startTime);

    var endLabel = document.createElement('label');
    endLabel.setAttribute('for', 'end_time');
    endLabel.innerHTML = '- ';
    scheduleDiv.appendChild(endLabel);

    var endTime = document.createElement('input');
    endTime.type = 'time';
    endTime.name = 'end_time[]';
    endTime.required = true;
    scheduleDiv.appendChild(endTime);

    var schedulesDiv = document.getElementById('schedules');
    schedulesDiv.appendChild(scheduleDiv);
}

function removeSchedule() {
    var schedules = document.getElementById('schedules');
    if (schedules.children.length > 1) {
        schedules.removeChild(schedules.lastChild);
    } else {
        alert("Debe haber al menos un día en el horario.");
    }
}

function updatePriorityValue(value) {
        document.getElementById('priorityValue').textContent = value;
}

function openModal() {
    var infoModal = document.getElementById('infoModal');
    infoModal.style.display = "block";
}

window.onclick = function(event) {
    var infoModal = document.getElementById('infoModal');
    var closeModal = document.getElementById('closeModal');
    if (event.target == infoModal) {
        infoModal.style.display = "none";
    }
    if (event.target == closeModal) {
        infoModal.style.display = "none";
    }
}