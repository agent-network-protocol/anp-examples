import React from 'react';
import { Button, Flex } from 'antd';
import { Attachments, Prompts, Sender } from '@ant-design/x';
import { CloudUploadOutlined, PaperClipOutlined } from '@ant-design/icons';
import { useStyles } from '../styles/useStyles';
import type { GetProp } from 'antd';

interface ChatSenderProps {
  inputValue: string;
  setInputValue: React.Dispatch<React.SetStateAction<string>>;
  onSubmit: (val: string) => void;
  attachmentsOpen: boolean;
  setAttachmentsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  attachedFiles: GetProp<typeof Attachments, 'items'>;
  setAttachedFiles: React.Dispatch<React.SetStateAction<GetProp<typeof Attachments, 'items'>>>;
  loading: boolean;
  onCancel: () => void; // 新增 onCancel 属性
}

const ChatSender: React.FC<ChatSenderProps> = ({
  inputValue,
  setInputValue,
  onSubmit,
  attachmentsOpen,
  setAttachmentsOpen,
  attachedFiles,
  setAttachedFiles,
  loading,
  onCancel, // 新增 onCancel 参数
}) => {
  const { styles } = useStyles();

  // 发送器头部（附件上传）
  const senderHeader = (
    <Sender.Header
      title="Upload File"
      open={attachmentsOpen}
      onOpenChange={setAttachmentsOpen}
      styles={{ content: { padding: 0 } }}
    >
      <Attachments
        beforeUpload={() => false}
        items={attachedFiles}
        onChange={(info) => setAttachedFiles(info.fileList)}
        placeholder={(type) =>
          type === 'drop'
            ? { title: 'Drop file here' }
            : {
              icon: <CloudUploadOutlined />,
              title: 'Upload files',
              description: 'Click or drag files to this area to upload',
            }
        }
      />
    </Sender.Header>
  );

  return (
    <>
      {/* 🌟 输入框 */}
      <Sender
        value={inputValue}
        header={senderHeader}
        onSubmit={() => {
          if (!loading) {
            onSubmit(inputValue);
            setInputValue('');
          }
        }}
        onChange={setInputValue}
        onCancel={onCancel} // 使用传入的 onCancel 函数
        prefix={
          <Button
            type="text"
            icon={<PaperClipOutlined style={{ fontSize: 18 }} />}
            onClick={() => setAttachmentsOpen(!attachmentsOpen)}
          />
        }
        className={styles.sender}
        allowSpeech
        actions={(_, info) => {
          const { SendButton, LoadingButton } = info.components;
          return (
            <Flex gap={4}>
              {loading ? (
                <div onClick={onCancel}>
                  <LoadingButton type="default"/>
                </div>

              ) : (
                <SendButton type="primary" />
              )}
            </Flex>
          );
        }}
        placeholder="Ask or input / use skills"
      />
    </>
  );
};

export default ChatSender;
