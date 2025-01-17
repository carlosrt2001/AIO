var logoutModal = document.getElementById('logoutModal');
var deleteAccountModal = document.getElementById('deleteAccountModal');
var editProfileModal = document.getElementById('editProfileModal');
var btnOpenLogout = document.getElementById("logout");
var btnOpenDeleteProfile = document.getElementById("deleteProfile");
var btnOpenEditProfile = document.getElementById('editProfile');
var btnConfirmLogout = document.getElementById("confirmLogout");
var btnCancelLogout = document.getElementById("cancelLogout");
var btnConfirmDelete = document.getElementById("confirmDelete");
var btnCancelDelete = document.getElementById("cancelDelete");
var btnCancelEditProfile = document.getElementById('cancelEditProfile');

btnOpenLogout.onclick = function() {
    logoutModal.style.display = "block";
}

btnConfirmLogout.onclick = function() {
    window.location.href = "/logout";
}

btnCancelLogout.onclick = function() {
    logoutModal.style.display = "none";
}

btnOpenDeleteProfile.onclick = function() {
    deleteAccountModal.style.display = "block";
}

btnConfirmDelete.onclick = function() {
    window.location.href = "/delete_account";
}

btnCancelDelete.onclick = function() {
    deleteAccountModal.style.display = "none";
}

btnOpenEditProfile.onclick = function() {
    editProfileModal.style.display = "block";
}

btnCancelEditProfile.onclick = function() {
    editProfileModal.style.display = "none";
}


document.getElementById('editProfileForm').addEventListener('submit', function(event) {
    var phone = document.getElementById('phone_number').value;

    if (!validatePhone(phone)) {
        event.preventDefault();
        return;
    }
});

function validatePhone(phone) {
    if (phone === "") {
        return true;
    }

    var phoneRegex = /^\d+$/;

    if (!phoneRegex.test(phone)) {
        alert('El número de teléfono solo debe contener números.');
        return false;
    }
    if (phone.length < 9 || phone.length > 15) {
        alert('El número de teléfono debe tener entre 9 y 15 dígitos.');
        return false;
    }

    return true;
}



window.onclick = function(event) {
    if (event.target == logoutModal) {
        logoutModal.style.display = "none";
    }
    if (event.target == deleteAccountModal) {
        deleteAccountModal.style.display = "none";
    }
    if (event.target == editProfileModal) {
        editProfileModal.style.display = "none";
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


