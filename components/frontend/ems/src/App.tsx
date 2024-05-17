import { StrictMode, useEffect } from 'react';
import { Provider, useSelector } from 'react-redux';
import store, { useAppDispatch } from 'store';
import Ru_RU from 'antd/es/locale/ru_RU';
import {
  authActions,
  authMe,
  selectIsAuth,
  selectIsInit,
  selectRole,
} from 'store/auth';
import { BrowserRouter } from 'react-router-dom';

import Router from 'routes';
import Loader from 'components/Loader';
import AppHeaderContainer from 'containers/AppHeaderContainer';
import PageLogin from './pages/PageLogin';
import AlertWrapperContainer from 'containers/AlertWrapperContainer';
import { ConfigProvider } from 'antd';

import { LoaderState } from 'components/Loader/Loader.type';
import styles from './App.module.scss';

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
Ru_RU.DatePicker.lang.locale = 'ru';

function App() {
  const isAuth = useSelector(selectIsAuth);
  const isInit = useSelector(selectIsInit);
  const dispatch = useAppDispatch();
  const role = useSelector(selectRole);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      dispatch(authActions.setIsAuth(true));
      dispatch(authMe());
    }
    dispatch(authActions.setIsInit(true));
  }, [dispatch]);

  if (!isInit || role === null)
    return <Loader loadingState={LoaderState.LOADING} />;

  if (isAuth)
    return (
      <div className={styles.app}>
        <AppHeaderContainer />
        <main>
          <Router />
        </main>
      </div>
    );

  return <PageLogin />;
}

function AppContainer() {
  return (
    <StrictMode>
      <ConfigProvider locale={Ru_RU}>
        <Provider store={store}>
          <BrowserRouter>
            <AlertWrapperContainer>
              <App />
            </AlertWrapperContainer>
          </BrowserRouter>
        </Provider>
      </ConfigProvider>
    </StrictMode>
  );
}
export default AppContainer;
