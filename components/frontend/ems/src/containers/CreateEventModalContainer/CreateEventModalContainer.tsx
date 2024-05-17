import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useAppDispatch } from 'store';
import { EventsApi } from 'services/api/events/eventsApi';
import { checkIfPlaceFree, postEvent, selectIsPlaceFree } from 'store/events';

import { Button, DatePicker, Drawer, Form, Input, Upload } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import TextArea from 'antd/es/input/TextArea';
import AsyncSelect from 'components/AsyncSelect';

import dateFnsGenerateConfig from 'rc-picker/lib/generate/dateFns';
import debounce from 'shared/utils/debounce/debounce';
import type {
  CreateEventModalContainerProps,
  ICreateEventField,
} from './CreateEventModalContainer.type';
import type { FormChangeInfo } from 'rc-field-form/lib/FormContext';
import type { IOption } from 'shared/types/types';

const MyDatePicker = DatePicker.generatePicker<Date>(dateFnsGenerateConfig);

export function CreateEventModalContainer({
  open,
  onClose,
}: CreateEventModalContainerProps) {
  const dispatch = useAppDispatch();
  const isPlaceFree = useSelector(selectIsPlaceFree);
  const [placeFields, setPlaceFields] = useState({
    dateend: null as null | Date,
    datetime: null as null | Date,
    placeId: undefined as undefined | IOption,
  });

  const submitEvent = (data: ICreateEventField) => {
    if (isPlaceFree)
      dispatch(
        postEvent({
          cover: data.cover,
          datetime: data.datetime.toISOString(),
          title: data.title,
          place_id: Number(data.placeId.value),
          type_id: Number(data.typeId.value),
          description: data.description,
          dateend: data.dateend.toISOString(),
        }),
      );
    onClose();
  };

  const getFile = (e: { fileList: Array<{ originFileObj: File }> }) => {
    return e && e.fileList.length !== 0 && e.fileList[0].originFileObj;
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const onChangeForm = (_: string, info: FormChangeInfo) => {
    const field = info.changedFields.length ? info.changedFields[0] : null;
    if (field) {
      const fieldName = field.name[0];
      switch (fieldName) {
        case 'datetime':
        case 'dateend':
        case 'placeId': {
          setPlaceFields((prev) => ({
            ...prev,
            [fieldName]: field.value,
          }));
          break;
        }
        default:
          break;
      }
    }
  };

  const onChangeFormDebounced = debounce(onChangeForm, 100);

  useEffect(() => {
    const { dateend, datetime, placeId } = placeFields;
    if (datetime && dateend && placeId) {
      dispatch(
        checkIfPlaceFree({
          dateend: dateend.toISOString(),
          datetime: datetime.toISOString(),
          place_id: Number(placeId.value),
        }),
      );
    }
  }, [dispatch, placeFields]);

  return (
    <Drawer
      title="Создание мероприятия"
      placement={'bottom'}
      width={'100vh'}
      onClose={onClose}
      open={open}
    >
      <Form.Provider onFormChange={onChangeFormDebounced}>
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
              name="placeId"
              style={{ width: 600 }}
              rules={[{ required: true }]}
            >
              <AsyncSelect allowClear fetchOptions={EventsApi.getEventPlaces} />
            </Form.Item>
            {!isPlaceFree && (
              <div
                style={{
                  marginLeft: '250px',
                  marginTop: '-20px',
                  color: 'red',
                }}
              >
                Место не свободно
              </div>
            )}

            <Form.Item<ICreateEventField>
              label="Дата и время"
              name="datetime"
              style={{ width: 600 }}
              rules={[{ required: true }]}
            >
              <MyDatePicker
                showTime
                showSecond={false}
                placeholder={''}
                format={'dd.MM.yyyy HH:mm'}
                style={{ width: 350 }}
              />
            </Form.Item>
            {!isPlaceFree && (
              <div
                style={{
                  marginLeft: '250px',
                  marginTop: '-20px',
                  color: 'red',
                }}
              >
                Место не свободно
              </div>
            )}

            <Form.Item<ICreateEventField>
              label="Дата и время окончания"
              name="dateend"
              style={{ width: 600 }}
              rules={[{ required: true }]}
            >
              <MyDatePicker
                showSecond={false}
                format={'dd.MM.yyyy HH:mm'}
                showTime
                placeholder={''}
                style={{ width: 350 }}
              />
            </Form.Item>
            {!isPlaceFree && (
              <div
                style={{
                  marginLeft: '250px',
                  marginTop: '-20px',
                  color: 'red',
                }}
              >
                Место не свободно
              </div>
            )}

            <Form.Item<ICreateEventField> label="Тип" name="typeId">
              <AsyncSelect allowClear fetchOptions={EventsApi.getEventTypes} />
            </Form.Item>

            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
              <Button type="primary" htmlType="submit">
                Создать
              </Button>
            </Form.Item>
          </div>
        </Form>
      </Form.Provider>
    </Drawer>
  );
}
