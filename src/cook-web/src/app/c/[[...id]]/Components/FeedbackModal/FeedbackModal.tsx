import styles from './FeedbackModal.module.scss';

import { useCallback, memo } from 'react';
import { useTranslation } from 'react-i18next';

// TODO: 完成 antd 组件的转换
// import { Modal, Form, Input, message } from 'antd';
import MainButton from '@/c-components/MainButton';
import { calModalWidth } from '@/c-utils/common';
import { submitFeedback } from '@/c-api/bz';

const FEEDBACK_MAX_LENGTH = 300;

export const FeedbackModal = ({ open, onClose, inMobile = false }) => {
  // const { t } = useTranslation();
  // const { TextArea } = Input;
  // const [form] = Form.useForm();
  // const [messageApi, contextHolder] = message.useMessage();

  // const onSubmitFeedback = useCallback(async () => {
  //   try {
  //     const data = await form.validateFields();
  //     const { feedback } = data;
  //     await submitFeedback(feedback);
  //     messageApi.success({
  //       content: t('feedback.feedbackSuccess'),
  //     });
  //     onClose();
  //   } catch {}
  // }, [form, messageApi, onClose, t]);

  return (
    <></>
    // <Modal
    //   className={styles.feedbackModal}
    //   width={calModalWidth({ inMobile })}
    //   open={open}
    //   footer={null}
    //   maskClosable={true}
    //   onCancel={onClose}
    // >
    //   <div className={styles.title}>{t('feedback.feedbackTitle')}</div>
    //   <Form form={form} className={styles.formWrapper}>
    //     <Form.Item
    //       name="feedback"
    //       rules={[{ required: true, message:t('feedback.feedbackPlaceholder') }]}
    //     >
    //       <TextArea
    //         // value={feedback}
    //         showCount
    //         maxLength={FEEDBACK_MAX_LENGTH}
    //         minLength={5}
    //         style={{ height: '90px', resize: 'none' }}
    //       />
    //     </Form.Item>
    //   </Form>
    //   <MainButton
    //     className={styles.okBtn}
    //     width="100%"
    //     onClick={onSubmitFeedback}
    //   >
    //     {t('feedback.feedbackSubmit')}
    //   </MainButton>
    //   { contextHolder }
    // </Modal>
  );
};

export default memo(FeedbackModal);
