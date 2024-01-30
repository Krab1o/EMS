import type { DataType } from './Users.type';
import type { ColumnsType } from 'antd/es/table';
export const TABLE_COLUMNS: ColumnsType<DataType> = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
  },
  {
    title: 'Email',
    dataIndex: 'email',
    key: 'email',
  },
];

//TODO: ASK DATA FROM BACKEND
export const data: DataType[] = [
  {
    key: '1',
    name: 'Fedor Fedorov',
    age: 32,
    email: 'ffed@gmail.com',
  },
  {
    key: '2',
    name: 'Grigoriy Grigoryev',
    age: 42,
    email: 'ggev@yandex.ru',
  },
  {
    key: '3',
    name: 'Rydanov Nikita',
    age: 22,
    email: 'rykita@gmail.com',
  },
  {
    key: '4',
    name: 'Andrey Gradusov',
    age: 33,
    email: 'andreygrad@gmail.com',
  },
];
