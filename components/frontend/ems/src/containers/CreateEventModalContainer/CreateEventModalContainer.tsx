import { useAppDispatch } from 'store';
import { EventsApi } from 'services/api/events/eventsApi';
import { postEvent } from 'store/events';

import { Button, DatePicker, Drawer, Form, Input, Upload } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import TextArea from 'antd/es/input/TextArea';
import AsyncSelect from 'components/AsyncSelect';

import type {
  CreateEventModalContainerProps,
  ICreateEventField,
} from './CreateEventModalContainer.type';

export function CreateEventModalContainer({
  open,
  onClose,
}: CreateEventModalContainerProps) {
  const dispatch = useAppDispatch();
  const submitEvent = (data: ICreateEventField) => {
    dispatch(
      postEvent({
        cover: data.cover,
        datetime: data.datetime.toISOString(),
        title: data.title,
        place: data.place,
        type_id: Number(data.typeId.value),
        description: data.description,
      }),
    );
  };
  const getFile = (e: { fileList: Array<{ originFileObj: File }> }) => {
    return e && e.fileList.length !== 0 && e.fileList[0].originFileObj;
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
            name="cover"
            rules={[{ required: true }]}
            getValueFromEvent={getFile}
          >
            <Upload>
              <Button icon={<UploadOutlined />}>Кликните для загрузки</Button>
            </Upload>
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
            <AsyncSelect allowClear fetchOptions={EventsApi.getEventTypes} />
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
