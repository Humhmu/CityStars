function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  const dets = params.get("city") ? params.get("city").split("_") : null;
  return {
    city: dets ? dets[0] : "-",
    cityId: dets ? dets[1] : "-",
  };
}

function a() {
  const { city, cityId } = getQueryParams();
  addTo.innerHTML = "Add post to " + city;
  if (city === "-") {
    addTo.style.display = "none";
    cityChoice.style.display = "block";
  } else {
    form.setAttribute("action", window.location.href);
    addTo.style.display = "block";
    cityChoice.style.display = "none";
    var option = document.createElement("option");
    option.setAttribute("selected", null);
    option.setAttribute("value", cityId);
    citySelect.appendChild(option);
  }
}

const titleInput = document.getElementById("title");
const textInput = document.getElementById("text");
const titleCharCount = document.getElementById("title-char-count");
const textCharCount = document.getElementById("text-char-count");
const alertList = document.querySelectorAll(".alert");

const imageInput = document.querySelector('input[type="file"]');
const imagePreview = document.getElementById("image-preview");
const imagePreviewContainer = document.getElementById(
  "image-preview-container"
);

const addTo = document.getElementById("add-to");
const cityChoice = document.getElementById("city-choice");
const citySelect = document.getElementById("city");
const form = document.getElementById("post_form");

window.onload = a();

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

imageInput.addEventListener("change", function (event) {
  const file = event.target.files[0];

  if (file && file.type.startsWith("image/")) {
    const imageUrl = URL.createObjectURL(file);

    imagePreview.src = imageUrl;
    imagePreviewContainer.style.display = "block";
  } else {
    imagePreviewContainer.style.display = "none";
  }
});

alertList.forEach(function (alert) {
  new bootstrap.Alert(alert);
});
