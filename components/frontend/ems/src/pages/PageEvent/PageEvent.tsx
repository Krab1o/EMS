import { selectCurrentEvent } from 'store/events';
import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { EventsApi } from 'services/api/events/eventsApi';
import { Image } from 'antd';
import styles from './PageEvent.module.scss';

export default function PageEvent() {
  const currentEvent = useSelector(selectCurrentEvent);
  const [image, setImage] = useState('');

  useEffect(() => {
    if (currentEvent)
      EventsApi.getEventImage(currentEvent.cover.uri).then((res) =>
        setImage(URL.createObjectURL(res)),
      );
  }, [currentEvent]);

  if (currentEvent) {
    return (
      <div>
        <div className={styles.event_photo_block}>
          <Image preview={false} className={styles.image} src={image} />
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
