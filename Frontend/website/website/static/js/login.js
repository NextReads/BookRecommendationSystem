
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


    
