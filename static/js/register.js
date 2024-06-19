$(document).ready(function() {
    document.getElementById('imageInput').addEventListener('change', previewImage);
});

function previewImage() {
    var file = document.getElementById('imageInput').files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(event) {
            var imagenPreview = document.getElementById('profile_image');
            imagenPreview.src = event.target.result;
            imagenPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

document.getElementById('formRegister').addEventListener('submit', function(event) {
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var user = document.getElementById('user').value;
    var phone = document.getElementById('phone_number').value;

    if (user.length > 10) {
        alert('El nombre de usuario no debe tener más de 10 caracteres');
        event.preventDefault();
        return;
    }

    if (!validatePhone(phone)) {
        event.preventDefault();
        return;
    }

    if (password1 !== password2) {
        alert('Las contraseñas no coinciden');
        event.preventDefault();
        return;
    }

    if (!validatePassword(password1, user)) {
        event.preventDefault();
    }
});

function validatePhone(phone) {
    if (phone === "") {
            return true;
        }

    var phoneRegex = /^\d+$/;

    if (!phoneRegex.test(phone)) {
        alert('El número de teléfono solo debe contener números');
        return false;
    }
    if (phone.length < 9 || phone.length > 15) {
        alert('El número de teléfono debe tener entre 9 y 15 dígitos');
        return false;
    }

    return true;
}

function validatePassword(password, username) {
    var minLength = 8;
    var hasUpperCase = /[A-Z]/.test(password);
    var hasLowerCase = /[a-z]/.test(password);
    var hasSpecialChar = /[!@#$%^&*(),.?:{}|<>]/.test(password);
    var containsUsername = password.includes(username);

    if (password.length < minLength) {
        alert('La contraseña debe tener al menos 8 caracteres');
        return false;
    }
    if (!hasUpperCase) {
        alert('La contraseña debe tener al menos una letra mayúscula');
        return false;
    }
    if (!hasLowerCase) {
        alert('La contraseña debe tener al menos una letra minúscula');
        return false;
    }
    if (!hasSpecialChar) {
        alert('La contraseña debe tener al menos un símbolo');
        return false;
    }
    if (containsUsername) {
        alert('La contraseña no puede contener el nombre de usuario');
        return false;
    }

    return true;
}

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