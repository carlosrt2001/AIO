// Update agenda color
function updateAgendaColor(newColor) {
  fetch('/update_agenda_color', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ color: newColor }),
  })
  .then(response => {
    if (response.ok) {
      location.reload();
    } else {
      console.error('Error al actualizar el color de la agenda');
    }
  })
  .catch(error => {
    console.error('Error al actualizar el color de la agenda:', error);
  });
}


// Add activity and routine modal windows
var activityModal = document.getElementById('activityModal');
var routineModal = document.getElementById('routineModal');
var btnOpenActivity = document.getElementById("activity");
var btnOpenRoutine = document.getElementById("routine");
var btnConfirmActivity = document.getElementById("confirmActivity");
var btnCancelActivity = document.getElementById("cancelActivity");
var btnConfirmRoutine = document.getElementById("confirmRoutine");
var btnCancelRoutine = document.getElementById("cancelRoutine");


// Validate the data introduced in the activity form
function validateActivityForm() {
  var activityName = document.getElementById('activity-name').value;
  var activityDate = document.getElementById('activity-date').value;
  var activityStartTime = document.getElementById('activity-startTime').value;
  var activityEndTime = document.getElementById('activity-endTime').value;

  if (!activityName || !activityDate || !activityStartTime || !activityEndTime) {
    return false;
  }

  return true;
}


// Validate the data introduced in the routine form
function validateRoutineForm(event) {
    const routineName = document.getElementById('routine-name').value.trim();
    const scheduleSelects = document.querySelectorAll('select[name="day_of_week[]"]');
    const scheduleStartTimes = document.querySelectorAll('input[name="start_time[]"]');
    const scheduleEndTimes = document.querySelectorAll('input[name="end_time[]"]');
    const routineDescription = document.getElementById('routine-description').value.trim();

    if (!routineName || routineDescription.trim() === '' || scheduleSelects.length === 0 || routineDescription === '') {
        event.preventDefault();
    } else {
        let allSchedulesValid = true;
        for (let i = 0; i < scheduleSelects.length; i++) {
            if (!scheduleSelects[i].value || !scheduleStartTimes[i].value || !scheduleEndTimes[i].value) {
                allSchedulesValid = false;
                break;
            }
        }
        if (!allSchedulesValid) {
            event.preventDefault();
        }
    }
}


btnOpenActivity.onclick = function() {
  activityModal.style.display = "block";
};

btnConfirmActivity.onclick = function() {
  if (validateActivityForm()) {
    window.location.href = "/activity_form";
  }
};

btnCancelActivity.onclick = function() {
  activityModal.style.display = "none";
};

btnOpenRoutine.onclick = function() {
  routineModal.style.display = "block";
};

btnConfirmRoutine.onclick = function() {
  if (validateRoutineForm()) {
    window.location.href = "/routine_form";
  }
};

btnCancelRoutine.onclick = function() {
  routineModal.style.display = "none";
};


window.onclick = function(event) {
  if (event.target == activityModal) {
    activityModal.style.display = "none";
  }
  if (event.target == routineModal) {
    routineModal.style.display = "none";
  }
};


// Delete an event from the agenda
var deleteModal = document.getElementById('deleteActivityModal');
var confirmDeleteBtn = document.getElementById('confirmDelete');
var cancelDeleteBtn = document.getElementById('cancelDelete');
var activityToDelete = null;
var eventToDelete = null;

function openDeleteModal(activityId, eventType) {
  activityToDelete = activityId;
  eventToDelete = eventType;
  deleteModal.style.display = 'block';
}

function closeDeleteModal() {
  activityToDelete = null;
  eventToDelete = null;
  deleteModal.style.display = 'none';
}

window.addEventListener('click', function(event) {
  if (event.target === deleteModal) {
    closeDeleteModal();
  }
});

cancelDeleteBtn.addEventListener('click', closeDeleteModal);

confirmDeleteBtn.addEventListener('click', function(event) {
  event.preventDefault();

  if (activityToDelete) {
    fetch(`/event/${eventToDelete}/${activityToDelete}/delete_event`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id: activityToDelete })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        closeDeleteModal();
        location.reload();
        document.getElementById(`activity-${activityToDelete}`).remove();
      }
    })
  }
});


// Add a day and schedule to a routine
function addSchedule() {
    var newSchedule = document.querySelector('.schedule').cloneNode(true);
    document.getElementById('schedules').appendChild(newSchedule);
}

// Remove an added day and schedule from a routine
function removeSchedule() {
    var schedules = document.getElementById('schedules');
    if (schedules.children.length > 1) {
        schedules.removeChild(schedules.lastChild);
    } else {
        alert("Debe haber al menos un día en el horario.");
    }
}

// Open modal window
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


// Allocated tasks checkbox to toggle if it's completed
document.querySelectorAll('.task-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const taskId = this.getAttribute('data-task-id');
        const isChecked = this.checked;

        fetch(`/task/${taskId}/toggle_completed`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed: isChecked })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Task updated successfully:', data);
            } else {
                console.log('Error updating task:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
