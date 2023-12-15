import cn from 'classnames';
import { ReactComponent as ESMUMLogo } from 'assets/icons/uuundulate.svg';
import type { PageLayoutAuthProps } from 'pages/PageLayoutAuth/PageLayoutAuth.type';
import styles from 'pages/PageLayoutAuth/PageLayoutAuth.module.scss';

function PageLayoutAuth({ className, children }: PageLayoutAuthProps) {
  return (
    <div className={cn(styles.auth, className)}>
      <div className={styles.page__left}>
        <ESMUMLogo />
        <h1 className={styles.page__heading}>
          Единая система менеджмента
          <br />
          управлений мероприятиями
        </h1>
      </div>
      <div className={styles.page__right}>{children}</div>

      <div className={styles.page__logo}></div>
      {/*<p className={styles.page__rights}>Все права защищены</p>*/}
      <p className={styles.page__year}>{new Date().getFullYear()}</p>
    </div>
  );
}

export default PageLayoutAuth;
