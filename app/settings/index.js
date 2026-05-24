/**
 * 导包语法
 * export const   变量名   # [可用多次]允许一个变量/对象被外界导包使用，外界导包需要使用 import {变量名} from "模块名"
 * export default 变量名   # [只用一次]允许一个变量/对象被外界导包使用，外界导包需要使用 import 变量名 from "模块名"
 * export const function  # [可用多次]允许一个函数被外界导包使用，外界导包需要使用 import {变量名} from "模块名"
 */

export const settings = {
    'host': 'http://127.0.0.1:8000', // http服务端的请求地址
}
