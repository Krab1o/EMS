import { useAppDispatch } from 'store';
import { postSection } from 'store/sections';

import { Button, Drawer, Form, Input } from 'antd';
import TextArea from 'antd/es/input/TextArea';

import type {
  CreateSectionModalContainerProps,
  ICreateSectionField,
} from './CreateSectionModalContainer.type';

export function CreateSectionModalContainer({
  open,
  onClose,
}: CreateSectionModalContainerProps) {
  const dispatch = useAppDispatch();
  const submitSection = (data: ICreateSectionField) => {
    dispatch(
      postSection({
        telegram: data.telegram,
        title: data.title,
        description: data.description,
        rutube: data.rutube,
        tiktok: data.tiktok,
        is_favorite: false,
        youtube: data.youtube,
        vk: data.vk,
      }),
    );
    onClose();
  };

  return (
    <Drawer
      title="Создание секции"
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
        onFinish={submitSection}
        autoComplete="off"
      >
        <div>
          <Form.Item<ICreateSectionField>
            label="Название"
            name="title"
            style={{ width: 600 }}
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            label="Описание"
            name="description"
            rules={[{ required: true }]}
          >
            <TextArea />
          </Form.Item>
        </div>

        <div>
          <Form.Item<ICreateSectionField>
            label="Telegram"
            name="telegram"
            style={{ width: 600 }}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            label="VK"
            name="vk"
            style={{ width: 600 }}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            style={{ width: 600 }}
            label="Youtube"
            name="youtube"
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            style={{ width: 600 }}
            label="Rutube"
            name="rutube"
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            style={{ width: 600 }}
            label="TikTok"
            name="tiktok"
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
