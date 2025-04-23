// authService.js
const API_URL = "http://localhost:8080/api/users";


// ✅ In-memory cache for access token
let accessToken = null;

export const setToken = (token) => {
  accessToken = token;
};

export const getToken = () => accessToken;

/**
 * Attempts to refresh access token using the cookie-based refresh_token.
 * Stores and returns new access token.
 */
export const refreshAccessToken = async () => {
  const res = await fetch(`${API_URL}/refresh`, {
    method: 'POST',
    credentials: 'include', // ✅ Required to send refresh_token cookie
  });

  if (!res.ok) {
    console.log("In refreshAccessToken !res.ok")
    throw new Error('Refresh failed');
  }

  const data = await res.json();
  setToken(data.access_token); // ✅ Store for reuse
  return data.access_token;
};

/**
 * Authenticated fetch using access token.
 * Refreshes once if needed.
 */
export const authFetch = async (url, options = {}) => {
  let token = getToken();
  if (!token) {
    try {
      token = await refreshAccessToken();
    } catch (err) {
      console.error('Initial refresh failed:', err);
      throw err;
    }
  }

  const headers = {
    ...(options.headers || {}),
    Authorization: `Bearer ${token}`,
  };

  let res = await fetch(url, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    try {
      const newToken = await refreshAccessToken();
      const retryHeaders = {
        ...headers,
        Authorization: `Bearer ${newToken}`,
      };

      res = await fetch(url, {
        ...options,
        headers: retryHeaders,
      });
    } catch (err) {
      console.error('Retry after refresh failed:', err);
      throw err;
    }
  }

  if (res.status === 429) {
      throw new Error('Too many requests. Please slow down.');
  }

  return res;
};

