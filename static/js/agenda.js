// Selección de elementos del DOM
const calendar = document.querySelector(".calendar"),
date = document.querySelector(".date"),
daysContainer = document.querySelector(".days"),
prev = document.querySelector(".prev"),
next = document.querySelector(".next"),
todayBtn = document.querySelector(".today-btn"),
gotoBtn = document.querySelector(".goto-btn"),
dateInput = document.querySelector(".date-input"),
eventDay = document.querySelector(".event-day"),
eventDate = document.querySelector(".event-date"),
eventsContainer = document.querySelector(".events"),
addEventBtn = document.querySelector(".add-event"),
addEventWrapper = document.querySelector(".add-event-wrapper"),
addEventCloseBtn = document.querySelector(".close"),
addEventTitle = document.querySelector(".event-name"),
addEventFrom = document.querySelector(".event-time-from"),
addEventTo = document.querySelector(".event-time-to"),
addEventSubmit = document.querySelector(".add-event-btn");

// Variables de estado
let today = new Date();
let activeDay;
let month = today.getMonth();
let year = today.getFullYear();
const eventsArr = [];

// Array de nombres de meses
const months = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

// Inicialización del calendario
function initCalendar() {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const prevLastDay = new Date(year, month, 0);
  const prevDays = prevLastDay.getDate();
  const lastDate = lastDay.getDate();
  const day = (firstDay.getDay() + 6) % 7;
  const nextDays = 7 - lastDay.getDay();

  date.innerHTML = `${months[month]} ${year}`;

  let days = "";

  for (let x = day; x > 0; x--) {
    days += `<div class="day prev-date">${prevDays - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDate; i++) {
    let event = eventsArr.some(eventObj => (
      eventObj.day === i && eventObj.month === month + 1 && eventObj.year === year
    ));

    if (
      i === new Date().getDate() &&
      year === new Date().getFullYear() &&
      month === new Date().getMonth()
    ) {
      activeDay = i;
      getActiveDay(i);
      fetchActivitiesForDate(activeDay, month, year);
      days += event ? `<div class="day today active event">${i}</div>` : `<div class="day today active">${i}</div>`;
    } else {
      days += event ? `<div class="day event">${i}</div>` : `<div class="day">${i}</div>`;
    }
  }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="day next-date">${j}</div>`;
  }

  daysContainer.innerHTML = days;
  addListener();
}

// Funciones para cambiar de mes
function prevMonth() {
  month--;
  if (month < 0) {
    month = 11;
    year--;
  }
  initCalendar();
}

function nextMonth() {
  month++;
  if (month > 11) {
    month = 0;
    year++;
  }
  initCalendar();
}

// Listeners para los botones de navegación
prev.addEventListener("click", prevMonth);
next.addEventListener("click", nextMonth);

// Inicialización del calendario
initCalendar();

// Función para agregar listener a los días
function addListener() {
  const days = document.querySelectorAll(".day");
  days.forEach(day => {
    day.addEventListener("click", e => {
      const clickedDay = Number(e.target.innerHTML);

      days.forEach(d => d.classList.remove("active"));

      if (e.target.classList.contains("prev-date")) {
        prevMonth();
        setTimeout(() => {
          selectDayAfterMonthChange(clickedDay);
        }, 100);
      } else if (e.target.classList.contains("next-date")) {
        nextMonth();
        setTimeout(() => {
          selectDayAfterMonthChange(clickedDay);
        }, 100);
      } else {
        e.target.classList.add("active");
        updateSelectedDay(clickedDay);
      }
    });
  });
}

function selectDayAfterMonthChange(day) {
  const days = document.querySelectorAll(".day");
  days.forEach(d => {
    if (Number(d.innerHTML) === day && !d.classList.contains("prev-date") && !d.classList.contains("next-date")) {
      d.classList.add("active");
      updateSelectedDay(day);
    }
  });
}

function updateSelectedDay(day) {
  activeDay = day;
  getActiveDay(day);
  fetchActivitiesForDate(activeDay, month, year);
}


