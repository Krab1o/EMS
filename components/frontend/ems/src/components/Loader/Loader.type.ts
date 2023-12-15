export interface LoaderProps {
  loadingState: number;
  zIndex?: number;
  withHeader?: boolean;
}
export enum LoaderState {
  DONE,
  ERROR,
  LOADING,
  NO_DATA,
}
