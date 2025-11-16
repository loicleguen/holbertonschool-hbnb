/* 
  HBnB Client-Side Scripts
*/

// Configuration de l'API
const API_URL = 'http://localhost:5000/api/v1'; // Modifiez selon votre URL d'API

// ========================================
// UTILITY FUNCTIONS - Gestion des cookies
// ========================================

/**
 * Récupère la valeur d'un cookie par son nom
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Définit un cookie
 */
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

/**
 * Supprime un cookie
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`;
}

/**
 * Vérifie si l'utilisateur est authentifié
 */
function checkAuthentication() {
    const token = getCookie('token');
    return token !== null;
}

// ========================================
// LOGIN FUNCTIONALITY
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Récupérer les valeurs du formulaire
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            
            // Validation côté client
            if (!email || !password) {
                displayError('Please enter both email and password.');
                return;
            }
            
            // Appel à la fonction de login
            await loginUser(email, password);
        });
    }
});

/**
 * Fonction de connexion à l'API
 */
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            
            // Stocker le token JWT dans un cookie
            setCookie('token', data.access_token, 7); // Cookie valide 7 jours
            
            // Rediriger vers la page principale
            window.location.href = 'index.html';
        } else {
            // Gérer les erreurs HTTP
            const errorData = await response.json();
            const errorMessage = errorData.message || response.statusText;
            displayError(`Login failed: ${errorMessage}`);
        }
    } catch (error) {
        // Gérer les erreurs réseau
        console.error('Login error:', error);
        displayError('Network error. Please check your connection and try again.');
    }
}

/**
 * Affiche un message d'erreur
 */
function displayError(message) {
    // Supprimer les anciennes erreurs
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Créer et afficher le nouveau message d'erreur
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
    
    // Supprimer l'erreur après 5 secondes
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

/**
 * Fonction de déconnexion
 */
function logout() {
    deleteCookie('token');
    window.location.href = 'login.html';
}