// Función para obtener actividades de una fecha
function fetchActivitiesForDate(day, month, year) {
  const selectedDate = new Date(year, month, day);
  const formattedDate = selectedDate.toISOString().split('T')[0];
  const day_of_week = getActiveDay(day);

  fetch('/get_events', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ date: formattedDate, day_of_week: day_of_week }),
  })
  .then(response => response.json())
  .then(data => {
    eventsContainer.innerHTML = '';
    data.forEach(activity => {
      const eventElement = document.createElement('div');
      eventElement.classList.add('event');

      eventElement.style.backgroundColor = activity.color;

      const nameElement = document.createElement('div');
      nameElement.classList.add('event-name');
      nameElement.textContent = activity.name;

      const timeElement = document.createElement('div');
      timeElement.classList.add('event-time');
      timeElement.textContent = `${activity.start_time} - ${activity.end_time}`;

      const descriptionElement = document.createElement('div');
      descriptionElement.classList.add('event-description');
      descriptionElement.textContent = activity.description;

      const deleteIcon = document.createElement('i');
      deleteIcon.classList.add('fas', 'fa-trash');
      deleteIcon.addEventListener('click', () => openDeleteModal(activity.id, activity.event_type));

      eventElement.appendChild(nameElement);
      eventElement.appendChild(timeElement);
      eventElement.appendChild(descriptionElement);
      eventElement.appendChild(deleteIcon);

      eventsContainer.appendChild(eventElement);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// Listener para el botón de "hoy"
todayBtn.addEventListener("click", () => {
  today = new Date();
  month = today.getMonth();
  year = today.getFullYear();
  initCalendar();
});

// Formato de entrada de fecha
dateInput.addEventListener("input", e => {
  dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
  if (dateInput.value.length === 2) {
    dateInput.value += "/";
  }
  if (dateInput.value.length > 7) {
    dateInput.value = dateInput.value.slice(0, 7);
  }
  if (e.inputType === "deleteContentBackward" && dateInput.value.length === 3) {
    dateInput.value = dateInput.value.slice(0, 2);
  }
});

// Listener para el botón de ir a una fecha específica
gotoBtn.addEventListener("click", gotoDate);

function gotoDate() {
  const dateArr = dateInput.value.split("/");
  if (dateArr.length === 2 && dateArr[0] > 0 && dateArr[0] < 13 && dateArr[1].length === 4) {
    month = dateArr[0] - 1;
    year = dateArr[1];
    initCalendar();
  } else {
    alert("Invalid Date");
  }
}

// Función para obtener el nombre del día activo y actualizar los elementos correspondientes
function getActiveDay(date) {
  const day = new Date(year, month, date);
  const options = { weekday: 'long' };
  const dayName = day.toLocaleDateString('es-ES', options);
  eventDay.innerHTML = dayName;
  return dayName;
}

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
      // Recargar la página
      location.reload();
    } else {
      // Manejar errores si es necesario
      console.error('Error al actualizar el color de la agenda');
    }
  })
  .catch(error => {
    console.error('Error al actualizar el color de la agenda:', error);
  });
}

// Gestión de modales de actividades y rutinas
var activityModal = document.getElementById('activityModal');
var routineModal = document.getElementById('routineModal');
var btnOpenActivity = document.getElementById("activity");
var btnOpenRoutine = document.getElementById("routine");
var btnConfirmActivity = document.getElementById("confirmActivity");
var btnCancelActivity = document.getElementById("cancelActivity");
var btnConfirmRoutine = document.getElementById("confirmRoutine");
var btnCancelRoutine = document.getElementById("cancelRoutine");

btnOpenActivity.onclick = function() {
  activityModal.style.display = "block";
};

btnConfirmActivity.onclick = function() {
  window.location.href = "/activity_form";
};

btnCancelActivity.onclick = function() {
  activityModal.style.display = "none";
};

btnOpenRoutine.onclick = function() {
  routineModal.style.display = "block";
};

btnConfirmRoutine.onclick = function() {
  window.location.href = "/routine_form";
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




// Variables para el modal de confirmación de eliminación
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

// Función para cerrar el modal de eliminación
function closeDeleteModal() {
  activityToDelete = null;
  eventToDelete = null;
  deleteModal.style.display = 'none';
}

// Agregar event listener para cerrar el modal si se hace clic fuera de él
window.addEventListener('click', function(event) {
  if (event.target === deleteModal) {
    closeDeleteModal();
  }
});


// Evento para cancelar eliminación
cancelDeleteBtn.addEventListener('click', closeDeleteModal);

// Evento para confirmar eliminación
confirmDeleteBtn.addEventListener('click', function() {
  if (activityToDelete) {
    fetch(`/event/${eventToDelete}/${activityToDelete}/delete_event`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id: activityToDelete })
    })
    .then(response => {
      if (response.ok) {
        closeDeleteModal();
        fetchActivitiesForDate(activeDay, month, year);
      } else {
        response.json().then(data => alert('Error: ' + data.error));
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al eliminar la actividad');
    });
  }
});



function addSchedule() {
    var newSchedule = document.querySelector('.schedule').cloneNode(true);
    document.getElementById('schedules').appendChild(newSchedule);
}

function removeSchedule() {
    var schedules = document.getElementById('schedules');
    if (schedules.children.length > 1) {
        schedules.removeChild(schedules.lastChild);
    } else {
        alert("Debe haber al menos un día en el horario.");
    }
}

