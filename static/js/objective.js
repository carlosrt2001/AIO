// Configure date format
$(function() {
    $(".datepicker").datepicker({
        dateFormat: "dd/mm/yy"
    });
});

// Validation of the dates introduced by a user to create an objective.
function validateDates() {
    var startDateInput = document.getElementById('edit_start_date');
    var endDateInput = document.getElementById('edit_end_date');

    var startDate = new Date(startDateInput.value);
    var endDate = new Date(endDateInput.value);

    if (!startDateInput.value || !endDateInput.value) {
        alert('Por favor, complete ambas fechas.');
        return false;
    }

    if (endDate < startDate) {
        alert('La fecha de finalización debe ser mayor o igual a la fecha de inicio.');
        return false;
    }

    return true;
}

// Modifies the value shown in the form based on the selection of the user
function updatePriorityValue(value) {
        document.getElementById('priorityValue').textContent = value;
}


var buttonsTask = document.querySelectorAll('.btnTask');
buttonsTask.forEach(function(button) {
    button.addEventListener('click', function() {
        var taskId = this.getAttribute('data-id');
        window.location.href = '/task/' + taskId;
    });
});


// Open modal windows to edit and delete an objective
var deleteObjectiveModal = document.getElementById('deleteObjectiveModal');
var btnOpenDeleteObjective = document.getElementById("deleteObjective");
var btnConfirmDelete = document.getElementById("confirmDelete");
var btnCancelDelete = document.getElementById("cancelDelete");
var editObjectiveModal = document.getElementById('editObjectiveModal');
var btnOpenEditObjective = document.getElementById("editObjective");

document.getElementById('btnAddTask').addEventListener('click', function() {
    var objectiveId = this.getAttribute('data-objective-id');
    window.location.href = '/' + objectiveId + '/task_form';
});

btnOpenDeleteObjective.onclick = function() {
    deleteObjectiveModal.style.display = "block";
}

btnOpenEditObjective.onclick = function() {
    editObjectiveModal.style.display = "block";
}

btnConfirmDelete.onclick = function() {
    var objectiveId = document.getElementById('deleteObjective').getAttribute('data-objective-id');
    window.location.href = "/objective/" + objectiveId + "/delete_objective";
}

btnCancelDelete.onclick = function() {
    deleteObjectiveModal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == deleteObjectiveModal) {
        deleteObjectiveModal.style.display = "none";
    }

    if (event.target == editObjectiveModal) {
        editObjectiveModal.style.display = "none";
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