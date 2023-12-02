import { Card, Typography } from 'antd';
import { DislikeOutlined, LikeOutlined } from '@ant-design/icons';
import Meta from 'antd/es/card/Meta';
import { validateLenght } from 'shared/utils/validateLength';
import { EventCardProps } from './EventCard.type';

function convertDate(date: Date) {
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    day: 'numeric',
    month: 'short',
  });
}
export function EventCard({ initialData, onCardClick }: EventCardProps) {
  return (
    <Card
      style={{ width: '30vw', minWidth: '400px' }}
      cover={<img src={initialData.cover} alt={'cover'} />}
      onClick={onCardClick}
      actions={[
        <DislikeOutlined
          key={'dislike'}
          onClick={(e) => e.stopPropagation()}
        />,
        <LikeOutlined key={'like'} onClick={(e) => e.stopPropagation()} />,
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
