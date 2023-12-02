import { useParams } from 'react-router-dom';
import { Image } from 'antd';
import event from 'assets/images/events.png';
import styles from './PageEvent.module.scss';

export default function PageEvent() {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { eventId } = useParams();
  return (
    <div>
      <div className={styles.event_photo_block}>
        <Image preview={false} className={styles.image} src={event} />
        <h1 className={styles.text}>Квест для первокурсников</h1>
      </div>
      <div className={styles.event_text_block}>
        Подходит к концу первый месяц нового этапа вашей жизни. Многие из вас
        успели обзавестись знакомыми, а некоторые даже стали друзьями. Но
        сможете ли вы стать настоящей командой? Ничего кроме этого уже не важно,
        ибо мир стоит на грани исчезновения... И вы должны спасти его, чего бы
        вам это ни стоило. Вам необходимо собрать команду из 5-7 человек (если
        вас меньше — не беда: мы поможем вам найти ещё людей) и помочь устранить
        временные катаклизмы, проходя испытания в разные эпохи человеческой
        истории. Обязательно придумайте название! Зарегистрироваться можно
        здесь: https://vk.cc/cr7aG6Регистрация продлится до 22:00 часов четверга
        (28 сентября). Дерзайте, время не ждёт... Сможете ли вы стать тем самым
        отрядом, который восстановит баланс и вернёт всё на свои места?
      </div>
    </div>
  );
}
