import { StrictMode, useEffect } from 'react';
import { Provider, useSelector } from 'react-redux';
import store, { useAppDispatch } from 'store';
import { authActions, selectIsAuth, selectIsInit } from 'store/auth';
import { BrowserRouter } from 'react-router-dom';

import Router from 'routes';
import Loader from 'components/Loader';
import AppHeaderContainer from 'containers/AppHeaderContainer';
import PageLogin from './pages/PageLogin';

import { LoaderState } from 'components/Loader/Loader.type';
import styles from './App.module.scss';

function App() {
  const isAuth = useSelector(selectIsAuth);
  const isInit = useSelector(selectIsInit);
  const dispatch = useAppDispatch();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      dispatch(authActions.setIsAuth(true));
    }
    dispatch(authActions.setIsInit(true));
  }, [dispatch]);

  if (!isInit) return <Loader loadingState={LoaderState.LOADING} />;

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
      <Provider store={store}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provider>
    </StrictMode>
  );
}
export default AppContainer;
