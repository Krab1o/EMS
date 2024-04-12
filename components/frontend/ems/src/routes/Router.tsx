import { Navigate, Route, Routes } from 'react-router-dom';
import PageEvents from 'pages/PageEvents';
import PageEvent from 'pages/PageEvent';
import PageUsers from 'pages/PageUsers';
import PageSections from 'pages/PageSections';
import PageSection from 'pages/PageSection';
import { routes } from 'routes';
import { EVENTS, LOGIN } from 'routes/routes';

export default function Router() {
  return (
    <Routes>
      <Route path="*" element={<Navigate to={routes.EVENTS} replace />} />
      <Route path="/" element={<Navigate to={routes.EVENTS} replace />} />
      <Route path={LOGIN} element={<Navigate to={EVENTS} replace />} />
      <Route path={routes.EVENTS} element={<PageEvents />} />
      <Route path={routes.EVENTS + '/:eventId'} element={<PageEvent />} />
      <Route path={routes.SECTIONS} element={<PageSections />} />
      <Route path={routes.SECTIONS + '/:sectionId'} element={<PageSection />} />
      <Route path={routes.USERS} element={<PageUsers />} />
    </Routes>
  );
}
