//agency_info.html
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("agencyForm");

  form.addEventListener("submit", function (event) {
      let errorMessage = "";
      let isValid = true; // Track if form is valid

      // Agency Name Validation
      const agcname = document.getElementById("bsname").value.trim();
      const namePattern = /^[A-Za-z\s]{3,}$/;
      if (!namePattern.test(agcname)) {
          errorMessage += "Agency name should only contain letters and be at least 3 characters long.\n";
          isValid = false;
      }

      // Contact Number Validation
      const contactno = document.getElementById("bscontactno").value.trim();
      const phonePattern = /^[6-9]\d{9}$/;
      if (!phonePattern.test(contactno)) {
          errorMessage += "Enter a valid 10-digit phone number starting with 6, 7, 8, or 9.\n";
          isValid = false;
      }

      // Email Validation
      const email = document.getElementById("bsemail").value.trim();
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailPattern.test(email)) {
          errorMessage += "Enter a valid email address.\n";
          isValid = false;
      }

      // Address Validation
      const address = document.getElementById("bsaddress").value.trim();
      if (address.length < 10) {
          errorMessage += "Address should be at least 10 characters long.\n";
          isValid = false;
      }

      // URL Validation
      const url = document.getElementById("bsurl").value.trim();
      const urlPattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]{2,}(\/[\w-]*)*$/;
      if (!urlPattern.test(url)) {
          errorMessage += "Enter a valid URL starting with http:// or https://\n";
          isValid = false;
      }

      // File Upload Validation
      const fileInput = document.getElementById("bsinputGroupFile04");
      const allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
      const maxFileSize = 2 * 1024 * 1024;

      if (fileInput.files.length === 0) {
          errorMessage += "Please select an image file.\n";
          isValid = false;
      } else {
          let file = fileInput.files[0];
          if (!allowedExtensions.test(file.name)) {
              errorMessage += "Only .jpg, .jpeg, or .png files are allowed.\n";
              isValid = false;
          }
          if (file.size > maxFileSize) {
              errorMessage += "File size must not exceed 2MB.\n";
              isValid = false;
          }
      }

      // Password Validation
      const password = document.getElementById("strpass").value.trim();
        const confirmPassword = document.getElementById("confirmpass").value.trim();
        const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (!passwordPattern.test(password)) {
            errorMessage += "Password must be at least 8 characters long and include at least one letter, one number, and one special character.\n";
            isValid = false;
        }

        // Confirm Password Validation
        if (password !== confirmPassword) {
            errorMessage += "Passwords do not match.\n";
            isValid = false;
        }

      // If there are errors, prevent form submission
      if (!isValid) {
          alert(errorMessage);
          event.preventDefault(); // Stop form submission
      } else {
          // Redirect to another page if all validations pass
          window.location.href = "/login"; // Change to your success page
          event.preventDefault(); // Prevent default form submission to allow redirection
      }
  });
});
