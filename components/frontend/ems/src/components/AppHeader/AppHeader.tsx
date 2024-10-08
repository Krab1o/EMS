import { useState } from 'react';
import { MenuOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons';
import { Drawer, Button, Popover } from 'antd';
// import cn from 'classnames';
import { ReactComponent as ESMUMLogo } from 'assets/icons/ESMUM_title.svg';
import ToggleButton from 'components/ToggleButton';
import ToggleButtonGroup from 'components/ToggleButtonGroup';
import {
  LOGOUT_APPROVE,
  LOGOUT_TEXT,
  MENU_CONSTANTS,
} from './AppHeader.constants';
import type { AppHeaderProps } from './AppHeader.type';
import styles from './AppHeader.module.scss';

export function renderLogout(logout: () => void) {
  return (
    <div data-testid={'popoverLogout'}>
      <Button onClick={logout} data-testid={'logoutButton'}>
        {LOGOUT_APPROVE}
      </Button>
    </div>
  );
}

export default function AppHeader({
  activeMenuItem,
  historyPush,
  logout,
  role,
}: AppHeaderProps) {
  const [isDrawerVisible, setIsDrawerVisible] = useState(false);

  const showDrawer = () => {
    setIsDrawerVisible(true);
  };

  const closeDrawer = () => {
    setIsDrawerVisible(false);
  };

  return (
    <header className={styles.app_header}>
      {/* Бургер-меню для мобильных устройств */}
      <div className={styles.burger_container}>
        <Button
          className={styles.burger_button}
          type="text"
          icon={<MenuOutlined />} // иконка бургера
          onClick={showDrawer}
        />
      </div>

      {/* Логотип, отображаемый слева на десктопе и по центру на мобильных */}
      <div className={styles.app_header__logo}>
        <ESMUMLogo />
      </div>

      {/* Drawer для отображения мобильного меню */}
      <Drawer
        title="Menu"
        placement="left" // Изменяем размещение на 'left'
        onClose={closeDrawer}
        open={isDrawerVisible}
        className={styles.mobile_menu}
      >
        <ToggleButtonGroup
          onChange={historyPush}
          value={activeMenuItem}
          isWithoutDivider
        >
          {MENU_CONSTANTS.map((el) => {
            if ((el.admin && role === 'admin') || !el.admin)
              return (
                <ToggleButton key={el.value} value={el.value}>
                  {el.label}
                </ToggleButton>
              );
            return null;
          })}
        </ToggleButtonGroup>

        {/* Дополнительные элементы, такие как кнопка выхода */}
        <div className={styles.drawer_logout}>
          <Button onClick={logout} icon={<LogoutOutlined />}>
            Logout
          </Button>
        </div>
      </Drawer>

      {/* Оригинальная навигация (только для десктопа) */}
      <div className={styles.app_header__bar}>
        <div className={styles.app_header__navigation}>
          <ToggleButtonGroup
            onChange={historyPush}
            value={activeMenuItem}
            isWithoutDivider
          >
            {MENU_CONSTANTS.map((el) => {
              if ((el.admin && role === 'admin') || !el.admin)
                return (
                  <ToggleButton key={el.value} value={el.value}>
                    {el.label}
                  </ToggleButton>
                );
              return null;
            })}
          </ToggleButtonGroup>
        </div>
      </div>

      {/* Оригинальная информация (только для десктопа) */}
      <div className={styles.app_header__info}>
        <Button type="text" data-testid="profileButton">
          <UserOutlined />
        </Button>
        <Popover
          content={() => renderLogout(logout)}
          title={LOGOUT_TEXT}
          trigger="click"
        >
          <Button type="text" data-testid="logoutPopoverButton">
            <LogoutOutlined />
          </Button>
        </Popover>
      </div>
    </header>
  );
}
