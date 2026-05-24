"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {};
if (!Array) {
  const _easycom_uni_icons2 = common_vendor.resolveComponent("uni-icons");
  _easycom_uni_icons2();
}
const _easycom_uni_icons = () => "../../uni_modules/uni-icons/components/uni-icons/uni-icons.js";
if (!Math) {
  _easycom_uni_icons();
}
function _sfc_render(_ctx, _cache) {
  return {
    a: common_vendor.p({
      type: "contact",
      size: "24",
      color: "rgb(66,157,250)"
    }),
    b: common_vendor.p({
      type: "eye",
      size: "24",
      color: "rgb(66,157,250)"
    }),
    c: common_vendor.p({
      type: "checkmarkempty",
      size: "24",
      color: "rgb(66,157,250)"
    }),
    d: common_vendor.p({
      type: "qq",
      size: "40",
      color: "rgb(66,157,250)"
    }),
    e: common_vendor.p({
      type: "weixin",
      size: "40",
      color: "rgb(2,187,17)"
    }),
    f: common_vendor.o((...args) => _ctx.wxLogin && _ctx.wxLogin(...args))
  };
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-e4e4508d"], ["__file", "C:/Users/Administrator/Desktop/fastapi-app/project_list/fastchat/app/pages/login/login.vue"]]);
wx.createPage(MiniProgramPage);
