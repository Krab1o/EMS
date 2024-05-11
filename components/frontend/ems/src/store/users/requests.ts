import { createAsyncThunk } from '@reduxjs/toolkit';
import { getUsersAdapter } from './adapters';
import { UsersApi } from 'services/api/users/usersApi';
import { ICreateUser, IUpdateUser } from 'services/api/users/usersApi.type';

const getUsers = createAsyncThunk('users/getUsers', async (page: number) => {
  const response = await UsersApi.getUsers(page);
  return getUsersAdapter(response);
});

const createUser = createAsyncThunk(
  'users/createUser',
  async (data: { page: number; data: ICreateUser }, { dispatch }) => {
    await UsersApi.createUser(data.data);
    dispatch(getUsers(data.page));
  },
);

const updateUser = createAsyncThunk(
  'users/updateUser',
  async (data: { data: IUpdateUser; page: number }, { dispatch }) => {
    await UsersApi.editUser(data.data);
    dispatch(getUsers(data.page));
  },
);

const deleteUser = createAsyncThunk(
  'users/deleteUser',
  async (data: { id: number; page: number }, { dispatch }) => {
    await UsersApi.deleteUser(data.id);
    dispatch(getUsers(data.page));
  },
);

export { getUsers, createUser, updateUser, deleteUser };
