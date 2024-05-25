import { useEffect, useState } from 'react';
import { useAppDispatch } from 'store';
import { useSelector } from 'react-redux';
import { Button, Flex } from 'antd';
import SectionCardContainer from 'containers/SectionCardContainer';
import CreateSectionModalContainer from 'containers/CreateSectionModalContainer';
import { PlusOutlined } from '@ant-design/icons';
import { getAllSections, selectSections } from 'store/sections';
import styles from './PageSections.module.scss';

export function PageSections() {
  const dispatch = useAppDispatch();
  const sections = useSelector(selectSections);

  const [isCreateSectionModalOpen, setIsCreateModalOpen] =
    useState<boolean>(false);

  useEffect(() => {
    dispatch(getAllSections());
  }, [dispatch]);

  const openModal = () => {
    setIsCreateModalOpen(true);
  };

  return (
    <div style={{ padding: '0 0 5% 0' }}>
      <div className={styles.header}>
        <div></div>
        <Button icon={<PlusOutlined />} onClick={openModal} />
      </div>
      <CreateSectionModalContainer
        open={isCreateSectionModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />
      <Flex
        wrap={'wrap'}
        gap={'middle'}
        justify={'start'}
        className={styles.content}
        style={{ marginTop: '3%', height: '100%', padding: '0 3%' }}
      >
        {sections &&
          sections.map((el) => <SectionCardContainer initialData={el} />)}
      </Flex>
    </div>
  );
}
