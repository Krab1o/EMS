import { createAsyncThunk } from '@reduxjs/toolkit';
import { authApi } from 'services/api/auth/authApi';
import type { FetchLoginDataProps } from './types';

const postLoginData = createAsyncThunk(
  'auth/postLoginData',
  async ({ login, password }: FetchLoginDataProps) => {
    const response = await authApi.login(login, password);
    localStorage.setItem('token', response.token);
  },
);

export { postLoginData };
