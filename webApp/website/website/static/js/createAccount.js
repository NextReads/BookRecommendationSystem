const emailField = document.querySelector('#emailField');
const emailFeedbackField = document.querySelector('.invalid-feedback-email');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');

const usernameField = document.querySelector('#usernameField');
const feedbackField = document.querySelector('.invalid-feedback');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');

const showPassword = document.querySelector('.showPasswordToggle');
const passwordField1 = document.querySelector('#floatingPassword');
const passwordField2 = document.querySelector('#floatingPassword2');
const passwordFeedbackField = document.querySelector('.invalid-feedback-password');

const submitBtn = document.querySelector('.submit-btn');
const formFeedbackField = document.querySelector('.invalid-feedback-form');
usernameValid = false;
emailValid = false;
passwordsMatch = false;

submitBtn.addEventListener('click', (e) => {
    //if empty fields, prevent default
    if (usernameField.value.length == 0
        || emailField.value.length == 0 || passwordField1.value.length == 0 || passwordField2.value.length == 0
        || usernameValid == false || emailValid == false || passwordsMatch == false ) {
        e.preventDefault();
        formFeedbackField.style.display = "block";
        formFeedbackField.style = "color: red";
        formFeedbackField.innerHTML = `<p>Please fill in all fields</p>`;
    }
    
});


passwordField2.addEventListener('keyup', (e) => {
    const passwordVal = e.target.value;
    const passwordVal2 = passwordField1.value;
    if (passwordVal.length > 0) {
        if (passwordVal != passwordVal2) {
            passwordsMatch = false;
            passwordField2.classList.add("is-invalid");
            passwordFeedbackField.style.display = "block";
            passwordFeedbackField.style = "color: red";
            passwordFeedbackField.innerHTML = `<p>Passwords do not match</p>`;
            submitBtn.disabled = true;
        } else {
            passwordsMatch = true;
            passwordField2.classList.remove("is-invalid");
            passwordFeedbackField.style.display = "none";
            if (usernameValid==true && emailValid==true){
            submitBtn.disabled = false;
            }
        }
    }
});

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
            usernameValid=false;
            submitBtn.disabled = true;
            usernameField.classList.add("is-invalid");
            feedbackField.style.display = "block";
            feedbackField.innerHTML = `<p>${data.username_error}</p>`;
          } 
          else{
            usernameValid=true;
            if (emailValid==true && passwordsMatch==true){
            submitBtn.disabled = false;
            }
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
                emailValid=false;
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedbackField.style.display = "block";
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
            }else{
                emailValid=true;
                if (usernameValid==true && passwordsMatch==true){
                submitBtn.disabled = false;
                }
            }
        });
    }
});
    
