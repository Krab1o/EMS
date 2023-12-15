import { Button, Form, Input, Checkbox } from 'antd';
import type { LoginProps } from './Login.type';
import styles from './Login.module.scss';

export default function Login({ postLogin, fetchStatus }: LoginProps) {
  return (
    <div className={styles.login}>
      {fetchStatus.error && (
        <p data-testid={'loginError'} className={styles.error}>
          {fetchStatus.error}
        </p>
      )}
      <Form
        name="basic"
        onFinish={postLogin}
        autoComplete="off"
        data-testid={'loginForm'}
        className={styles.form}
      >
        <div className={styles.form__item}>
          <label>Логин</label>
          <Form.Item
            name="login"
            rules={[{ required: true, message: 'Введите имя!' }]}
          >
            <Input data-testid={'loginInput'} />
          </Form.Item>
        </div>

        <div className={styles.form__item}>
          <label>Пароль</label>
          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Введите пароль!' }]}
          >
            <Input type={'password'} data-testid={'passInput'} />
          </Form.Item>
        </div>

        <div className={styles.form__checkbox}>
          <Checkbox>Запомнить меня</Checkbox>
        </div>

        <Form.Item>
          <Button
            loading={fetchStatus.isLoading}
            type={'text'}
            htmlType="submit"
            data-testid={'loginBtn'}
          >
            {!fetchStatus.isLoading && 'Войти'}
          </Button>
        </Form.Item>
      </Form>

      <Form.Item>
        <div>
          Ещё не с нами? <a>Зарегистрироваться</a>
        </div>
      </Form.Item>
    </div>
  );
}
