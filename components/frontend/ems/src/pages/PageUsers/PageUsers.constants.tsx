import type { ColumnType } from 'antd/es/table/interface';
import type { IField } from 'shared/types/types';
import { UserType } from 'store/users/types';

export const columns: Array<ColumnType<UserType> & IField> = [
  {
    title: 'Имя',
    dataIndex: 'firstName',
    key: 'firstName',
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
    dataIndex: 'lastName',
    key: 'lastName',
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
    dataIndex: 'middleName',
    key: 'middleName',
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
    title: 'Курс',
    dataIndex: 'course',
    key: 'course',
    formField: {
      fieldType: 'number',
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
    title: 'Институт',
    dataIndex: 'ins',
  },
];
