const spinnerBox = document.querySelector('#spinner-box');
const dataBox = document.querySelector('#data-box');
console.log("spinner",spinnerBox)
console.log("data", dataBox)

//get the response from the server
//while the response is being fetched, show the spinner
//when the response is ready, hide the spinner and show the data
//if there is an error, hide the spinner and show the error message

//window.location.pathname = "/userProfile/recommendations";

//spinnerBox.style.display = "block";
//dataBox.style.display = "none";

// const loadBooks = () => {
//     fetch("/userProfile/recommendations")
//     .then((res) => res.json())
//     .then((data) => {
//         spinnerBox.style.display = "none";
//         dataBox.style.display = "block";
//         if (data.message_error) {
//             dataBox.innerHTML = `<div class="alert alert-danger" role="alert">
//             ${data.error}
//           </div>`;
//         } else {
//             dataBox.innerHTML = data.books;
//         }
//     });
// }

// loadBooks();