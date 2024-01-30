import { Typography } from 'antd';
const { Title } = Typography;
export default function Sections() {
  // useEffect(() => {
  //   dispatch(getAllEvents());
  // }, [dispatch]);

  return (
    <div style={{ textAlign: 'center' }}>
      <Typography>
        <Title>
          Данный функционал ещё не разработан
          <br />
          Следи за обновлениями!
        </Title>
      </Typography>
    </div>
  );
}
