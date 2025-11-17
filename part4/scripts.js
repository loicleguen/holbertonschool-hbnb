/* 
  HBnB Client-Side Scripts
*/

// API Configuration
const API_URL = 'http://localhost:5000/api/v1'; // Update according to your API URL

// ========================================
// UTILITY FUNCTIONS - Cookie Management
// ========================================

/**
 * Retrieves the value of a cookie by its name
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Sets a cookie
 */
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

/**
 * Deletes a cookie
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
}

/**
 * Checks if the user is authenticated (simple version)
 * @returns {boolean} true if a token exists, false otherwise
 */
function isAuthenticated() {
    const token = getCookie('token');
    return token !== null;
}

/**
 * Logout function
 */
function logout() {
    deleteCookie('token');
    window.location.href = 'login.html';
}

// ========================================
// LOGIN FUNCTIONALITY
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // LOGIN PAGE
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Retrieve form values
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            
            // Client-side validation
            if (!email || !password) {
                displayError('Please enter both email and password.');
                return;
            }
            
            // Call the login function
            await loginUser(email, password);
        });
    }

    // INDEX PAGE - List of Places
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthenticationAndFetchPlaces();
        initializePriceFilter();
    }
});

/**
 * API login function
 */
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            
            // Store JWT token in a cookie
            setCookie('token', data.access_token, 7); // Cookie valid for 7 days
            
            // Redirect to the main page
            window.location.href = 'index.html';
        } else {
            // Handle HTTP errors
            const errorData = await response.json();
            const errorMessage = errorData.message || response.statusText;
            displayError(`Login failed: ${errorMessage}`);
        }
    } catch (error) {
        // Handle network errors
        console.error('Login error:', error);
        displayError('Network error. Please check your connection and try again.');
    }
}

/**
 * Displays an error message
 */
function displayError(message) {
    // Remove old errors
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Create and display the new error message
    const loginForm = document.getElementById('login-form');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.color = 'red';
    errorDiv.style.marginTop = '1rem';
    errorDiv.style.padding = '0.5rem';
    errorDiv.style.backgroundColor = '#ffe6e6';
    errorDiv.style.border = '1px solid red';
    errorDiv.style.borderRadius = '5px';
    
    loginForm.insertBefore(errorDiv, loginForm.firstChild);
    
    // Remove the error after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// ========================================
// INDEX PAGE - List of Places
// ========================================

/**
 * Checks authentication and manages index page display
 */
function checkAuthenticationAndFetchPlaces() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        // User not authenticated - show login link
        if (loginLink) {
            loginLink.style.display = 'block';
        }
        fetchPlaces();
    } else {
        // User authenticated - hide login link
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        fetchPlaces(token);
    }
}

/**
 * Fetches the list of places from the API
 */
async function fetchPlaces(token = null) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        // Add Authorization header if token is provided
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            // Store places globally for filtering
            window.allPlaces = places;
        } else {
            console.error('Failed to fetch places:', response.statusText);
            const placesList = document.getElementById('places-list');
            placesList.innerHTML = '<p>Error loading places. Please try again later.</p>';
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        const placesList = document.getElementById('places-list');
        placesList.innerHTML = '<p>Network error. Please check your connection.</p>';
    }
}

/**
 * Displays the list of places
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    
    placesList.innerHTML = '';

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        
        // Adapt to API field names: title instead of name, price instead of price_per_night
        const placeName = place.title || 'Unnamed Place';
        const placePrice = place.price || 0;
        const placeDescription = place.description || 'No description available.';
        const placeLocation = `GPS: ${place.latitude?.toFixed(4) || '?'}°, ${place.longitude?.toFixed(4) || '?'}°`;
        
        placeCard.dataset.price = placePrice;

        placeCard.innerHTML = `
            <h3>${placeName}</h3>
            <p><strong>Price:</strong> $${placePrice} per night</p>
            <p><strong>Location:</strong> ${placeLocation}</p>
            <p>${placeDescription}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

/**
 * Initializes the price filter
 */
function initializePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    
    if (!priceFilter) return;

    // Populate filter options
    priceFilter.innerHTML = `
        <option value="">All</option>
        <option value="10">Up to $10</option>
        <option value="50">Up to $50</option>
        <option value="100">Up to $100</option>
    `;

    // Add event listener for filtering
    priceFilter.addEventListener('change', (event) => {
        filterPlacesByPrice(event.target.value);
    });
}

/**
 * Filters places by price (client-side)
 */
function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseFloat(card.dataset.price);

        if (maxPrice === '' || maxPrice === 'All') {
            // Show all places
            card.style.display = 'block';
        } else {
            // Show only places within the price range
            if (price <= parseFloat(maxPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}