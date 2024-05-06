import { getClient } from 'services/api/axios';
import { ICreateUser, IUpdateUser, IUser } from './usersApi.type';

export const UsersApi = {
  async getUsers(page: number) {
    const response = await getClient().get<Array<IUser>>('/users?' + page);
    return response.data;
  },

  async createUser(data: ICreateUser) {
    const response = await getClient().post('/users', data);
    return response.data;
  },

  async editUser(data: IUpdateUser) {
    const response = await getClient().put('/users', data);
    return response.data;
  },

  async deleteUser(id: number) {
    const response = await getClient().delete('/users/' + id);
    return response.data;
  },
};
