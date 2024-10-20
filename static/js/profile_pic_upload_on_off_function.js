// Ensure the page reacts to the checkbox state on page load and when toggled
document.addEventListener('DOMContentLoaded', function () {
    const toggleCheckbox = document.getElementById('toggleProfileImage');
    const uploadDiv = document.getElementById('profileImageUpload');

    // Set initial state based on checkbox status
    toggleProfileImage();

    // Add event listener to toggle the file input when the checkbox is clicked
    toggleCheckbox.addEventListener('change', toggleProfileImage);

    function toggleProfileImage() {
        var checkBox = document.getElementById("toggleProfileImage");
        var fileUploadDiv = document.getElementById("profileImageUpload");
        var profileImageStatus = document.getElementById("profileImageStatus");

        if (checkBox.checked) {
            fileUploadDiv.style.display = "block";
            profileImageStatus.value = "on";  // Profile image toggle is on
        } else {
            fileUploadDiv.style.display = "none";
            profileImageStatus.value = "off";  // Profile image toggle is off
        }
    }
});