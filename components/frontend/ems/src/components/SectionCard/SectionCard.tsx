import { Button, Card, Typography } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import Meta from 'antd/es/card/Meta';
import { validateLenght } from 'shared/utils/validateLength';
import type { SectionCardProps } from './SectionCard.type';
import type { ReactNode } from 'react';

export function SectionCard({
  initialData,
  onCardClick,
  onDelete,
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
      style={{ width: '20vw' }}
      onClick={onCardClick}
      actions={actionsButtons}
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
