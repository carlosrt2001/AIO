// Delete a notification
var deleteNotificationModal = document.getElementById('deleteNotificationModal');
var btnConfirmDeleteNotification = document.getElementById("confirmDeleteNotification");
var btnCancelDeleteNotification = document.getElementById("cancelDeleteNotification");
var currentNotificationId = null;

document.querySelectorAll('.deleteNotification').forEach(button => {
    button.onclick = function() {
        currentNotificationId = this.getAttribute('data-notification-id');
        deleteNotificationModal.style.display = "block";
    };
});

btnConfirmDeleteNotification.onclick = function() {
    if (currentNotificationId) {
        window.location.href = "/inbox/" + currentNotificationId + "/delete_notification";
    }
};

btnCancelDeleteNotification.onclick = function() {
    deleteNotificationModal.style.display = "none";
    currentNotificationId = null;
};

window.onclick = function(event) {
    if (event.target == deleteNotificationModal) {
        deleteNotificationModal.style.display = "none";
        currentNotificationId = null;
    }
};


// Delete all notifications
var confirmationModal = document.getElementById('confirmationModal');
var openConfirmationModalButton = document.getElementById("openConfirmationModal");
var confirmDeleteAllNotificationsButton = document.getElementById("confirmDeleteAllNotifications");
var cancelDeleteAllNotificationsButton = document.getElementById("cancelDeleteAllNotifications");

openConfirmationModalButton.onclick = function() {
    confirmationModal.style.display = "block";
};

confirmDeleteAllNotificationsButton.onclick = function() {
    document.getElementById("deleteAllNotificationsForm").submit();
};

cancelDeleteAllNotificationsButton.onclick = function() {
    confirmationModal.style.display = "none";
};

window.onclick = function(event) {
    if (event.target == confirmationModal) {
        confirmationModal.style.display = "none";
    }
};

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