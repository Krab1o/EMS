import { IInstitution } from 'services/api/events/eventsApi.type';

export interface IUser {
  id: number;
  last_name: string;
  first_name: string;
  middle_name: string;
  institution: IInstitution;
  course: number;
  group: number;
  role: 'user' | 'admin';
  version: number;
}

export interface ICreateUser {
  last_name: string;
  first_name: string;
  middle_name: string;
  institution_id: number;
  course: number;
  group: number;
  telegram: string;
  vk: string;
  phone_number: string;
  email: string;
  password: string;
}

export interface IUpdateUser {
  id: number;
  last_name: string;
  first_name: string;
  middle_name: string;
  institution_id: number;
  course: number;
  group: number;
  telegram: string;
  vk: string;
  phone_number: string;
  email: string;
  password: string;
}
