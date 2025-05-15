document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("jobseekerForm");

    form.addEventListener("submit", function (event) {
        let isValid = true;

        // Function to show error message and add red border
        function showError(inputId, errorId, message) {
            document.getElementById(errorId).textContent = message;
            document.getElementById(inputId).classList.add("error-border");
            isValid = false;
        }

        // Function to clear error message and remove red border
        function clearError(inputId, errorId) {
            document.getElementById(errorId).textContent = "";
            document.getElementById(inputId).classList.remove("error-border");
        }

        // Clear all previous errors
        document.querySelectorAll(".error-text").forEach(el => el.textContent = "");
        document.querySelectorAll(".error-border").forEach(el => el.classList.remove("error-border"));

        // First Name Validation
        const firstName = document.getElementById("firstname").value.trim();
        if (!/^[A-Za-z]+$/.test(firstName)) {
            showError("firstname", "firstnameError", "⚠ First name should contain only alphabets.");
        } else {
            clearError("firstname", "firstnameError");
        }

        // Last Name Validation
        const lastName = document.getElementById("lastname").value.trim();
        if (!/^[A-Za-z]+$/.test(lastName)) {
            showError("lastname", "lastnameError", "⚠ Last name should contain only alphabets.");
        } else {
            clearError("lastname", "lastnameError");
        }

        // Gender Validation
        const gender = document.getElementById("gender").value;
        if (gender === "") {
            showError("gender", "genderError", "⚠ Please select a gender.");
        } else {
            clearError("gender", "genderError");
        }

        // Date of Birth Validation
        const dob = document.getElementById("dateofbirth").value;
        if (!dob) {
            showError("dateofbirth", "dobError", "⚠ Please enter your date of birth.");
        } else {
            clearError("dateofbirth", "dobError");
        }

        // City Validation
        const city = document.getElementById("city").value;
        if (city === "none") {
            showError("city", "cityError", "⚠ Please select a city.");
        } else {
            clearError("city", "cityError");
        }

        // Address Validation
        const address = document.getElementById("address").value.trim();
        if (address.length < 10) {
            showError("address", "addressError", "⚠ Address must be at least 10 characters long.");
        } else {
            clearError("address", "addressError");
        }

        // Mobile Number Validation
        const mobileNumber = document.getElementById("strmobileno").value.trim();
        if (!/^[6-9]\d{9}$/.test(mobileNumber)) {
            showError("strmobileno", "mobileError", "⚠ Enter a valid 10-digit phone number starting with 6, 7, 8, or 9.");
        } else {
            clearError("strmobileno", "mobileError");
        }

        // Position Validation
        const position = document.getElementById("position").value;
        if (position === "none") {
            showError("position", "positionError", "⚠ Please select a position.");
        } else {
            clearError("position", "positionError");
        }

        // Profile Image Validation
        const profileInput = document.getElementById("profile");
        if (profileInput.files.length === 0) {
            showError("profile", "profileError", "⚠ Please upload a profile image.");
        } else {
            const file = profileInput.files[0];
            const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
            const maxFileSize = 2 * 1024 * 1024; // 2MB

            if (!allowedExtensions.test(file.name)) {
                showError("profile", "profileError", "⚠ Only .jpg, .jpeg, or .png files are allowed.");
            } else if (file.size > maxFileSize) {
                showError("profile", "profileError", "⚠ File size must not exceed 2MB.");
            } else {
                clearError("profile", "profileError");
            }
        }

        // Email Validation
        const email = document.getElementById("stremail").value.trim();
        if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
            showError("stremail", "emailError", "⚠ Enter a valid email address.");
        } else {
            clearError("stremail", "emailError");
        }

        // Password Validation
        const password = document.getElementById("strpass").value.trim();
        const confirmPassword = document.getElementById("confirmpass").value.trim();
        if (!/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password)) {
            showError("strpass", "passwordError", "⚠ Password must be at least 8 characters long and include at least one letter, one number, and one special character.");
        } else {
            clearError("strpass", "passwordError");
        }
        if (password !== confirmPassword) {
            showError("confirmpass", "confirmPasswordError", "⚠ Passwords do not match.");
        } else {
            clearError("confirmpass", "confirmPasswordError");
        }

        // Prevent form submission if invalid
        if (!isValid) {
            event.preventDefault();
        }
    });
});
