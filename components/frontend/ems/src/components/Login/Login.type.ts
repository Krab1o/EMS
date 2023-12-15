export interface ILoginData {
  login: string;
  password: string;
}
export interface LoginProps {
  postLogin: (data: ILoginData) => void;
  fetchStatus: {
    isLoading: boolean;
    error: string;
  };
}
