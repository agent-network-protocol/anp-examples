import React from 'react';
import { Modal, Form, Input, DatePicker } from 'antd';
import dayjs from 'dayjs';
import { RoomInfo } from '../hooks/useChat';

interface HotelOrderFormProps {
  visible: boolean;
  room: RoomInfo;
  onCancel: () => void;
  onSubmit: (values: any) => void;
  loading: boolean;
}

const HotelOrderForm: React.FC<HotelOrderFormProps> = ({ visible, room, onCancel, onSubmit, loading }) => {
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

  return (
    <Modal
      title="填写订单信息"
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
          checkInDate: today,
          checkOutDate: tomorrow,
        }}
      >
        <Form.Item label="酒店名称" name="hotelName">
          <Input disabled />
        </Form.Item>
        <Form.Item label="房型" name="roomType">
          <Input disabled />
        </Form.Item>
        <Form.Item label="床型" name="bedType">
          <Input disabled />
        </Form.Item>
        <Form.Item label="价格/晚" name="price">
          <Input disabled prefix="¥" />
        </Form.Item>
        <Form.Item label="入住人" name="guestName" rules={[{ required: true, message: '请输入入住人姓名' }]}> 
          <Input placeholder="请输入入住人姓名" />
        </Form.Item>
        <Form.Item label="手机号" name="contactMobile" rules={[{ required: true, message: '请输入手机号' }]}> 
          <Input placeholder="请输入手机号" />
        </Form.Item>
        <Form.Item label="入住日期" name="checkInDate" rules={[{ required: true, message: '请选择入住日期' }]}> 
          <DatePicker style={{ width: '100%' }} disabledDate={d => d && d < today.startOf('day')} />
        </Form.Item>
        <Form.Item label="离店日期" name="checkOutDate" rules={[{ required: true, message: '请选择离店日期' }]}> 
          <DatePicker style={{ width: '100%' }} disabledDate={d => d && d <= form.getFieldValue('checkInDate')} />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default HotelOrderForm; 