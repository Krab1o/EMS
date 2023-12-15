import axios from 'axios';

const baseUrl = process.env.REACT_APP_BASE_URL;

export const getClient = () => {
  const client = axios.create({
    baseURL: `${baseUrl}`,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  client.interceptors.request.use(function (config) {
    const token = localStorage.getItem('token');
    config.headers.Authorization = token
      ? `Bearer ${token}`
      : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MDIxMzg3Mjl9.cMTJy6ELq8Qf-ADR-yQspvWQQAriTk-y3FTUDxKZFFs';
    return config;
  });
  return client;
};
