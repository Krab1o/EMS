import { IInstitution } from 'services/api/events/eventsApi.type';

export type UserType = {
  id: number;
  lastName: string;
  firstName: string;
  middleName: string;
  institution: IInstitution;
  course: number;
  group: number;
  role: 'user' | 'admin';
  version: number;
};
