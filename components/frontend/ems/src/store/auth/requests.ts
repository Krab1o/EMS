import { createAsyncThunk } from '@reduxjs/toolkit';
import { authApi } from 'services/api/auth/authApi';
import type { FetchLoginDataProps } from './types';

const authMe = createAsyncThunk('auth/authMe', async () => {
  const response = await authApi.authMe();
  return response.role;
});

const postLoginData = createAsyncThunk(
  'auth/postLoginData',
  async ({ login, password }: FetchLoginDataProps, { dispatch }) => {
    const response = await authApi.login(login, password);
    localStorage.setItem('token', response.token);
    dispatch(authMe());
  },
);

export { postLoginData, authMe };
