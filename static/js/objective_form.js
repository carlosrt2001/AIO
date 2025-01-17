$(document).ready(function() {
    document.getElementById('imageInput').addEventListener('change', previewImage);
});

function previewImage() {
    var file = document.getElementById('imageInput').files[0];
    if (file) {
      var reader = new FileReader();
      reader.onload = function(event) {
        var imagenPreview = document.getElementById('objective_image');
        imagenPreview.src = event.target.result;
        imagenPreview.style.display = 'block';
      };
      reader.readAsDataURL(file);
    }
}

function updatePriorityValue(value) {
        document.getElementById('priorityValue').textContent = value;
}

document.getElementById('formObjective').addEventListener('submit', function(event) {
    var startDate = new Date(document.getElementById('start_date').value);
    var endDate = new Date(document.getElementById('end_date').value);

    if (!startDate || !endDate) {
        alert('Por favor, complete ambas fechas.');
        event.preventDefault();
        return;
    }

    if (endDate < startDate) {
        alert('La fecha de finalización debe ser mayor o igual a la fecha de inicio.');
        event.preventDefault();
    }
});

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