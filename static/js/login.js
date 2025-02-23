// Get information submitted in the form by the user
document.getElementById('formLogin').addEventListener('submit', function(event) {
    var user = document.getElementById('user').value;
    var password = document.getElementById('password').value;
});

// Toggle the visibility of the password
function togglePassword(inputId, eyeId) {
    var passwordInput = document.getElementById(inputId);
    var eyeIcon = document.getElementById(eyeId);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    }
}

// Open modal window with help information to log in
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