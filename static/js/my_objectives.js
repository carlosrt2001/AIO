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