import { UserType } from './types';
import { IUser } from 'services/api/users/usersApi.type';

function getUsersAdapter(data: Array<IUser>): Array<UserType> {
  return data.map((el) => {
    return {
      id: el.id,
      lastName: el.last_name,
      firstName: el.first_name,
      middleName: el.middle_name,
      institution: el.institution,
      course: el.course,
      group: el.group,
      role: el.role,
      version: el.version,
    };
  });
}

export { getUsersAdapter };
