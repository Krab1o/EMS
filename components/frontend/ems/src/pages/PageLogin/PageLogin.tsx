import { useAppDispatch } from 'store';
import { useSelector } from 'react-redux';
import { selectFetchStatus } from 'store/auth';
import { postLoginData } from 'store/auth/requests';
import Login from 'components/Login';
import PageLayoutAuth from 'pages/PageLayoutAuth';

import type { ILoginData } from 'components/Login/Login.type';

export default function PageLogin() {
  const dispatch = useAppDispatch();
  const fetchStatus = useSelector(selectFetchStatus);
  const postLogin = (data: ILoginData) => {
    dispatch(postLoginData(data));
  };
  return (
    <PageLayoutAuth>
      <h2>Авторизация</h2>
      <Login postLogin={postLogin} fetchStatus={fetchStatus} />
    </PageLayoutAuth>
  );
}
