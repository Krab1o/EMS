import { useSelector } from 'react-redux';
import { selectCurrentSection } from 'store/sections';
import { Image } from 'antd';
import image from 'assets/images/events.png';
import styles from './PageSection.module.scss';

export default function PageSection() {
  const currentSection = useSelector(selectCurrentSection);

  if (currentSection) {
    return (
      <div>
        <div className={styles.event_photo_block}>
          <Image preview={false} className={styles.image} src={image} />
          <h1 className={styles.text}>{currentSection.title}</h1>
        </div>
        <div className={styles.event_text_block}>
          {currentSection.description}
        </div>
      </div>
    );
  } else {
    return null;
  }
}
