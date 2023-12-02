<<<<<<< HEAD
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
=======
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        hello
      </header>
>>>>>>> 396cac0 (init frontend app)
    </div>
  );
}

<<<<<<< HEAD
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
=======
export default App;
>>>>>>> 396cac0 (init frontend app)
