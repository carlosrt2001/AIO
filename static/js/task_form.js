// Validation of the hours introduced by a user when creating a task.
function validateHours() {
    var min_hours = parseInt(document.getElementById('min_hours').value);
    var max_hours = parseInt(document.getElementById('max_hours').value);

    if (min_hours > max_hours) {
        alert("Las horas mínimas no pueden ser mayores que las horas máximas.");
        return false;
    }

    var start_times = document.querySelectorAll('input[name="start_time[]"]');
    var end_times = document.querySelectorAll('input[name="end_time[]"]');

    for (var i = 0; i < start_times.length; i++) {
        if (!start_times[i].value || !end_times[i].value) {
            alert("Por favor, introduzca las horas de inicio y finalización para cada día.");
            return false;
        }
    }

    return true;
}

// Modifies the value shown in the form based on the selection of the user
function updatePriorityValue(value) {
        document.getElementById('priorityValue').textContent = value;
}

// Add a day and schedule to a task
function addSchedule() {
    var newSchedule = document.querySelector('.schedule').cloneNode(true);
    document.getElementById('schedules').appendChild(newSchedule);
}

// Remove an added day and schedule from a task
function removeSchedule() {
    var schedules = document.getElementById('schedules');
    if (schedules.children.length > 1) {
        schedules.removeChild(schedules.lastChild);
    } else {
        alert("Debe haber al menos un día de realización.");
    }
}


// Open modal window with help information for objectives
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
