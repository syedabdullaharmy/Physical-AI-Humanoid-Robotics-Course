import React from 'react';
import Layout from '@theme-original/Layout';
import ChatWidget from '@site/src/components/ChatWidget';
import AuthModal from '@site/src/components/Auth';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props} />
      <AuthModal />
      <ChatWidget />
    </>
  );
}
