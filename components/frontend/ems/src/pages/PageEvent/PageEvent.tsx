import { selectCurrentEvent } from 'store/events';
import { useSelector } from 'react-redux';
import { Image } from 'antd';
import styles from './PageEvent.module.scss';

export default function PageEvent() {
  const currentEvent = useSelector(selectCurrentEvent);

  if (currentEvent) {
    return (
      <div>
        <div className={styles.event_photo_block}>
          <Image
            preview={false}
            className={styles.image}
            src={currentEvent.cover}
          />
          <h1 className={styles.text}>{currentEvent.title}</h1>
        </div>
        <div className={styles.event_text_block}>
          {currentEvent.description}
        </div>
      </div>
    );
  } else {
    return null;
  }
}
