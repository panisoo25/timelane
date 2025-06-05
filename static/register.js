document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");

  const fields = {
    first_name: document.getElementById("first_name"),
    last_name: document.getElementById("last_name"),
    email: document.getElementById("email"),
    username: document.getElementById("username"),
    password: document.getElementById("password"),
    confirm_password: document.getElementById("confirm_password"),
  };

  const errors = {
    first_name: document.getElementById("error_first_name"),
    last_name: document.getElementById("error_last_name"),
    email: document.getElementById("error_email"),
    username: document.getElementById("error_username"),
    password: document.getElementById("error_password"),
    confirm_password: document.getElementById("error_confirm_password"),
  };

  function clearErrors() {
    for (let key in errors) {
      errors[key].textContent = "";
    }
  }

  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  function hasUpperCase(str) {
    return /[A-Z]/.test(str);
  }

  function hasSpecialChar(str) {
    return /[!@#$%^&*(),.?":{}|<>]/.test(str);
  }

  function isAlpha(str) {
    return /^[A-Za-z\u0590-\u05FF]+$/.test(str);
  }

  form.addEventListener("submit", (e) => {
    clearErrors();
    let valid = true;

    if (!fields.first_name.value.trim()) {
      errors.first_name.textContent = "This field is required.";
      valid = false;
    } else if (fields.first_name.value.trim().length < 2) {
      errors.first_name.textContent = "First name must be at least 2 characters.";
      valid = false;
    } else if (!isAlpha(fields.first_name.value.trim())) {
      errors.first_name.textContent = "First name must contain letters only.";
      valid = false;
    }

    if (!fields.last_name.value.trim()) {
      errors.last_name.textContent = "This field is required.";
      valid = false;
    } else if (fields.last_name.value.trim().length < 2) {
      errors.last_name.textContent = "Last name must be at least 2 characters.";
      valid = false;
    } else if (!isAlpha(fields.last_name.value.trim())) {
      errors.last_name.textContent = "Last name must contain letters only.";
      valid = false;
    }

    if (!fields.email.value.trim()) {
      errors.email.textContent = "This field is required.";
      valid = false;
    } else if (!validateEmail(fields.email.value.trim())) {
      errors.email.textContent = "Please enter a valid email.";
      valid = false;
    }

    if (!fields.username.value.trim()) {
      errors.username.textContent = "This field is required.";
      valid = false;
    } else if (fields.username.value.trim().length < 2) {
      errors.username.textContent = "Username must be at least 2 characters.";
      valid = false;
    }

    const pwd = fields.password.value;
    if (!pwd) {
      errors.password.textContent = "This field is required.";
      valid = false;
    } else if (pwd.length < 6) {
      errors.password.textContent = "Password must be at least 6 characters.";
      valid = false;
    } else if (!hasUpperCase(pwd)) {
      errors.password.textContent = "Password must include at least one uppercase letter.";
      valid = false;
    } else if (!hasSpecialChar(pwd)) {
      errors.password.textContent = "Password must include at least one special character.";
      valid = false;
    }

    if (fields.confirm_password.value !== pwd) {
      errors.confirm_password.textContent = "Passwords do not match.";
      valid = false;
    }

    if (valid) {
      alert("Registration successful");
    } else {
      e.preventDefault();
    }
  });
});
