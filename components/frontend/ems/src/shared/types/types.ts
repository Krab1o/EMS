import type { ReactNode } from 'react';

export interface IOption {
  value: string;
  label: ReactNode;
}

export interface IPagination {
  page: number;
  pageSize: number;
}

export interface IWithPagination<T> {
  count: number;
  next: null | string;
  previous: string;
  results: Array<T>;
}
