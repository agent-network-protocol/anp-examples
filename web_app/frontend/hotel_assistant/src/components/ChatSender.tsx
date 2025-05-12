import React from 'react';
import { Button, Flex } from 'antd';
import { Attachments, Prompts, Sender } from '@ant-design/x';
import { CloudUploadOutlined, PaperClipOutlined } from '@ant-design/icons';
import { useStyles } from '../styles/useStyles';
import { SENDER_PROMPTS } from '../constants/chatData';
import type { GetProp } from 'antd';

interface ChatSenderProps {
  inputValue: string;
  setInputValue: React.Dispatch<React.SetStateAction<string>>;
  onSubmit: (val: string) => void;
  loading: boolean;
  attachmentsOpen: boolean;
  setAttachmentsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  attachedFiles: GetProp<typeof Attachments, 'items'>;
  setAttachedFiles: React.Dispatch<React.SetStateAction<GetProp<typeof Attachments, 'items'>>>;
}

const ChatSender: React.FC<ChatSenderProps> = ({
  inputValue,
  setInputValue,
  onSubmit,
  loading,
  attachmentsOpen,
  setAttachmentsOpen,
  attachedFiles,
  setAttachedFiles,
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
      {/* 🌟 提示词 */}
      {/* <Prompts
        items={SENDER_PROMPTS}
        onItemClick={(info) => {
          onSubmit(info.data.description as string);
        }}
        styles={{ item: { padding: '6px 12px' } }}
        className={styles.senderPrompt}
      /> */}
      {/* 🌟 输入框 */}
      <Sender
        value={inputValue}
        // header={senderHeader}
        onSubmit={() => {
          onSubmit(inputValue);
          setInputValue('');
        }}
        onChange={setInputValue}
        onCancel={() => {
          // 如果需要取消请求，可以在这里实现
        }}
        // prefix={
        //   <Button
        //     type="text"
        //     icon={<PaperClipOutlined style={{ fontSize: 18 }} />}
        //     onClick={() => setAttachmentsOpen(!attachmentsOpen)}
        //   />
        // }
        loading={loading}
        className={styles.sender}
        // allowSpeech
        // actions={(_, info) => {
        //   const { SendButton, LoadingButton, SpeechButton } = info.components;
        //   return (
        //     <Flex gap={4}>
        //       <SpeechButton className={styles.speechButton} />
        //       {loading ? <LoadingButton type="default" /> : <SendButton type="primary" />}
        //     </Flex>
        //   );
        // }}
        placeholder="Ask or input / use skills"
      />
    </>
  );
};

export default ChatSender;
