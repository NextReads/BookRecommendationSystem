const emailField = document.querySelector('#emailField');
const emailFeedbackField = document.querySelector('.invalid-feedback-email');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');

const usernameField = document.querySelector('#usernameField');
const feedbackField = document.querySelector('.invalid-feedback');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');

const showPassword = document.querySelector('.showPasswordToggle');
const passwordField1 = document.querySelector('#floatingPassword');
const passwordField2 = document.querySelector('#floatingPassword2');

showPassword.addEventListener('click', (e) => {
    if (passwordField1.type === "password") {
        passwordField1.type = "text";
        passwordField2.type = "text";
    } else {
        passwordField1.type = "password";
        passwordField2.type = "password";
    }
});


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = "Checking username...";
    if (usernameVal.length == 0) {
        usernameSuccessOutput.style.display = "none";
    };
    usernameField.classList.remove("is-invalid");
    feedbackField.style.display = "none";
  
    if (usernameVal.length > 0) {
      fetch("/authentication/validate-username", {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          usernameSuccessOutput.style.display = "none";
          if (data.username_error) {
            usernameField.classList.add("is-invalid");
            feedbackField.style.display = "block";
            feedbackField.innerHTML = `<p>${data.username_error}</p>`;
          } 
        });
    }
});
    

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    emailSuccessOutput.style.display = "block";
    emailSuccessOutput.textContent = "Checking email...";
    if (emailVal.length == 0) {
        emailSuccessOutput.style.display = "none";
    };

    emailField.classList.remove("is-invalid");
    emailFeedbackField.style.display = "none";
    
    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
          emailSuccessOutput.style.display = "none";
            if (data.email_error) {
                emailField.classList.add("is-invalid");
                emailFeedbackField.style.display = "block";
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
            } 
        });
    }
});
    
