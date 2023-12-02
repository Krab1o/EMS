import { Navigate, Route, Routes } from 'react-router-dom';
import { EVENTS, LOGIN } from 'routes/routes';
import { routes } from 'routes/index';
import PageEvent from 'pages/PageEvent';

export default function Router() {
  return (
    <Routes>
      <Route path="*" element={<Navigate to={EVENTS} replace />} />
      <Route path="/" element={<Navigate to={EVENTS} replace />} />
      <Route path={LOGIN} element={<Navigate to={EVENTS} replace />} />
      <Route path={routes.EVENTS} element={<>Мероприятия</>} />
      <Route path={routes.EVENTS + '/:eventId'} element={<PageEvent />} />
      <Route path={routes.SECTIONS} element={<>Секции</>} />
      <Route path={routes.USERS} element={<>Пользователи</>} />
    </Routes>
  );
}
