$(function() {
    $(".datepicker").datepicker({
        dateFormat: "dd/mm/yy"
    });
});

function validateDates() {
    var start_date = $("#start_date").datepicker("getDate");
    var end_date = $("#end_date").datepicker("getDate");

    if (start_date > end_date) {
        alert("La fecha de inicio no puede ser mayor que la fecha de fin.");
        return false;
    }
    return true;
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