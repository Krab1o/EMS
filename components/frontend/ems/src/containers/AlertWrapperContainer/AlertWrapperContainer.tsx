import { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useAppDispatch } from 'store';
import { appActions, selectAlert } from 'store/app';
import cn from 'classnames';
import { Alert } from 'antd';
import type { AlertWrapperContainerProps } from 'containers/AlertWrapperContainer/AlertWrapperContainer.type';
import styles from './AlertWrapperContainer.module.scss';

export function AlertWrapperContainer({
  children,
}: AlertWrapperContainerProps) {
  const { message, isError } = useSelector(selectAlert);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (message) {
      setTimeout(
        () =>
          dispatch(
            appActions.setAlert({
              message: '',
              isError: false,
            }),
          ),
        3000,
      );
    }
  }, [dispatch, message]);

  return (
    <>
      <Alert
        type="error"
        message={message}
        banner
        className={cn(styles.alert, {
          [styles.alert_unvisible]: !message && !isError,
        })}
      />
      <Alert
        type="success"
        message={message}
        banner
        className={cn(styles.alert, {
          [styles.alert_unvisible]: !message || (message && isError),
        })}
      />
      {children}
    </>
  );
}
