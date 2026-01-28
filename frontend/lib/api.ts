import AsyncStorage from '@react-native-async-storage/async-storage';

export const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:5000/api';

const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

export async function setTokens(accessToken: string, refreshToken: string) {
  await AsyncStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  await AsyncStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
}

export async function clearTokens() {
  await AsyncStorage.removeItem(ACCESS_TOKEN_KEY);
  await AsyncStorage.removeItem(REFRESH_TOKEN_KEY);
}

export async function getAccessToken() {
  return AsyncStorage.getItem(ACCESS_TOKEN_KEY);
}

export async function getRefreshToken() {
  return AsyncStorage.getItem(REFRESH_TOKEN_KEY);
}

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface ApiOptions {
  method?: HttpMethod;
  body?: any;
  auth?: boolean;
  retry?: boolean;
}

async function rawRequest(path: string, options: ApiOptions = {}) {
  const url = `${API_URL}${path}`;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (options.auth) {
    const token = await getAccessToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  const response = await fetch(url, {
    method: options.method ?? 'GET',
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  return response;
}

export async function apiRequest(path: string, options: ApiOptions = {}) {
  const response = await rawRequest(path, options);

  // If unauthorized and we have a refresh token, try refresh flow once.
  if (response.status === 401 && options.auth && options.retry !== false) {
    const refreshToken = await getRefreshToken();
    if (!refreshToken) {
      throw new Error('Unauthorized');
    }

    const refreshRes = await rawRequest('/auth/refresh', {
      method: 'POST',
      body: { refresh_token: refreshToken },
      auth: false,
    });

    if (!refreshRes.ok) {
      await clearTokens();
      throw new Error('Session expired');
    }

    const refreshData = await refreshRes.json();
    const newAccess = refreshData.access_token as string;
    await AsyncStorage.setItem(ACCESS_TOKEN_KEY, newAccess);

    // Retry original request once with new token
    const retryRes = await rawRequest(path, { ...options, retry: false });
    return retryRes;
  }

  return response;
}

