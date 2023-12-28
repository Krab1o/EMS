import { Navigate, Route, Routes } from 'react-router-dom';
import PageEvents from 'pages/PageEvents';
import PageEvent from 'pages/PageEvent';
import PageUsers from 'pages/PageUsers';
import { EVENTS, LOGIN } from 'routes/routes';
import { routes } from 'routes';

export default function Router() {
  return (
    <Routes>
      <Route path="*" element={<Navigate to={routes.EVENTS} replace />} />
      <Route path="/" element={<Navigate to={routes.EVENTS} replace />} />
      <Route path={LOGIN} element={<Navigate to={EVENTS} replace />} />
      <Route path={routes.EVENTS} element={<PageEvents />} />
      <Route path={routes.EVENTS + '/:eventId'} element={<PageEvent />} />
      <Route path={routes.SECTIONS} element={<>Секции</>} />
      <Route path={routes.USERS} element={<PageUsers />} />
    </Routes>
  );
}
