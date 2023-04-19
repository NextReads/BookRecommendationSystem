const emailField = document.querySelector('#emailField');
const emailFeedbackField = document.querySelector('.invalid-feedback-email');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');


const showPassword = document.querySelector('.showPasswordToggle');
const passwordField1 = document.querySelector('#floatingPassword');

showPassword.addEventListener('click', (e) => {
    if (passwordField1.type === "password") {
        passwordField1.type = "text";
        passwordField2.type = "text";
    } else {
        passwordField1.type = "password";
        passwordField2.type = "password";
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
    
