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
    
    try {
      // Get order details from API
      const detail = await getHotelOrderDetail({ customerOrderNo: orderNo });
      console.log('Order detail response:', detail);
      
      const statusEl = document.getElementById(`polling-status-${orderNo}`);
      const detailEl = document.getElementById(`order-detail-${orderNo}`);
      
      // Check if payment is successful based on payStatus field
      // 0: unpaid, 1: paid
      if (detail.success && detail.data && detail.data.payStatus === 1) {
        if (statusEl) statusEl.textContent = '支付成功，订单信息如下：';
        if (detailEl) {
          // Display order details
          detailEl.innerHTML = `
            <div style="margin-top: 10px; text-align: left; font-size: 14px;">
              <div>酒店：${detail.data.hotelName}</div>
              <div>房型：${detail.data.roomTypeName}</div>
              <div>入住：${detail.data.checkInDate}</div>
              <div>离店：${detail.data.checkOutDate}</div>
              <div>房客：${detail.data.guestNames}</div>
              <div>金额：¥${detail.data.orderAmount}</div>
              <div>状态：${'已支付'}</div>
            </div>
          `;
        }
        return;
      }
      
      // Calculate max polling attempts (3 minutes with 2 second intervals)
      const maxPollingCount = (3 * 60) / 2; // 90 polling attempts
      
      // Display current status and continue polling if within time limit
      if (pollingCount.current < maxPollingCount) {
        if (statusEl) {
          const elapsedSeconds = pollingCount.current * 2;
          const minutes = Math.floor(elapsedSeconds / 60);
          const seconds = elapsedSeconds % 60;
          const timeDisplay = minutes > 0 
            ? `${minutes}分${seconds}秒` 
            : `${seconds}秒`;
            
          statusEl.textContent = `正在查询支付状态...（已等待${timeDisplay}）`;
        }
        
        // Poll every 2 seconds
        timer.current = setTimeout(pollOrderDetail, 2000);
      } else {
        if (statusEl) statusEl.textContent = '未查到订单支付信息，请稍后在订单中心查看。';
      }
    } catch (error) {
      console.error('Error polling order details:', error);
      // Continue polling despite errors
      if (!modalDestroyed.current && pollingCount.current < (3 * 60) / 2) {
        timer.current = setTimeout(pollOrderDetail, 2000);
      }
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
        {qrCodeUrl && qrCodeUrl.startsWith('http') ? (
          <img 
            src={qrCodeUrl} 
            alt="支付二维码" 
            style={{ width: 200, height: 200 }} 
            onError={(e) => {
              // 如果图片加载失败，显示替代内容
              const target = e.target as HTMLImageElement;
              target.onerror = null; // 防止无限递归错误
              target.style.display = 'none';
              const container = target.parentNode as HTMLElement;
              const fallbackDiv = document.createElement('div');
              fallbackDiv.style.width = '200px';
              fallbackDiv.style.height = '200px';
              fallbackDiv.style.margin = '0 auto';
              fallbackDiv.style.border = '1px dashed #ccc';
              fallbackDiv.style.borderRadius = '4px';
              fallbackDiv.style.display = 'flex';
              fallbackDiv.style.alignItems = 'center';
              fallbackDiv.style.justifyContent = 'center';
              fallbackDiv.innerHTML = `
                <div style="text-align: center; padding: 20px;">
                  <p style="margin-bottom: 10px;">二维码加载失败</p>
                  <p style="margin-bottom: 10px;">请使用订单号在当面支付</p>
                </div>
              `;
              container.appendChild(fallbackDiv);
            }}
          />
        ) : (
          // 如果URL无效，直接显示替代内容
          <div style={{ 
            width: 200, 
            height: 200, 
            margin: '0 auto',
            border: '1px dashed #ccc',
            borderRadius: '4px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <p style={{ marginBottom: '10px' }}>支付二维码不可用</p>
              <p style={{ marginBottom: '10px' }}>请使用订单号在银行或商家处支付</p>
            </div>
          </div>
        )}
        <p>订单号：{orderNo}</p>
        <div id={`order-detail-${orderNo}`}></div>
        <p id={`polling-status-${orderNo}`}>正在查询支付状态...</p>
      </div>
    </Modal>
  );
};

export default PayQrModal; 