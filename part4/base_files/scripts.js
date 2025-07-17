// Utility functions
function setCookie(name, value, days) {
  let expires = '';
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = '; expires=' + date.toUTCString();
  }
  document.cookie = name + '=' + (value || '') + expires + '; path=/';
}

function getCookie(name) {
  const nameEQ = name + '=';
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

function eraseCookie(name) {
  document.cookie = name + '=; Max-Age=-99999999;';
}

const API_BASE = 'http://127.0.0.1:5000/api/v1';

// API helpers
async function apiRequest(endpoint, method = 'GET', data = null, token = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = 'Bearer ' + token;
  const options = { method, headers };
  if (data) options.body = JSON.stringify(data);
  console.log(API_BASE + endpoint);
  const res = await fetch(API_BASE + endpoint, options);
  return res;
}

// Login logic
async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  try {
    const res = await apiRequest('/auth/login', 'POST', { email, password });
    if (res.ok) {
      const data = await res.json();
      setCookie('token', data.access_token, 1);
      window.location.href = 'index.html';
    } else {
      const err = await res.json();
      alert('Login failed: ' + (err.error || res.statusText));
    }
  } catch (e) {
    alert('Login error: ' + e.message);
  }
}

// Index page logic
async function loadIndexPage() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) loginLink.style.display = token ? 'none' : 'block';
  // Price filter options
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    [10, 50, 100, 'All'].forEach(val => {
      const opt = document.createElement('option');
      opt.value = val;
      opt.textContent = val;
      priceFilter.appendChild(opt);
    });
  }
  // Fetch amenities for mapping
  let amenitiesMap = {};
  try {
    const amenitiesRes = await apiRequest('/amenities/');
    if (amenitiesRes.ok) {
      const amenities = await amenitiesRes.json();
      amenities.forEach(a => { amenitiesMap[a.id] = a.name; });
    }
  } catch {}
  // Fetch places
  let places = [];
  try {
    const res = await apiRequest('/places/');
    if (res.ok) {
      places = await res.json();
    }
  } catch {}
  displayPlaces(places, amenitiesMap);
  if (priceFilter) {
    priceFilter.addEventListener('change', function () {
      displayPlaces(places, amenitiesMap, this.value);
    });
  }
}

function displayPlaces(places, amenitiesMap, maxPrice = 'All') {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';
  places.forEach(place => {
    if (maxPrice !== 'All' && place.price > Number(maxPrice)) return;
    const card = document.createElement('div');
    card.className = 'place-card';
    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: $${place.price} / night</p>
      <p>${place.description || ''}</p>
      <p>Amenities: ${(place.amenities || []).map(id => amenitiesMap[id] || id).join(', ')}</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;
    list.appendChild(card);
  });
}

// Place details logic
async function loadPlaceDetailsPage() {
  const placeId = getPlaceIdFromURL();
  if (!placeId) return;
  // Fetch amenities for mapping
  let amenitiesMap = {};
  try {
    const amenitiesRes = await apiRequest('/amenities/');
    if (amenitiesRes.ok) {
      const amenities = await amenitiesRes.json();
      amenities.forEach(a => { amenitiesMap[a.id] = a.name; });
    }
  } catch {}
  // Fetch place details
  let place = null;
  try {
    const res = await apiRequest(`/places/${placeId}`);
    if (res.ok) {
      place = await res.json();
    }
  } catch {}
  if (!place) return;
  displayPlaceDetails(place, amenitiesMap);
  // Reviews: fetch user info for each review
  if (place.reviews && Array.isArray(place.reviews)) {
    displayReviews(place.reviews);
  }
  // Show/hide add review form
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');
  if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';
  }
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function displayPlaceDetails(place, amenitiesMap) {
  const details = document.getElementById('place-details');
  if (!details) return;
  details.innerHTML = `
    <div class="place-details">
      <h2>${place.title}</h2>
      <p class="place-info">Price: $${place.price} / night</p>
      <p class="place-info">${place.description || ''}</p>
      <p class="place-info">Amenities: ${(place.amenities || []).map(id => amenitiesMap[id] || id).join(', ')}</p>
    </div>
  `;
}

async function displayReviews(reviews) {
  const reviewsSection = document.getElementById('reviews');
  if (!reviewsSection) return;
  reviewsSection.innerHTML = '';
  for (const review of reviews) {
    // Fetch user info
    let userName = 'User';
    try {
      const res = await apiRequest(`/users/${review.user_id}`);
      if (res.ok) {
        const user = await res.json();
        userName = user.first_name + ' ' + user.last_name;
      }
    } catch {}
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `
      <p><strong>${userName}</strong> (${review.rating}/5)</p>
      <p>${review.text}</p>
    `;
    reviewsSection.appendChild(card);
  }
}

// Add review page logic
async function loadAddReviewPage() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }
  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    window.location.href = 'index.html';
    return;
  }
  // Populate rating dropdown
  const ratingSelect = document.getElementById('rating');
  if (ratingSelect) {
    for (let i = 1; i <= 5; i++) {
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = i;
      ratingSelect.appendChild(opt);
    }
  }
  // Handle form submission
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review').value;
      const rating = Number(document.getElementById('rating').value);
      // Get user ID from token (decode JWT or fetch /users/me if available)
      let userId = null;
      try {
        // Try to get user info from /users/me (not implemented in backend, so fallback to decode JWT)
        const payload = JSON.parse(atob(token.split('.')[1]));
        userId = payload.sub || payload.identity || payload.user_id || payload.id;
      } catch {}
      if (!userId) {
        alert('Could not determine user ID.');
        return;
      }
      try {
        const res = await apiRequest('/reviews/', 'POST', {
          text: reviewText,
          rating,
          user_id: userId,
          place_id: placeId
        }, token);
        if (res.ok) {
          alert('Review submitted successfully!');
          reviewForm.reset();
        } else {
          const err = await res.json();
          alert('Failed to submit review: ' + (err.message || err.error || res.statusText));
        }
      } catch (e) {
        alert('Error submitting review: ' + e.message);
      }
    });
  }
}

// Main entry point

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
    return;
  }
  if (document.getElementById('places-list')) {
    loadIndexPage();
    return;
  }
  if (document.getElementById('place-details')) {
    loadPlaceDetailsPage();
    // Add review form on place details page
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        // Reuse add review logic
        const token = getCookie('token');
        if (!token) {
          alert('You must be logged in to submit a review.');
          return;
        }
        const placeId = getPlaceIdFromURL();
        const reviewText = document.getElementById('review-text').value;
        const rating = 5; // Default rating if not present
        let userId = null;
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          userId = payload.sub || payload.identity || payload.user_id || payload.id;
        } catch {}
        if (!userId) {
          alert('Could not determine user ID.');
          return;
        }
        try {
          const res = await apiRequest('/reviews/', 'POST', {
            text: reviewText,
            rating,
            user_id: userId,
            place_id: placeId
          }, token);
          if (res.ok) {
            alert('Review submitted successfully!');
            reviewForm.reset();
          } else {
            const err = await res.json();
            alert('Failed to submit review: ' + (err.message || err.error || res.statusText));
          }
        } catch (e) {
          alert('Error submitting review: ' + e.message);
        }
      });
    }
    return;
  }
  if (document.getElementById('review-form') && document.getElementById('rating')) {
    loadAddReviewPage();
    return;
  }
});
