import { selectCurrentEvent } from 'store/events';
// import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
// import { EventsApi } from 'services/api/events/eventsApi';
// import { Image } from 'antd';
import styles from './PageEvent.module.scss';

export default function PageEvent() {
  const currentEvent = useSelector(selectCurrentEvent);

  if (currentEvent) {
    return (
      <div>
        <div className={styles.event_text_block}>
          {currentEvent.description}
        </div>
      </div>
    );
  } else {
    return null;
  }
}
