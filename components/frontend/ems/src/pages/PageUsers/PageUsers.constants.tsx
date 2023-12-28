import type { IUser } from 'pages/PageUsers/PageUsers.type';
import type { ColumnType } from 'antd/es/table/interface';
import type { IField } from 'shared/types/types';

export const columns: Array<ColumnType<IUser> & IField> = [
  {
    title: 'Имя пользователя',
    dataIndex: 'username',
    key: 'username',
    formField: {
      fieldType: 'input',
      rules: [
        {
          required: true,
          message: 'Обязательное поле',
        },
        {
          max: 256,
          message: 'Максимальное количество символов - 256',
        },
      ],
    },
  },
  {
    title: 'Фамилия',
    dataIndex: 'lastname',
    key: 'lastname',
    formField: {
      fieldType: 'input',
      rules: [
        {
          required: true,
          message: 'Обязательное поле',
        },
        {
          max: 256,
          message: 'Максимальное количество символов - 256',
        },
      ],
    },
  },
  {
    title: 'Имя',
    dataIndex: 'firstname',
    key: 'address',
    formField: {
      fieldType: 'input',
      rules: [
        {
          required: true,
          message: 'Обязательное поле',
        },
        {
          max: 256,
          message: 'Максимальное количество символов - 256',
        },
      ],
    },
  },
  {
    title: 'Отчество',
    key: 'surname',
    dataIndex: 'surname',
    formField: {
      fieldType: 'input',
    },
  },
  {
    title: 'Роль',
    key: 'role',
    dataIndex: 'role',
    formField: {
      fieldType: 'select',
      selectFields: [
        {
          label: 'Администратор',
          value: 'admin',
        },
        {
          label: 'Студент',
          value: 'student',
        },
      ],
      rules: [
        {
          required: true,
          message: 'Обязательное поле',
        },
        {
          max: 256,
          message: 'Максимальное количество символов - 256',
        },
      ],
    },
  },
];
