import { Button, DatePicker, Drawer, Form, Input } from 'antd';
import { useAppDispatch } from 'store';
import { postEvent } from 'store/events';
import type {
  CreateEventModalContainerProps,
  ICreateEventField,
} from './CreateEventModalContainer.type';
import TextArea from 'antd/es/input/TextArea';

export function CreateEventModalContainer({
  open,
  onClose,
}: CreateEventModalContainerProps) {
  const dispatch = useAppDispatch();
  const submitEvent = (data: ICreateEventField) => {
    dispatch(
      postEvent({
        cover_id: null,
        datetime: data.datetime.toISOString(),
        title: data.title,
        place: data.place,
        type_id: data.typeId,
        description: data.description,
      }),
    );
  };
  return (
    <Drawer
      title="Создание мероприятия"
      placement={'bottom'}
      width={'100vh'}
      onClose={onClose}
      open={open}
    >
      <Form
        name="basic"
        labelCol={{ span: 10 }}
        wrapperCol={{ span: 33 }}
        style={{
          display: 'flex',
          justifyContent: 'space-around',
        }}
        initialValues={{ remember: true }}
        onFinish={submitEvent}
        autoComplete="off"
      >
        <div>
          <Form.Item<ICreateEventField>
            label="Название"
            name="title"
            style={{ width: 600 }}
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateEventField>
            label="Фото"
            name="coverId"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateEventField>
            label="Описание"
            name="description"
            rules={[{ required: true }]}
          >
            <TextArea />
          </Form.Item>
        </div>

        <div>
          <Form.Item<ICreateEventField>
            label="Место проведения"
            name="place"
            style={{ width: 600 }}
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateEventField>
            label="Дата и время"
            name="datetime"
            style={{ width: 600 }}
            rules={[{ required: true }]}
          >
            <DatePicker placeholder={''} style={{ width: 350 }} />
          </Form.Item>

          <Form.Item<ICreateEventField>
            label="Тип"
            name="typeId"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
              Создать
            </Button>
          </Form.Item>
        </div>
      </Form>
    </Drawer>
  );
}
