import { useAppDispatch } from 'store';
import { postSection } from 'store/sections';

import { Button, Drawer, Form, Input } from 'antd';
import TextArea from 'antd/es/input/TextArea';

import type {
  CreateSectionModalContainerProps,
  ICreateSectionField,
} from './CreateSectionModalContainer.type';

import styles from './CreateSectionModalContainer.module.scss';

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
        className={styles.form}
        initialValues={{ remember: true }}
        onFinish={submitSection}
        autoComplete="off"
      >
        <div>
          <Form.Item<ICreateSectionField>
            label="Название"
            name="title"
            className={styles.form_item}
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            label="Описание"
            name="description"
            className={styles.form_item}
            rules={[{ required: true }]}
          >
            <TextArea />
          </Form.Item>
        </div>

        <div>
          <Form.Item<ICreateSectionField>
            label="Telegram"
            name="telegram"
            className={styles.form_item}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            label="VK"
            name="vk"
            className={styles.form_item}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            label="Youtube"
            name="youtube"
            className={styles.form_item}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            label="Rutube"
            name="rutube"
            className={styles.form_item}
          >
            <Input />
          </Form.Item>

          <Form.Item<ICreateSectionField>
            label="TikTok"
            name="tiktok"
            className={styles.form_item}
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
