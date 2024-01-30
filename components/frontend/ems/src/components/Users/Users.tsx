import { Table } from 'antd';
import { TABLE_COLUMNS, data } from './Users.constants';

export default function Users() {
  // useEffect(() => {
  //   dispatch(getAllEvents());
  // }, [dispatch]);

  return <Table columns={TABLE_COLUMNS} dataSource={data} />;
}
