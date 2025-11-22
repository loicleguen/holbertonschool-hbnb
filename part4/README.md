<div align= 'center'>
  <img src="images/logo_double.png" style="width:30vw;">
</div>

# 🖥️ HBnB - Simple Web Client

The fourth and final phase introduces a functional front-end built with
**HTML5, CSS3, and JavaScript ES6**, consuming the backend API.

### Goals

-   Build user interface pages (Login, Index, Place Details, Add
    Review).
-   Use Fetch API to interact with backend endpoints.
-   Store and manage JWT tokens using cookies.
-   Provide client-side filtering and dynamic DOM updates.

------------------------------------------------------------------------

## 📚 Table of Contents

[🖥️ HBnB - Simple Web Client](#-hbnb---simple-web-client)
- [1. Design (HTML & CSS)](#1-design-html--css)
- [2. Login (JWT Authentication](#2-login-jwt-authentication)
- [3. Index -- List of Places](#3-index--list-of-places)
- [4. Place Details](#4-place-details)
- [5. Add Review Form](#5-add-review-form)
- [👥 Authors](#-authors)

------------------------------------------------------------------------

### 1. Design (HTML & CSS)

Four fully functional and responsive pages:

-   **login.html**
-   **index.html**
-   **place.html**
-   **add_review.html**

#### Page Components

-   Header with logo and login link\
-   Footer with rights notice\
-   Navigation bar\
-   Semantic HTML5 structure\
-   Responsive layout\
-   W3C-compliant code

#### Sample Components

-   `.place-card`\
-   `.details-button`\
-   `.place-details`\
-   `.place-info`\
-   `.review-card`\
-   `.add-review`

------------------------------------------------------------------------

### 2. Login (JWT Authentication)

The login page authenticates users with their credentials and stores a
JWT token in a cookie.

#### Example Code

``` javascript
async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = "index.html";
  } else {
    const err = await response.text();
    alert("Login failed: " + err);
  }
}
```

------------------------------------------------------------------------

### 3. Index -- List of Places

#### Example Code

``` javascript
function getCookie(name) {
  const matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}()\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

async function fetchPlaces(token) {
  const headers = token ? { "Authorization": `Bearer ${token}` } : {};
  const response = await fetch(`${API_URL}/places`, { headers });
  if (!response.ok) throw new Error("Failed to fetch places");
  const places = await response.json();
  displayPlaces(places);
}
```

------------------------------------------------------------------------

### 4. Place Details

``` javascript
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}
```

------------------------------------------------------------------------

### 5. Add Review Form

``` javascript
async function submitReview(token, placeId, reviewText) {
  const response = await fetch(`${API_URL}/reviews`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ place_id: placeId, text: reviewText })
  });

  if (response.ok) {
    alert("Review submitted successfully!");
  } else {
    const err = await response.text();
    alert("Failed to submit review: " + err);
  }
}
```