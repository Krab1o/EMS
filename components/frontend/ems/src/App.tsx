import { StrictMode } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import Router from 'routes';
import AppHeaderContainer from 'containers/AppHeaderContainer';
import store from 'store';
import styles from './App.module.scss';

function App() {
  return (
    <div className={styles.app}>
      <AppHeaderContainer />
      <main>
        <Router />
      </main>
      <footer>
        © {new Date().getFullYear()} ООО «Говна кусок». Все права защищены.
      </footer>
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
