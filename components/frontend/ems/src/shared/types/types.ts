import type { ReactNode } from 'react';

export interface IOption {
  value: string;
  label: ReactNode;
}

export interface IPagination {
  page: number;
  size: number;
}

export interface ITableParams {
  pagination?: IPagination;
}

export interface IWithPagination<T> {
  count: number;
  next: null | string;
  previous: string;
  results: Array<T>;
}
