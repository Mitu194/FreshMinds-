const inputs = document.querySelectorAll('.otp-input');

inputs.forEach((input, index) => {
  input.addEventListener('input', () => {
    if (input.value.length === 1 && index < inputs.length - 1) {
      inputs[index + 1].focus();
    }
});

input.addEventListener('keydown', (event) => {
    if (event.key === 'Backspace' && index > 0 && input.value === '') {
      inputs[index - 1].focus();
    }
  });
});
/*password validation*///signup
function validationform() {
  const firstName = document.getElementById("fname").value;
  const lastName = document.getElementById("lname").value;
  const message1 = document.getElementById("message1");
  const namePattern = /^[A-Za-z]+$/; // Regular expression to match only alphabets
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmpassword").value;
  const message = document.getElementById("message");
  const contactNumber = document.getElementById('contactNumber').value;
  const error = document.getElementById('message2');
  // Regular expression for validating contact number (10 digits)
  const regex = /^[0-9]{10}$/;

  //name
  if (!namePattern.test(firstName) || !namePattern.test(lastName)) 
  {
    message1.textContent="Name should contain only alphabets.";
    return false;
  }

  //contact number
  if (!regex.test(contactNumber)) 
  {
    error.textContent = "Enter valid contact number."; // Show error message
    return false; // Prevent form submission
  } 

  // Minimum password length requirement
  if (password.length < 6) 
  {
    message.textContent = "Password must be at least 6 characters long.";
    return false;
  }

  // Check if passwords match
  if (password !== confirmPassword) 
  {
     message.textContent = "Passwords do not match.";
     // return false;
  }

  else
  {
    message.textContent = "";
    message1.textContent = "";
    error.textContent = "";
    //alert("Form submitted successfully!");
    return true;
  }
}

function validationform1()//login
{
  const password = document.getElementById("password").value;
  let username = document.getElementById("username").value;
  let usernameError = document.getElementById("usernameError");
  let valid = true;
  usernameError.textContent = "";
  

  if (username.length < 3 || username.length > 15) 
  {
    usernameError.textContent = "Username must be between 3 and 15 characters.";
    valid = false;
  }

  const usernameRegex = /^[a-zA-Z0-9_]+$/;
  if (!usernameRegex.test(username)) 
  {
    usernameError.textContent = "Username can only contain letters, numbers, or underscores.";
    valid = false;
  }

  /*password*/
  if (password.length < 6) 
  {
    message.textContent = "Password must be at least 6 characters long.";
    return false;
  }
  else
  {
    message.textContent = "";
    username.textContent = "";
    return true;
  }
}

function passwordvarification()
{
    const psw = document.getElementById("password").value;
    const confirmPsw = document.getElementById("confirmpassword").value;
    const message = document.getElementById("message");
  
    // Check password length
    if (psw.length < 8) {
      message.textContent = "Password must be at least 8 characters long.";
      return false;
    }
  
    // Check if passwords match
    if (psw !== confirmPsw) {
      message.textContent = "Passwords do not match.";
      return false;
    }
  
    // Clear any previous error messages if validation passes
    message.textContent = "";
    alert("Password set successfully!");
    return true;  
}

//otp varification
const inputs1 = document.querySelectorAll('.otp-input');

inputs.forEach((input, index) => {
  // Allow only numeric input
  input.addEventListener('input', (event) => {
    const value = event.target.value;
    // If input is not a number, clear the input
    if (isNaN(value) || value === ' ') {
      event.target.value = ''; 
    } else if (value.length === 1 && index < inputs.length - 1) {
      // Move focus to the next input field if a digit is entered
      inputs[index + 1].focus();
    }
  });

  input.addEventListener('keydown', (event) => {
    // Move focus back on backspace if the input is empty
    if (event.key === 'Backspace' && index > 0 && input.value === '') {
      inputs[index - 1].focus();
    }
  });
});
