document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("cmpForm");

    form.addEventListener("submit", function (event) {
        let isValid = true;

        // Clear previous error messages
        document.querySelectorAll(".error-text").forEach((el) => el.textContent = "");

        // Business Name Validation
        const cmpname = document.getElementById("cmpname").value.trim();
        const cmpnameError = document.getElementById("cmpnameError");
        if (!/^[A-Za-z\s]{3,}$/.test(cmpname)) {
            cmpnameError.textContent = "⚠ Business name must be at least 3 letters.";
            isValid = false;
        }

        // Email Validation
        const email = document.getElementById("stremail").value.trim();
        const emailError = document.getElementById("emailError");
        if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
            emailError.textContent = "⚠ Enter a valid email address.";
            isValid = false;
        }

        // Address Validation
        const address = document.getElementById("address").value.trim();
        const addressError = document.getElementById("addressError");
        if (address.length < 10) {
            addressError.textContent = "⚠ Address must be at least 10 characters.";
            isValid = false;
        }

        // Website URL Validation
        const website = document.getElementById("website").value.trim();
        const websiteError = document.getElementById("websiteError");
        if (!/^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/[\w-]*)*$/.test(website)) {
            websiteError.textContent = "⚠ Enter a valid website URL.";
            isValid = false;
        }

        // Password Validation
        const password = document.getElementById("strpass").value.trim();
        const confirmPassword = document.getElementById("confirmpass").value.trim();
        const passwordError = document.getElementById("passwordError");
        const confirmPasswordError = document.getElementById("confirmPasswordError");

        if (!/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password)) {
            passwordError.textContent = "⚠ Password must have at least 8 characters, 1 letter, 1 number, and 1 special character.";
            isValid = false;
        }
        if (password !== confirmPassword) {
            confirmPasswordError.textContent = "⚠ Passwords do not match.";
            isValid = false;
        }

        // Contact Number Validation
        const contact = document.getElementById("strmobileno").value.trim();
        const contactError = document.getElementById("contactError");
        if (!/^[6-9]\d{9}$/.test(contact)) {
            contactError.textContent = "⚠ Enter a valid 10-digit number (starting with 6, 7, 8, or 9).";
            isValid = false;
        }

        // Prevent form submission if invalid
        if (!isValid) {
            event.preventDefault();
        }
    });
});
