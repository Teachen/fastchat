"use strict";
const common_vendor = require("../../common/vendor.js");
const stores_index = require("../../stores/index.js");
const settings_index = require("../../settings/index.js");
if (!Array) {
  const _easycom_uni_icons2 = common_vendor.resolveComponent("uni-icons");
  const _easycom_uni_popup_message2 = common_vendor.resolveComponent("uni-popup-message");
  const _easycom_uni_popup2 = common_vendor.resolveComponent("uni-popup");
  (_easycom_uni_icons2 + _easycom_uni_popup_message2 + _easycom_uni_popup2)();
}
const _easycom_uni_icons = () => "../../uni_modules/uni-icons/components/uni-icons/uni-icons.js";
const _easycom_uni_popup_message = () => "../../uni_modules/uni-popup/components/uni-popup-message/uni-popup-message.js";
const _easycom_uni_popup = () => "../../uni_modules/uni-popup/components/uni-popup/uni-popup.js";
if (!Math) {
  (_easycom_uni_icons + _easycom_uni_popup_message + _easycom_uni_popup)();
}
const _sfc_main = {
  __name: "register",
  setup(__props) {
    const store = stores_index.useStore();
    const message = common_vendor.ref();
    const msgType = common_vendor.ref("success");
    const messageText = common_vendor.ref("");
    const user_info = common_vendor.reactive({
      mobile: "",
      password: "",
      sms_code: ""
    });
    const userRegister = (e) => {
      console.log(e);
      common_vendor.index.login({
        provider: "weixin",
        success(response) {
          console.log(response.code);
          common_vendor.index.request({
            method: "POST",
            url: `${settings_index.settings.host}/users/register`,
            data: {
              code: response.code,
              ...user_info,
              ...e.detail.userInfo
            }
          }).then((response2) => {
            if (response2.data.code != 200) {
              msgType.value = "error";
              messageText.value = `登陆失败!：${response2.data.err_msg}`;
            } else {
              messageText.value = `登陆成功!：${response2.data.err_msg}`;
              store.set_token(response2.data.token);
              common_vendor.index.navigateTo({
                url: "/pages/index/index"
              });
            }
            message.value.open();
          });
        }
      });
    };
    var timer = common_vendor.ref(0);
    var timer_text = common_vendor.ref("验证码");
    const sendSMS = () => {
      if (!/^1[3-9]\d+/.test(user_info.mobile)) {
        msgType.value = "error";
        messageText.value = `发送短信失败，手机格式不正确！`;
        message.value.open();
        return;
      }
      if (timer.value > 0) {
        msgType.value = "error";
        messageText.value = `发送短信失败，不能频繁点击发送！`;
        message.value.open();
        return;
      }
      common_vendor.index.request({
        method: "GET",
        url: `${settings_index.settings.host}/sms/${user_info.mobile}`
      }).then((response) => {
        console.log(response.data.err_msg);
        if (response.data.code != 200) {
          msgType.value = "error";
          messageText.value = `发送短信失败!：${response.data.err_msg}`;
        } else {
          messageText.value = `发送短信成功!：${response.data.err_msg}`;
          timer.value = 60;
          let t = setInterval(() => {
            console.log(timer.value);
            if (timer.value > 1) {
              timer.value -= 1;
              timer_text.value = timer.value;
            } else {
              timer_text.value = "验证码";
              clearInterval(t);
            }
          }, 1e3);
        }
        message.value.open();
      }).catch((error) => {
        var _a, _b;
        msgType.value = "error";
        messageText.value = (_b = (_a = error == null ? void 0 : error.response) == null ? void 0 : _a.data) == null ? void 0 : _b.err_msg;
        message.value.open();
      });
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.p({
          type: "contact",
          size: "24",
          color: "rgb(66,157,250)"
        }),
        b: user_info.mobile,
        c: common_vendor.o(($event) => user_info.mobile = $event.detail.value),
        d: common_vendor.p({
          type: "eye",
          size: "24",
          color: "rgb(66,157,250)"
        }),
        e: user_info.password,
        f: common_vendor.o(($event) => user_info.password = $event.detail.value),
        g: common_vendor.p({
          type: "checkmarkempty",
          size: "24",
          color: "rgb(66,157,250)"
        }),
        h: user_info.sms_code,
        i: common_vendor.o(($event) => user_info.sms_code = $event.detail.value),
        j: common_vendor.t(common_vendor.unref(timer_text)),
        k: common_vendor.o(sendSMS),
        l: common_vendor.o(userRegister),
        m: common_vendor.p({
          type: msgType.value,
          message: messageText.value,
          duration: 2e3
        }),
        n: common_vendor.sr(message, "bac4a35d-3", {
          "k": "message"
        }),
        o: common_vendor.p({
          type: "message"
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-bac4a35d"], ["__file", "C:/Users/Administrator/Desktop/fastapi-app/project_list/fastchat/app/pages/register/register.vue"]]);
wx.createPage(MiniProgramPage);
