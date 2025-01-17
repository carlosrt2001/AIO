document.getElementById('btnAddObjective').addEventListener('click', function() {
    window.location.href = '/objective_form';
});

var buttonsObjective = document.querySelectorAll('.btnObjective');
buttonsObjective.forEach(function(button) {
    button.addEventListener('click', function() {
        var objectiveId = this.getAttribute('data-id');
        window.location.href = '/objective/' + objectiveId;
    });
});

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