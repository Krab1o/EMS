import axios from 'axios';

const baseUrl = 'http://dev.evgenym.com:3000';

export const getClient = () => {
  const client = axios.create({
    baseURL: `${baseUrl}`,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  client.interceptors.request.use(function (config) {
    const token = localStorage.getItem('token');
    config.headers.Authorization = token ? `Bearer ${token}` : '';
    return config;
  });
  return client;
};
