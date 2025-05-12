import React, { useEffect, useRef } from 'react';
import { Modal, message } from 'antd';
import { getHotelOrderDetail } from '../services/hotelService';

interface PayQrModalProps {
  visible: boolean;
  orderNo: string;
  qrCodeUrl: string;
  onClose: () => void;
}

const PayQrModal: React.FC<PayQrModalProps> = ({ visible, orderNo, qrCodeUrl, onClose }) => {
  const pollingCount = useRef(0);
  const timer = useRef<NodeJS.Timeout | null>(null);
  const modalDestroyed = useRef(false);

  useEffect(() => {
    modalDestroyed.current = false;
    if (visible) {
      pollOrderDetail();
    }
    return () => {
      modalDestroyed.current = true;
      if (timer.current) clearTimeout(timer.current);
    };
    // eslint-disable-next-line
  }, [visible, orderNo]);

  const pollOrderDetail = async () => {
    if (modalDestroyed.current) return;
    pollingCount.current++;
    const detail = await getHotelOrderDetail({ customerOrderNo: orderNo });
    const statusEl = document.getElementById(`polling-status-${orderNo}`);
    const detailEl = document.getElementById(`order-detail-${orderNo}`);
    if (detail.success && detail.data && detail.data.orderStatus === '已支付') {
      if (statusEl) statusEl.textContent = '支付成功，订单信息如下：';
      if (detailEl) {
        detailEl.innerHTML = `
          <div style="margin-top: 10px; text-align: left; font-size: 14px;">
            <div>酒店：${detail.data.hotelName}</div>
            <div>房型：${detail.data.roomType}</div>
            <div>入住：${detail.data.checkInDate}</div>
            <div>离店：${detail.data.checkOutDate}</div>
            <div>房客：${detail.data.guestNames?.join('、')}</div>
            <div>金额：¥${detail.data.orderAmount}</div>
            <div>状态：${detail.data.orderStatus}</div>
          </div>
        `;
      }
      return;
    }
    if (pollingCount.current < 6) {
      if (statusEl) statusEl.textContent = `正在查询支付状态...（第${pollingCount.current}次）`;
      timer.current = setTimeout(pollOrderDetail, 10000);
    } else {
      if (statusEl) statusEl.textContent = '未查到订单支付信息，请稍后在订单中心查看。';
    }
  };

  return (
    <Modal
      title="请扫码支付"
      open={visible}
      onOk={onClose}
      onCancel={onClose}
      okText="关闭"
      cancelButtonProps={{ style: { display: 'none' } }}
      width={300}
      destroyOnClose
    >
      <div style={{ textAlign: 'center' }}>
        <img src={qrCodeUrl} alt="支付二维码" style={{ width: 200, height: 200 }} />
        <p>订单号：{orderNo}</p>
        <div id={`order-detail-${orderNo}`}></div>
        <p id={`polling-status-${orderNo}`}>正在查询支付状态...</p>
      </div>
    </Modal>
  );
};

export default PayQrModal; 