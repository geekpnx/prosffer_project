// Function to open file upload when profile image is clicked
function openFileUpload() {
    document.getElementById('fileUpload').click();
}

// Function to toggle profile image usage
function toggleProfileImage() {
    const profileImage = document.getElementById('profileImage');
    const toggle = document.getElementById('toggleProfileImage').checked;

    if (toggle) {
        // Activate profile image
        profileImage.style.display = 'block';
    } else {
        // Deactivate profile image
        profileImage.style.display = 'none';
    }
}