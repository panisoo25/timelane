document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
  
    const usernameField = document.getElementById("username");
    const passwordField = document.getElementById("password");
  
    const errorUsername = document.getElementById("error_username");
    const errorPassword = document.getElementById("error_password");
  
    function clearErrors() {
      errorUsername.textContent = "";
      errorPassword.textContent = "";
    }
  
    form.addEventListener("submit", (e) => {
      clearErrors();
      let valid = true;
  
      if (!usernameField.value.trim()) {
        errorUsername.textContent = "Username is required.";
        valid = false;
      } else if (usernameField.value.trim().length < 2) {
        errorUsername.textContent = "Username must be at least 2 characters.";
        valid = false;
      }
  
      if (!passwordField.value) {
        errorPassword.textContent = "Password is required.";
        valid = false;
      } else if (passwordField.value.length < 6) {
        errorPassword.textContent = "Password must be at least 6 characters.";
        valid = false;
      }
  
      if (!valid) {
        e.preventDefault();
      }
    });
  });
  