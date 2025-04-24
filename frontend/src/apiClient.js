// src/apiClient.js
import { getToken } from './authService';

export const authFetch = async (url, options = {}, onUnauthorized) => {
  let token = getToken();

  const headers = {
    ...(options.headers || {}),
    Authorization: token ? `Bearer ${token}` : '',
    'Content-Type': 'application/json',
  };

  try {
    const res = await fetch(url, {
      ...options,
      headers,
      credentials: 'include',  // In case refresh token cookie is needed
    });

    // If unauthorized
    //if (res.status === 401) {
    //clearToken();  // token may be expired
    //throw new Error('Unauthorized - please log in again');
    //}
    if (res.status === 401 && onUnauthorized) {
      onUnauthorized(); // ✅ trigger logout if token is expired
    }

    // Handle rate limiting
    if (res.status === 429) {
      const msg = await res.text();
      throw new Error(`Rate limit hit: ${msg}`);
    }

    return res;
  } catch (err) {
    console.error('authFetch error:', err);
    throw err;
  }
};

