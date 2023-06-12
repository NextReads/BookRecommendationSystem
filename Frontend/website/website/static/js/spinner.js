

//get the response from the server
//while the response is being fetched, show the spinner
//when the response is ready, hide the spinner and show the data
//if there is an error, hide the spinner and show the error message


const getRecommendations = () => {
    const spinnerBox = document.querySelector('#spinner-box');
    const dataBox = document.querySelector('#data-box');
    console.log("spinner",spinnerBox)
    console.log("data", dataBox)
    spinnerBox.style.display = "block";
    dataBox.style.display = "none";
    console.log("/userProfile/recommendations")
    fetch("/userProfile/recommendations", {
        method: "GET",
    })
    .then((res) => res.json())
    .then((data) => {
        spinnerBox.style.display = "none";
        dataBox.style.display = "block";
        if (data.message_error) {
            dataBox.innerHTML = `<div class="alert alert-danger" role="alert">
            ${data.error}   
            </div>`;
        } else {
            console.log(data.recommendations)
            dataBox.innerHTML += `
                <div>
                    <h1>Recommended for you!</h1>
                </div>
                <div class="cards-container">
            `
            for (let i = 0; i < data.recommendations.length; i++){
                dataBox.innerHTML += `
                <a href="/userProfile/book/${data.recommendations[i]._id}" style="text-decoration: none;">
                <div class="card shadow p-3 mb-3 bg-body rounded" style="min-width: 300px">
                <div class="inner-card">
                  <img
                  src="${data.recommendations[i].imageUrl}"
                  height="210"
                  width="130" 
                  />
                  <div class="card-body">
                    <h5 class="card-title">#${i}: ${data.recommendations[i].title}</h5>
                    <p class="card-text">
                        Author : ${data.recommendations[i].authors}
                    </p>
                    <p class="card-text">
                      Average book rating : ${data.recommendations[i].avgRating}/5
                    </p>
                  </div>
                </div>
              </div>
             </a>
                `
            }


        }
    });
}
window.onload = getRecommendations();
