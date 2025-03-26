function filterPosts() {
  const searchInput = document.getElementById("searchBar").value.toLowerCase();
  const elements = document.querySelectorAll(querySelectValue);

  elements.forEach((element) => {
    const elementValues = element.dataset.search.toLowerCase();
    if (elementValues.includes(searchInput)) {
      element.style.display = "block";
    } else {
      element.style.display = "none";
    }
  });
}
