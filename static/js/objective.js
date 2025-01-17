$(function() {
    $(".datepicker").datepicker({
        dateFormat: "dd/mm/yy"
    });
});

function validateDates() {
    var startDateInput = document.getElementById('edit_start_date');
    var endDateInput = document.getElementById('edit_end_date');

    var startDate = new Date(startDateInput.value);
    var endDate = new Date(endDateInput.value);

    // Validar que ambas fechas estén completas
    if (!startDateInput.value || !endDateInput.value) {
        alert('Por favor, complete ambas fechas.');
        return false;
    }

    // Validar que la fecha de finalización no sea anterior a la de inicio
    if (endDate < startDate) {
        alert('La fecha de finalización debe ser mayor o igual a la fecha de inicio.');
        return false;
    }

    return true;
}

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