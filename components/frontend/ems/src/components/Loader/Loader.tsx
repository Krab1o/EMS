import cn from 'classnames';
import { LoaderProps, LoaderState } from './Loader.type';

import styles from './Loader.module.scss';

function Loader({
  loadingState,
  zIndex,
  withHeader,
}: LoaderProps): JSX.Element {
  return (
    <div
      className={cn(styles.overlay, {
        [styles.overlay_header]: withHeader,
      })}
      style={{ zIndex: zIndex }}
    >
      {loadingState === LoaderState.LOADING && (
        <div className={styles.spinner} />
      )}
      {loadingState === LoaderState.ERROR ||
        (loadingState === LoaderState.NO_DATA && (
          <div className={styles.error}>Нет актуальных данных</div>
        ))}
    </div>
  );
}

export default Loader;
