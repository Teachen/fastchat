<template>
<view class="page-layout">
  <view class="page-body" id="x_chat">
    <view :key="index" v-for="(message, index) in messages">
      <view class="chat-item-body">
        <view class="chat-item-time">{{message.time}}</view>
        <view key="index" v-if="message.type == 'ai'" class="chat-item-layout chat-left">
          <view class="chat-inner-layout">
            <view class="chat-item-name">{{message.sender}}</view>
            <view class="chat-item-msg-layout">
              <image class="chat-item-photo" v-if="message.photoUrl" :src="message.photoUrl" mode="aspectFit"></image>
              <view class="chat-inner-msg-left" v-html="message.text"></view>
            </view>
          </view>
        </view>
      </view>
      <view :key="index" v-if="message.type == 'sender'" class="chat-item-layout chat-right">
        <view class="chat-inner-layout">
          <view class="chat-item-name-right">{{message.sender}}</view>
          <view class="chat-item-msg-layout">
            <view class="chat-inner-msg-right" v-html="message.text"></view>
            <image class="chat-item-photo" v-if="message.photoUrl" :src="message.photoUrl" mode="aspectFit"></image>
          </view>
        </view>
      </view>
    </view>
  </view>
  <view class="submit-layout">
    <input class="submit-input" :disabled="isSending" placeholder="点击输入，开始聊天吧" v-model="userInput"/>
    <view class="submit-submit" type="submit" size="mini" @click="sendMessage">{{ isSending ? '思考中...' : '发送' }}</view>
  </view>
</view>
</template>

<script setup>
import {nextTick, ref} from "vue";
import {useStore} from '../../stores';
import {settings} from '../../settings';

const store = useStore();

const userInput = ref("");
const isSending = ref(false);
const messages = ref([{
    type: 'ai',
    sender: '闲语',
    text: '你好，我是情感助手，有问题可以直接问我。',
    time: formatTime(),
    photoUrl: '',
  }
])

function formatTime() {
  const date = new Date();
  const pad = (value)=>`${value}`.padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

function formatMessageText(text) {
  return `${text || ''}`
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>');
}

const pageScrollToBottom = ()=>{
    wx.createSelectorQuery().select('#x_chat').boundingClientRect(function (rect) {
      if (!rect) {
        return;
      }
      let top = rect.height;
      wx.pageScrollTo({
        scrollTop: top,
        duration: 100
      })
    }).exec()
}
pageScrollToBottom();

const sendMessage = async ()=>{
  // if(!store.get_payload()){
  //   // 如果没有认证Token，则跳转登陆页面
  //   uni.navigateTo({
  //      url: '/pages/login/login',
  //   });  
  // }

  if (isSending.value || userInput.value.trim() === '') return;

  const content = userInput.value.trim();
  const userMessage = {
    type: 'sender',
    sender: '我',
    text: formatMessageText(content),
    time: formatTime(),
    photoUrl: '',
  };
  messages.value.push(userMessage);
  userInput.value = '';
  isSending.value = true;
  await nextTick();
  pageScrollToBottom();

  const history = messages.value
    .filter((message)=>message.type === 'sender' || message.type === 'ai')
    .slice(-10)
    .map((message)=>({
      role: message.type === 'sender' ? 'user' : 'assistant',
      content: `${message.text}`.replace(/<br>/g, '\n').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'),
    }));

  try {
    const response = await uni.request({
      method: 'POST',
      url: `${settings.host}/chat`,
      data: {
        message: content,
        history: history.slice(0, -1),
      },
      // header: {
      //   Authorization: `Bearer ${store.get_token()}`,
      // }
      header: {}
    });

    if (response.data.code !== 200) {
      throw new Error(response.data.err_msg || '对话失败');
    }

    messages.value.push({
      type: 'ai',
      sender: 'DeepSeek',
      text: formatMessageText(response.data.reply),
      time: formatTime(),
      photoUrl: '',
    });
  } catch (error) {
    messages.value.push({
      type: 'ai',
      sender: 'DeepSeek',
      text: formatMessageText(error?.message || error?.response?.data?.err_msg || '服务暂时不可用，请稍后重试'),
      time: formatTime(),
      photoUrl: '',
    });
  } finally {
    isSending.value = false;
    await nextTick();
    pageScrollToBottom();
  }
}

</script>

<style>
.page-layout {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.page-body {
  width: 100%;
  display: flex;
  flex-direction: column;
  padding-bottom: 56px;
}

.chat-item-body {
  display: flex;
  flex-direction: column;
  margin-top: 20rpx;
}

.chat-item-time {
  width: 100vw;
  text-align: center;
  font-size: 28rpx;
  color: #ccc;
  border-radius: 10rpx;
  margin-top: 40rpx;
}

.chat-item-layout {
  display: block;
  max-width: 82%;
  margin: 1rpx 5rpx;
  box-sizing: border-box;
  padding: 0 1rpx;
}

.chat-right {
  float: right;
}

.chat-left {
  float: left;
}

.chat-inner-layout {
  display: flex;
  flex-direction: column;
}

.chat-item-photo {
  width: 70rpx;
  height: 70rpx;
  min-width: 70rpx;
  min-height: 70rpx;
  border-radius: 50%;
}

.chat-item-msg-layout {
  display: flex;
  flex-direction: row;
}

.chat-item-name {
  display: flex;
  flex-direction: row;
  align-items: center;
  font-size: 28rpx;
  color: #999;
  border-radius: 10rpx;
  margin: 5rpx 0 0 80rpx;
}

.chat-item-name-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  font-size: 28rpx;
  color: #999;
  border-radius: 10rpx;
  margin: 5rpx 0 0 5rpx;
}

.chat-inner-msg-left {
  display: inline-block;
  flex-direction: row;
  align-items: center;
  color: #000;
  font-size: 30rpx;
  border-radius: 10rpx;
  background: #eee;
  padding: 15rpx 15rpx 15rpx 25rpx;
  margin-left: 12rpx;
}

.chat-inner-msg-right {
  display: inline-block;
  color: #000;
  font-size: 30rpx;
  border-radius: 10rpx;
  background: #87EE5F;
  padding: 15rpx 5rpx 15rpx 15rpx;
  margin-right: 12rpx;
}

.submit-layout {
  position: absolute;
  bottom: 0;
  width: 100%;
  background: #eee;
  flex-direction: row;
}

.submit-layout {
  width: 100%;
  position: fixed;
  bottom: 0;
  border-top: 1px solid #ddd;
  padding: 10rpx 0;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.submit-input {
  flex: 1;
  background: #fff;
  margin: 5rpx 10rpx;
  border-radius: 5rpx;
  padding: 15rpx 20rpx;
  color: #333;
  font-size: 30rpx;
}

.submit-submit {
  background-color: rgb(66,157,250);
  color: #fff;
  font-weight: 700;
  font-size: 30rpx;
  border-radius: 10rpx;
  padding: 18rpx 30rpx;
  margin-right: 10rpx;
  text-align: center;
}
</style>
