const API_URL = 'http://localhost:5000/api';

async function request(endpoint, options = {}) {
  const url = `${API_URL}${endpoint}`;
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'An unknown error occurred' }));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

export const login = (email, password) => {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
};

export const register = (username, email, password) => {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
  });
};

export const getTickets = () => {
  return request('/tickets');
};

export const getTicket = (ticketId) => {
  return request(`/tickets/${ticketId}`);
};

export const createTicket = (title, description) => {
  return request('/tickets', {
    method: 'POST',
    body: JSON.stringify({ title, description }),
  });
};

export const updateTicket = (ticketId, status) => {
  return request(`/tickets/${ticketId}`, {
    method: 'PUT',
    body: JSON.stringify({ status }),
  });
};

export const getComments = (ticketId) => {
  return request(`/tickets/${ticketId}/comments`);
};

export const addComment = (ticketId, text) => {
  return request(`/tickets/${ticketId}/comments`, {
    method: 'POST',
    body: JSON.stringify({ text }),
  });
};
