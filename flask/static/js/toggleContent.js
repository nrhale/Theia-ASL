document.addEventListener("DOMContentLoaded", (event) => {
  document.querySelectorAll(".toggle").forEach((item) => {
    item.addEventListener("click", (event) => {
      let content = item.nextElementSibling;
      content.classList.toggle("hide-content");
    });
  });
});
