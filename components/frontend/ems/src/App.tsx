import React, { StrictMode } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import Router from 'routes';
import AppHeaderContainer from 'containers/AppHeaderContainer';
import store from 'store';
import styles from './App.module.scss';
import PageLogin from './pages/PageLogin';

function App() {
  return <PageLogin />;
  return (
    <div className={styles.app}>
      <AppHeaderContainer />
      <main>
        <Router />
      </main>
    </div>
  );
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
