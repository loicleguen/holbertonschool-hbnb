<div align="center">
  <img src="images/logo_double.png" style="width:30vw;">
</div>

# 🖥️ HBnB - Simple Web Client

This fourth and final phase focuses on building a dynamic front-end for HBnB using **HTML5**, **CSS3**, and **JavaScript ES6**. The client interacts with the backend API, providing a seamless user experience for authentication, browsing places, viewing details, and submitting reviews.

---

## 📚 Table of Contents

- [Project Overview](#project-overview)
- [Design & Pages](#design--pages)
- [Login (JWT Authentication)](#login-jwt-authentication)
- [Index: List of Places](#index-list-of-places)
- [Place Details](#place-details)
- [Add Review Form](#add-review-form)
- [Technical Requirements](#technical-requirements)
- [Snippet Video](#snippet-video)
- [Resources](#resources)
- [Author](#author)

---

## Project Overview

**Objectives:**
- Develop a user-friendly interface following provided design specifications.
- Implement client-side functionality to interact with the back-end API.
- Ensure secure and efficient data handling using JavaScript.
- Apply modern web development practices to create a dynamic web application.

**Learning Goals:**
- Apply HTML5, CSS3, and JavaScript ES6 in a real-world project.
- Interact with back-end services using AJAX/Fetch API.
- Implement authentication mechanisms and manage user sessions.
- Use client-side scripting to enhance user experience without page reloads.

---

## Design & Pages

**Pages to implement:**
- `login.html` – Login form for user authentication.
- `index.html` – Main page listing all places.
- `place.html` – Detailed view for a specific place.
- `add_review.html` – Form to add a review for a place.

**Required Structure:**
- **Header:** Application logo (`logo.png`) with class `logo`, login button/link with class `login-button`.
- **Footer:** Text indicating all rights reserved.
- **Navigation Bar:** Links to relevant pages (e.g., index.html, login.html).
- **Cards:** Use `.place-card` for places and `.review-card` for reviews.
- **Details:** Use `.place-details`, `.place-info`, `.details-button`, `.add-review` classes.

**Styling Requirements:**
- Margin: 20px for place and review cards.
- Padding: 10px within cards.
- Border: 1px solid #ddd for cards.
- Border Radius: 10px for cards.
- Color palette, font, images, and favicon are flexible and customizable.
- All pages must be valid on [W3C Validator](https://validator.w3.org/).

---

## Login (JWT Authentication)

- Implements login functionality using the backend API.
- Stores the JWT token returned by the API in a cookie for session management.
- Redirects to the main page (`index.html`) after successful login.
- Displays error messages if login fails.

**Example:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = loginForm.email.value;
      const password = loginForm.password.value;
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
        alert("Login failed: " + await response.text());
      }
    });
  }
});
```

---

## Index: List of Places

- Displays a list of all places as cards.
- Fetches places data from the API and implements client-side filtering by price.
- Shows the login link only if the user is not authenticated.

**Example:**
```javascript
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

---

## Place Details

- Displays detailed information about a place, including host, price, description, amenities, and reviews.
- Fetches place details from the API using the place ID from the URL.
- Shows the add review form only if the user is authenticated.

**Example:**
```javascript
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

async function fetchPlaceDetails(token, placeId) {
  const headers = token ? { "Authorization": `Bearer ${token}` } : {};
  const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
  if (!response.ok) throw new Error("Failed to fetch place details");
  const place = await response.json();
  displayPlaceDetails(place);
}
```

---

## Add Review Form

- Only authenticated users can submit reviews.
- Unauthenticated users are redirected to the index page.
- Sends review data to the API and handles the response.

**Example:**
```javascript
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
    alert("Failed to submit review: " + await response.text());
  }
}
```

---

## Technical Requirements

- Use semantic HTML5 elements for structure.
- Responsive design with CSS3.
- All client-server communication via Fetch API.
- JWT token stored in cookies for session management.
- CORS must be enabled on the backend for API access.
- Client-side form validation and error handling.
- All pages must pass W3C validation.
---

## Snippet Video

Here’s a short video showing how to use HBNB.
[**Video link**](https://youtu.be/fYF85jYeWRg)

---

## Resources

- [HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
- [CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript ES6 Features](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Responsive Web Design Basics](https://web.dev/responsive-web-design-basics/)
- [Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
- [Client-Side Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)

---

## 👥 Author

| Author           | Role      | GitHub                                   | Email                        |
|------------------|-----------|------------------------------------------|------------------------------|
| **Loïc Le Guen** | Developer | [@loicleguen](https://github.com/loicleguen) | 11510@holbertonstudents.com  |


