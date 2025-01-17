// Validation of the hours introduced by a user when editing a task.
function validateHours() {
    var min_hours = parseInt(document.getElementById('min_hours').value);
    var max_hours = parseInt(document.getElementById('max_hours').value);
    if (min_hours > max_hours) {
        alert("Las horas mínimas no pueden ser mayores que las horas máximas.");
        return false;
    }
    return true;
}

// Edit and delete task modal windows
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
        alert("Debe haber al menos un día en el horario.");
    }
}


// Modifies the value shown in the form based on the selection of the user
function updatePriorityValue(value) {
        document.getElementById('priorityValue').textContent = value;
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