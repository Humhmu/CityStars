const titleInput = document.getElementById("title");
const textInput = document.getElementById("text");
const titleCharCount = document.getElementById("title-char-count");
const textCharCount = document.getElementById("text-char-count");
const alertList = document.querySelectorAll(".alert");

document.addEventListener("DOMContentLoaded", function () {
  titleCharCount.textContent = `${titleInput.value.length}/20`;
  textCharCount.textContent = `${textInput.value.length}/500`;
});

titleInput.addEventListener("input", () => {
  const currentLength = titleInput.value.length;
  titleCharCount.textContent = `${currentLength}/20`;
});

textInput.addEventListener("input", () => {
  const currentLength = textInput.value.length;
  textCharCount.textContent = `${currentLength}/500`;
});

alertList.forEach(function (alert) {
  new bootstrap.Alert(alert);
});
