import React from 'react';
import { Modal, Form, Input, DatePicker } from 'antd';
import dayjs from 'dayjs';
import { RoomInfo, ChatResponse } from '../hooks/useChat';

interface HotelOrderFormProps {
  visible: boolean;
  room: RoomInfo;
  onCancel: () => void;
  onSubmit: (values: any) => void;
  loading: boolean;
  apiData?: ChatResponse; // 添加API返回的数据
}

const HotelOrderForm: React.FC<HotelOrderFormProps> = ({ visible, room, onCancel, onSubmit, loading, apiData }) => {
  const [form] = Form.useForm();
  const today = dayjs();
  const tomorrow = dayjs().add(1, 'day');

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      onSubmit(values);
      form.resetFields();
    } catch (e) {}
  };

  const handleCancel = () => {
    onCancel();
    form.resetFields();
  };

  // 增强调试日志
  console.log('HotelOrderForm received apiData:', apiData);
  console.log('apiData fields available:', apiData ? Object.keys(apiData) : 'null');
  console.log('guestNames:', apiData?.guestNames);
  console.log('contactName:', apiData?.contactName);
  console.log('contactMobile:', apiData?.contactMobile);
  console.log('checkInDate:', apiData?.checkInDate);
  console.log('checkOutDate:', apiData?.checkOutDate);
  
  // 测试日期解析
  if (apiData?.checkInDate) {
    console.log('Parsed checkInDate:', dayjs(apiData.checkInDate).format('YYYY-MM-DD'));
  }
  if (apiData?.checkOutDate) {
    console.log('Parsed checkOutDate:', dayjs(apiData.checkOutDate).format('YYYY-MM-DD'));
  }

  return (
    <Modal
      title="确认订单信息"
      open={visible}
      onOk={handleOk}
      onCancel={handleCancel}
      okText="提交订单"
      cancelText="取消"
      confirmLoading={loading}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          hotelName: room.hotel.hotelName,
          roomType: room.roomType,
          bedType: room.bedType,
          price: room.pricePerNight,
          // 使用API返回的数据填充，如果没有则使用默认值
          guestName: apiData?.guestNames?.[0] || '',
          contactMobile: apiData?.contactMobile || '',
          // 直接使用字符串格式的日期值
          checkInDate: apiData?.checkInDate || today.format('YYYY-MM-DD'),
          checkOutDate: apiData?.checkOutDate || tomorrow.format('YYYY-MM-DD'),
          contactName: apiData?.contactName || '',
        }}
      >
        <Form.Item label="酒店名称" name="hotelName">
          <Input disabled />
        </Form.Item>
        <Form.Item label="联系人" name="contactName" rules={[{ required: true, message: '请输入联系人姓名' }]}> 
          <Input placeholder="请输入联系人姓名" />
        </Form.Item>
        <Form.Item label="入住人" name="guestName" rules={[{ required: true, message: '请输入入住人姓名' }]}> 
          <Input placeholder="请输入入住人姓名" />
        </Form.Item>
        <Form.Item label="房型" name="roomType">
          <Input disabled />
        </Form.Item>
        <Form.Item label="床型" name="bedType">
          <Input disabled />
        </Form.Item>
        <Form.Item label="手机号" name="contactMobile" rules={[{ required: true, message: '请输入手机号' }]}> 
          <Input placeholder="请输入手机号" />
        </Form.Item>
        <Form.Item label="入住日期" name="checkInDate" rules={[{ required: true, message: '请输入入住日期' }]}> 
          <Input disabled />
        </Form.Item>
        <Form.Item label="离店日期" name="checkOutDate" rules={[{ required: true, message: '请输入离店日期' }]}> 
          <Input disabled />
        </Form.Item>
        <Form.Item label="价格/晚" name="price">
          <Input disabled prefix="¥" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default HotelOrderForm; 