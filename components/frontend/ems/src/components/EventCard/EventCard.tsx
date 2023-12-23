import { Button, Card, Typography } from 'antd';
import {
  DeleteOutlined,
  DislikeOutlined,
  LikeOutlined,
} from '@ant-design/icons';
import Meta from 'antd/es/card/Meta';
import { validateLenght } from 'shared/utils/validateLength';
import { EventCardProps } from './EventCard.type';
import { ActionsEnum } from 'containers/EventCardContainer/EventCardContainer.type';
import styles from './EventCard.module.scss';

function convertDate(date: Date) {
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    day: 'numeric',
    month: 'short',
  });
}

export function EventCard({
  initialData,
  image,
  onCardClick,
  onActionsClick,
  onDelete,
}: EventCardProps) {
  return (
    <Card
      hoverable={true}
      style={{ width: '20vw' }}
      cover={<img className={styles.image} src={image} alt={'cover'} />}
      onClick={onCardClick}
      actions={[
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
          icon={<DeleteOutlined />}
          style={{ border: 'none' }}
          onClick={(e) => {
            e.stopPropagation();
            onDelete();
          }}
        />,
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
      ]}
    >
      <Typography.Text
        style={{ color: '#006eff', marginBottom: '10px', display: 'block' }}
      >
        {initialData.place + ' • ' + convertDate(initialData.date)}
      </Typography.Text>
      <Meta
        title={initialData.title}
        description={validateLenght(initialData.description, 200)}
      />
    </Card>
  );
}
