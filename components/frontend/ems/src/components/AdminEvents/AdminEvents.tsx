import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useAppDispatch } from 'store';
import {
  deleteEvent,
  eventsActions,
  selectCurrentEvent,
  selectCurrentEventsStatus,
  updateEvent,
} from 'store/events';
import { EventsApi } from 'services/api/events/eventsApi';

import {
  Button,
  Descriptions,
  Flex,
  Image,
  Space,
  Spin,
  Table,
  TableProps,
} from 'antd';

import type { AdminEventsProps } from 'components/AdminEvents/AdminEvents.type';
import type { EventType } from 'store/events/types';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';

import styles from './AdminEvents.module.scss';

export function AdminEvents({ events }: AdminEventsProps) {
  const dispatch = useAppDispatch();
  const currentEvent = useSelector(selectCurrentEvent);
  const currentEventStatus = useSelector(selectCurrentEventsStatus);
  const [image, setImage] = useState('');

  useEffect(() => {
    if (currentEvent && currentEvent.cover)
      EventsApi.getEventImage(currentEvent.cover.uri).then((res) =>
        setImage(URL.createObjectURL(res)),
      );
  }, [currentEvent]);

  const onCardClick = (data: EventType) => {
    dispatch(eventsActions.setCurrentEvent(data));
    setImage('');
  };

  const onDelete = () => {
    if (currentEvent)
      dispatch(
        deleteEvent({ id: currentEvent.id, status: currentEventStatus }),
      );
  };

  const onChangesStatus = (status: EventStatusEnum) => {
    if (currentEvent)
      dispatch(
        updateEvent({
          id: currentEvent.id,
          status: status,
          cover: currentEvent.cover,
          datetime: currentEvent.date.toISOString(),
          description: currentEvent.description,
          place: {
            title: currentEvent.place.title,
            floor: currentEvent.place.floor,
            id: Number(currentEvent.place.id),
            institution: currentEvent.place.institution,
            institution_id: Number(currentEvent.place.id),
          },
          title: currentEvent.title,
          user_vote: currentEvent.userVote,
          version: currentEvent.version + 1,
          voted_no: currentEvent.votedNo,
          voted_yes: currentEvent.votedYes,
          place_id: currentEvent.place.id,
          dateend: currentEvent.dateEnd.toISOString(),
        }),
      );
  };

  const columns: TableProps<EventType>['columns'] = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Название',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: 'Действия',
      key: 'action',
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      render: (_, record) => (
        <Space size="middle">
          <Button type={'link'} onClick={() => onCardClick(record)}>
            Просмотреть
          </Button>
        </Space>
      ),
    },
  ];

  if (events)
    return (
      <Flex
        wrap={'wrap'}
        gap={'middle'}
        justify={'space-around'}
        style={{ marginTop: '20px' }}
      >
        <Table className={styles.table} columns={columns} dataSource={events} />
        {currentEvent && (
          <div className={styles.description_block}>
            <div className={styles.event_photo_block}>
              {image ? (
                <Image preview={false} className={styles.image} src={image} />
              ) : (
                <Spin />
              )}
            </div>
            <h4 className={styles.text}>{currentEvent.title}</h4>
            <div className={styles.event_text_block}>
              {currentEvent.description}
            </div>
            <Descriptions
              style={{ padding: '10px' }}
              title={'Дополнительная информация'}
              layout="vertical"
              bordered
              items={[
                {
                  key: '2',
                  label: 'Дата проведения',
                  children: currentEvent.date.toLocaleDateString(),
                },
                {
                  key: '3',
                  label: 'Голосов за',
                  children: currentEvent.votedYes,
                },
                {
                  key: '3',
                  label: 'Голосов против',
                  children: currentEvent.votedNo,
                },
                {
                  key: '1',
                  label: 'Место проведения',
                  children: currentEvent.place.title,
                },
              ]}
            />
            <div className={styles.actions}>
              <Button onClick={onDelete} type={'primary'} danger>
                Удалить
              </Button>

              {currentEventStatus === EventStatusEnum.OnPoll && (
                <Button
                  onClick={() => onChangesStatus(EventStatusEnum.Planned)}
                  type={'primary'}
                >
                  Запланировать
                </Button>
              )}

              {currentEventStatus === EventStatusEnum.OnReview && (
                <Button
                  onClick={() => onChangesStatus(EventStatusEnum.OnPoll)}
                  type={'primary'}
                >
                  Одобрить
                </Button>
              )}

              {currentEventStatus === EventStatusEnum.Planned && (
                <Button
                  danger
                  type={'primary'}
                  onClick={() => onChangesStatus(EventStatusEnum.Ended)}
                >
                  Завершить
                </Button>
              )}
            </div>
          </div>
        )}
      </Flex>
    );
  return null;
}
