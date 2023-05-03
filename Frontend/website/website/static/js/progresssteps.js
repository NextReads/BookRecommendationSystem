const progressBar = document.getElementById("progress-bar");
const progressNext = document.getElementById("progress-next");
const progressPrev = document.getElementById("progress-prev");
const skipSteplink = document.getElementsByClassName("actionLink");
const steps = document.querySelectorAll(".step");
let active = 1;
progressNext.addEventListener("click", () => {
    active++;
    if (active > steps.length) {
      active = steps.length;
    }
    if (active == 2){
        window.location.pathname = "/authentication/rate-books-step";
        progressNext.disabled = false;
    }
    if (active == 3){
        window.location.pathname = "/userProfile/userhome";
        progressNext.disabled = false;
    }
    updateProgress();
  });
  
  progressPrev.addEventListener("click", () => {
    active--;
    if (active < 1) {
      active = 1;
    }
    if(active == 1){
        window.location.pathname = "/authentication/set-goal-step";
    }
    updateProgress();
  });

  if(skipSteplink.length > 0){
    skipSteplink[0].addEventListener("click", () => {
        if (active ==1){
        active++;
        if (active > steps.length) {
          active = steps.length;
        }
        updateProgress();
        }
        
      }); 
  }
  
  const updateProgress = () => {
    // toggle active class on list items
    steps.forEach((step, i) => {
      if (i < active) {
        step.classList.add("active");
      } else {
        step.classList.remove("active");
      }
    });
    // set progress bar width  
    progressBar.style.width = 
      ((active - 1) / (steps.length - 1)) * 100 + "%";
    // enable disable prev and next buttons
    if (active === 1) {
      progressPrev.disabled = true;
    } else if (active === steps.length) {
      progressNext.disabled = true;
    } else {
      progressPrev.disabled = false;
      progressNext.disabled = false;
    }
  };
  //upateprogrss if url is /authentication/rate-books-step
  console.log(window.location.pathname )

    if (window.location.pathname == "/authentication/rate-books-step"){
        active = 2;
        updateProgress();
        progressNext.disabled = false;
    }


