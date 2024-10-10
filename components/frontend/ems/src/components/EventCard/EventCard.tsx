import { Button, Card, Typography } from 'antd';
import {
  DeleteOutlined,
  DislikeOutlined,
  LikeOutlined,
} from '@ant-design/icons';
import Meta from 'antd/es/card/Meta';
import { validateLenght } from 'shared/utils/validateLength';
import type { EventCardProps } from './EventCard.type';
import type { ReactNode } from 'react';
import { ActionsEnum } from 'containers/EventCardContainer/EventCardContainer.type';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';
import styles from './EventCard.module.scss';

function convertDate(date: Date) {
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    day: 'numeric',
    month: 'short',
    hour: 'numeric',
    minute: 'numeric',
  });
}

export function EventCard({
  initialData,
  image,
  onCardClick,
  onActionsClick,
  onDelete,
}: EventCardProps) {
  let actionsButtons: Array<ReactNode> = [];
  switch (initialData.status) {
    case EventStatusEnum.OnReview: {
      actionsButtons = [
        <Button
          shape={'round'}
          icon={<DeleteOutlined />}
          style={{ border: 'none' }}
          onClick={(e) => {
            e.stopPropagation();
            onDelete();
          }}
        />,
      ];
      break;
    }
    case EventStatusEnum.OnPoll: {
      actionsButtons = [
        <Button
          shape={'round'}
          type={
            !initialData.userVote && initialData.userVote !== null
              ? 'primary'
              : 'text'
          }
          icon={<DislikeOutlined />}
          style={{ border: 'none' }}
          onClick={(e) => {
            e.stopPropagation();
            onActionsClick(ActionsEnum.DISLIKE);
          }}
        >
          {String(initialData.votedNo)}
        </Button>,
        <Button
          shape={'round'}
          icon={<LikeOutlined />}
          style={{ border: 'none' }}
          type={initialData.userVote ? 'primary' : 'text'}
          onClick={(e) => {
            e.stopPropagation();
            onActionsClick(ActionsEnum.LIKE);
          }}
        >
          {String(initialData.votedYes)}
        </Button>,
      ];
      break;
    }
  }
  return (
    <Card
      hoverable={true}
      style={{ width: '20vw', minWidth: '350px' }}
      cover={
        image ? (
          <img className={styles.image} src={image} alt={'cover'} />
        ) : (
          <div className={styles.skeleton_image} />
        )
      }
      onClick={onCardClick}
      actions={actionsButtons}
    >
      <Typography.Text
        style={{ color: '#006eff', marginBottom: '10px', display: 'block' }}
      >
        {initialData.place.title +
          ' • ' +
          `${convertDate(initialData.date)} - ${convertDate(
            initialData.dateEnd,
          )}`}
      </Typography.Text>
      <Meta
        title={initialData.title}
        description={validateLenght(initialData.description, 200)}
      />
    </Card>
  );
}
