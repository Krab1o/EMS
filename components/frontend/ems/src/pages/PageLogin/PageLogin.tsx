// import { useAppDispatch } from 'store';
// import { useSelector } from 'react-redux';
// import { selectFetchStatus } from 'store/auth';
// import { postLoginData } from 'store/auth/requests';
import Login from 'components/Login';
import PageLayoutAuth from 'pages/PageLayoutAuth';

import type { ILoginData } from 'components/Login/Login.type';

export default function PageLogin() {
  // const dispatch = useAppDispatch();
  // const fetchStatus = useSelector(selectFetchStatus);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const postLogin = (data: ILoginData) => {
    return;
  };
  return (
    <PageLayoutAuth>
      <h2>Авторизация</h2>
      <Login
        postLogin={postLogin}
        fetchStatus={{ error: '', isLoading: false }}
      />
    </PageLayoutAuth>
  );
}
