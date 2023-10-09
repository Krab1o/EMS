import { StrictMode } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import store from 'store';
import routes from 'routes';

function App() {
  return (
    <div>
      <header>Хедер</header>
      <main>
        <Routes>
          <Route path="*" element={<Navigate to={routes.EVENTS} replace />} />
          <Route path="/" element={<Navigate to={routes.EVENTS} replace />} />
          <Route
            path="/login"
            element={<Navigate to={routes.EVENTS} replace />}
          />
          <Route path={routes.EVENTS} element={<>Мероприятия</>} />
          <Route path={routes.SECTIONS} element={<>Секции</>} />
        </Routes>
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
