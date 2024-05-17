import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAppDispatch } from 'store';
import { authActions, selectRole } from 'store/auth';

import AppHeader from 'components/AppHeader';

export default function AppHeaderContainer() {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useAppDispatch();
  const role = useSelector(selectRole);

  const [activeMenuItem, setActiveMenuItem] = useState('');

  useEffect(() => {
    setActiveMenuItem(location.pathname.split('/')[1]);
  }, [location.pathname]);

  const historyPush = (value: string) => {
    navigate(`/${value}`);
  };

  const logout = () => {
    localStorage.removeItem('token');
    dispatch(authActions.setIsAuth(false));
    navigate('/login');
  };

  return (
    <AppHeader
      activeMenuItem={activeMenuItem}
      logout={logout}
      historyPush={historyPush}
      role={role}
    />
  );
}
