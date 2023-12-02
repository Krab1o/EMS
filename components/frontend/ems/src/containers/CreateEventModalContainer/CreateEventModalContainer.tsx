import { Drawer } from 'antd';
import { CreateEventModalContainerProps } from './CreateEventModalContainer.type';

export function CreateEventModalContainer({
  open,
  onClose,
}: CreateEventModalContainerProps) {
  return (
    <Drawer
      title="Создание мероприятия"
      placement={'bottom'}
      width={'100vh'}
      onClose={onClose}
      open={open}
    >
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
    </Drawer>
  );
}
