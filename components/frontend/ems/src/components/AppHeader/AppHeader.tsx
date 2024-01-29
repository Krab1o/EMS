import cn from 'classnames';
import { ReactComponent as ESMUMLogo } from 'assets/icons/orangeAVM.svg';
import ToggleButton from 'components/ToggleButton';
import ToggleButtonGroup from 'components/ToggleButtonGroup';
import { Button, Popover } from 'antd';
import { UserOutlined, LogoutOutlined } from '@ant-design/icons';
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
}: AppHeaderProps) {
  return (
    <header className={styles.app_header}>
      <div className={styles.app_header__bar}>
        <ESMUMLogo />
        <div className={styles.app_header__navigation}>
          <ToggleButtonGroup
            onChange={historyPush}
            value={activeMenuItem}
            isWithoutDivider
          >
            {MENU_CONSTANTS.map((el) => (
              <ToggleButton key={el.value} value={el.value}>
                {el.label}
              </ToggleButton>
            ))}
          </ToggleButtonGroup>
        </div>
      </div>

      <div className={styles.app_header__info}>
        <div className={styles.user}>
          <Button type={'text'} data-testid={'profileButton'}>
            <UserOutlined />
          </Button>
        </div>
        <div className={cn(styles.user, styles.user__logout)}>
          <Popover
            content={() => renderLogout(logout)}
            title={LOGOUT_TEXT}
            trigger="click"
          >
            <Button data-testid={'logoutPopoverButton'} type={'text'}>
              <LogoutOutlined />
            </Button>
          </Popover>
        </div>
      </div>
    </header>
  );
}
