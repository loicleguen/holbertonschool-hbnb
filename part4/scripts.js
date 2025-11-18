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
    console.log('🚪 Logging out...');
    deleteCookie('token');
    alert('You have been logged out successfully.');
    window.location.href = 'index.html';
}

/**
 * Updates header links based on authentication status
 * Shows/hides Login and Logout buttons
 */
function updateHeaderLinks() {
    // Use class selector to match your HTML structure
    const loginButton = document.querySelector('.login-button');
    const logoutButton = document.getElementById('logout-button');
    const token = getCookie('token');

    if (token) {
        // User is authenticated - hide Login, show Logout
        if (loginButton) loginButton.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';
        console.log('🔓 Header updated: User authenticated');
    } else {
        // User is NOT authenticated - show Login, hide Logout
        if (loginButton) loginButton.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
        console.log('🔒 Header updated: User not authenticated');
    }
}

// ========================================
// LOGIN FUNCTIONALITY
// ========================================

document.addEventListener('DOMContentLoaded', () => {

    // UPDATE HEADER LINKS (ALL PAGES)
    updateHeaderLinks();

    // LOGOUT BUTTON CLICK EVENT
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

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

    // PLACE DETAILS PAGE - Get Place ID
    const placeInfo = document.querySelector('.place-info');
    if (placeInfo) {
        const placeId = getPlaceIdFromURL();
        console.log('🔍 Place ID from URL:', placeId);
        
        if (!placeId) {
            console.error('❌ No Place ID found in URL');
            placeInfo.innerHTML = `
                <div class="error-message">
                    <h2>Invalid Place</h2>
                    <p>No place ID provided in the URL.</p>
                    <a href="index.html" class="button">Back to Home</a>
                </div>
            `;
            return;
        }
        
        console.log('✅ Place ID successfully extracted:', placeId);

        // Check authentication
        checkAuthenticationForPlace();

        fetchPlaceDetails(placeId);
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
        <option value="200">Up to $200</option>
        <option value="300">Up to $300</option>
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

/**
 * Extract the place ID from the URL query parameters
 * Example URL: place.html?id=abc-123-def-456
 * Returns: "abc-123-def-456"
 */
function getPlaceIdFromURL() {
    // Get the query string from the URL (e.g., "?id=abc-123")
    const params = new URLSearchParams(window.location.search);
    
    // Extract the 'id' parameter
    const placeId = params.get('id');
    
    if (!placeId) {
        console.error('No place ID found in URL');
        return null;
    }
    
    return placeId;
}

// ========================================
// Authentication Functions for Place Details
// ========================================

/**
 * Check if the user is authenticated for the place details page
 * Show/hide the "Add Review" button based on authentication status
 * @returns {string|null} - JWT token if authenticated, null otherwise
 */
function checkAuthenticationForPlace() {
    const token = getCookie('token');
    const addReviewButton = document.getElementById('add-review-button');
    
    if (!token) {
        console.log('🔒 User not authenticated - Add Review button hidden');
        if (addReviewButton) {
            addReviewButton.style.display = 'none';
        }
        return null;
    } else {
        console.log('🔓 User authenticated - Add Review button visible');
        if (addReviewButton) {
            addReviewButton.style.display = 'block';
        }
        return token;
    }
}


/**
 * Fetch the details of a specific place from the API
 * @param {string} placeId - The UUID of the place
 */
async function fetchPlaceDetails(placeId) {
    try {
        console.log('🌐 Fetching place details for ID:', placeId);
        
        // Get JWT token from cookies (if available)
        const token = getCookie('token');
        
        // Prepare request headers
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Include JWT token in Authorization header if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
            console.log('🔑 Request with authentication token');
        } else {
            console.log('🔓 Request without authentication token');
        }
        
        // Make GET request to fetch place details
        const response = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });
        
        // Handle HTTP errors
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Place not found');
            } else if (response.status === 401) {
                throw new Error('Unauthorized - Please login');
            } else if (response.status === 403) {
                throw new Error('Forbidden - Access denied');
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        }
        
        // Parse JSON response
        const place = await response.json();
        
        console.log('✅ Place details fetched successfully:', place);
        
        // Step 4: Display the place details on the page (next step)
        displayPlaceDetails(place);
        
    } catch (error) {
        console.error('❌ Error fetching place details:', error);
        
        // Display error message to user
        const placeInfo = document.querySelector('.place-info');
        placeInfo.innerHTML = `
            <div class="error-message">
                <h2>Error Loading Place</h2>
                <p>${error.message}</p>
                <a href="index.html" class="button">⬅️ Back to Home</a>
            </div>
        `;
    }
}
