import { useEffect, useState } from 'react';
import { useAppDispatch } from 'store';
import { useSelector } from 'react-redux';
import { Button, Flex } from 'antd';
import SectionCardContainer from 'containers/SectionCardContainer';
import CreateSectionModalContainer from 'containers/CreateSectionModalContainer';
import { PlusOutlined } from '@ant-design/icons';
import { getAllSections, selectSections } from 'store/sections';

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
    <div style={{ height: '100%' }}>
      <Button icon={<PlusOutlined />} onClick={openModal} />
      <CreateSectionModalContainer
        open={isCreateSectionModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />
      <Flex
        wrap={'wrap'}
        gap={'middle'}
        justify={'center'}
        style={{ marginTop: '3%', height: '100%' }}
      >
        {sections &&
          sections.map((el) => <SectionCardContainer initialData={el} />)}
      </Flex>
    </div>
  );
}
