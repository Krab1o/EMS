import { getClient } from 'services/api/axios';
import type { ILoginData } from './authApi.type';

export const authApi = {
  async login(login: string, password: string) {
    const response = await getClient().post<ILoginData>('auth/login/', {
      email: login,
      password: password,
    });
    return response.data;
  },
};
