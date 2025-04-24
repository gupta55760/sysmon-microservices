import { jwtDecode } from 'jwt-decode';

const ACCESS_KEY = 'access_token';

export function setToken(token) {
  localStorage.setItem(ACCESS_KEY, token);
}

export function getToken() {
  return localStorage.getItem(ACCESS_KEY);
}

export function clearToken() {
  localStorage.removeItem(ACCESS_KEY);
}

export function getRoleFromToken(token) {
  try {
    const decoded = jwtDecode(token);
    return decoded.role || '';
  } catch {
    return '';
  }
}

