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