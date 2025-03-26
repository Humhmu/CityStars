function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    city: params.get("city") ? params.get("city") : "all",
    country: params.get("country") ? params.get("country") : "all",
  };
}

function setFiltersFromQueryParams() {
  const { city, country } = getQueryParams();
  console.log(city, country);

  const filterCountry = document.getElementById("countryDropdown");
  if (country !== "all") {
    filterCountry.value = country;
  }

  const filterCity = document.getElementById("cityDropdown");
  if (city !== "all") {
    filterCity.value = city;
  }

  filterPosts();
}

function filterPosts() {
  const searchInput = document.getElementById("searchBar").value.toLowerCase();
  const filterCountry = document
    .getElementById("countryDropdown")
    .value.toLowerCase();
  const filterCity = document
    .getElementById("cityDropdown")
    .value.toLowerCase();
  const posts = document.querySelectorAll(".feedpostt");

  posts.forEach((post) => {
    const postContentTitle = post.dataset.postContent.toLowerCase();
    const postContentCountry = post.dataset.country.toLowerCase();
    const postContentCity = post.dataset.city.toLowerCase();
    if (
      postContentTitle.includes(searchInput) &&
      (postContentCountry.includes(filterCountry) || filterCountry === "all") &&
      (postContentCity.includes(filterCity) || filterCity === "all")
    ) {
      post.style.display = "block";
    } else {
      post.style.display = "none";
    }
  });
}

window.onload = setFiltersFromQueryParams();
