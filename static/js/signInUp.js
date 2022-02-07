const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const message = document.querySelectorAll(".message");

sign_up_btn.addEventListener("click", () => {
  if (message){
    message.forEach((msg)=>{
      msg.remove()
    })
  }
  container.classList.add("sign-in-activate");

});

sign_in_btn.addEventListener("click", () => {
  if (message){
    message.forEach((msg)=>{
      msg.remove()
    })
  }
  container.classList.remove("sign-in-activate");
});