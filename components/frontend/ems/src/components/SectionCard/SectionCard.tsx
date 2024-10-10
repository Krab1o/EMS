import { Button, Card, Typography } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import Meta from 'antd/es/card/Meta';
import { validateLenght } from 'shared/utils/validateLength';
import type { SectionCardProps } from './SectionCard.type';
import type { ReactNode } from 'react';
import styles from './SectionCard.module.scss';

export function SectionCard({
  initialData,
  onCardClick,
  onDelete,
  role,
}: SectionCardProps) {
  const actionsButtons: Array<ReactNode> = [
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
  return (
    <Card
      hoverable={true}
      style={{ width: '20vw', minWidth: '350px' }}
      cover={
        <img
          className={styles.image}
          src={
            'https://habrastorage.org/webt/lc/-6/ef/lc-6efvgqpkky1ohuk8alctjonw.png'
          }
          alt={'cover'}
        />
      }
      onClick={onCardClick}
      actions={role === 'admin' ? actionsButtons : undefined}
    >
      <Typography.Text
        style={{ color: '#006eff', marginBottom: '10px', display: 'block' }}
      >
        {initialData.telegram}
      </Typography.Text>
      <Meta
        title={initialData.title}
        description={validateLenght(initialData.description, 200)}
      />
    </Card>
  );
}
