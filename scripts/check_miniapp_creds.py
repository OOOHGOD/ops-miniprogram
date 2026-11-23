# -*- coding: utf-8 -*-
"""
微信小程序 AppID/AppSecret 连通性与权限范围自检脚本
用法（凭据只走环境变量，绝不落盘）：
    APPID=wx... APPSECRET=... python check_miniapp_creds.py
"""
import json
import os
import sys
import urllib.request
import urllib.error

BASE = "https://api.weixin.qq.com"
TIMEOUT = 15

APPID = os.environ.get("APPID", "").strip()
APPSECRET = os.environ.get("APPSECRET", "").strip()

ERR_HINT = {
    40164: "服务器 IP 未加入 IP 白名单（去 mp 后台 开发管理→开发设置 添加本机公网 IP，或临时关闭白名单）",
    40013: "AppID 无效",
    40001: "AppSecret 无效或被重置过",
    40125: "AppSecret 无效（invalid appsecret）",
    89503: "需要管理员确认（new appid），先去后台完成管理员确认",
    -1: "微信侧系统繁忙，稍后再试",
}


def http_json(method, url, payload=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, {"raw": body}
    except Exception as e:  # 网络层错误
        return None, {"error": f"{type(e).__name__}: {e}"}


def show(name, status, obj):
    errcode = obj.get("errcode", 0)
    ok = status == 200 and errcode in (0, None)
    mark = "OK " if ok else "FAIL"
    print(f"[{mark}] {name}")
    if errcode not in (0, None):
        hint = ERR_HINT.get(errcode, "")
        print(f"      errcode={errcode} errmsg={obj.get('errmsg')} {hint}")
    elif "error" in obj:
        print(f"      网络错误: {obj['error']}")
    else:
        print(f"      {json.dumps(obj, ensure_ascii=False, indent=2)}")
    return ok


def main():
    if not APPID or not APPSECRET:
        print("缺少 APPID / APPSECRET 环境变量")
        sys.exit(2)

    print(f"AppID: {APPID}   AppSecret: {APPSECRET[:4]}...{APPSECRET[-4:]} (已打码)")
    print("=" * 60)

    # 1. 换 access_token
    status, tok = http_json(
        "GET", f"{BASE}/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    )
    ok = show("1. 获取 access_token", status, tok)
    if not ok or "access_token" not in tok:
        print("\n凭据校验未通过，后续检查中止。")
        sys.exit(1)
    token = tok["access_token"]
    print(f"      token 有效期 {tok.get('expires_in')}s（已获取，不回显）")

    # 2. 账号主体信息（认证状态、主体名）
    status, info = http_json("GET", f"{BASE}/cgi-bin/account/getaccountbasicinfo?access_token={token}")
    show("2. 账号主体信息（含认证状态/主体）", status, info)

    # 3. 服务器域名配置
    status, dom = http_json("POST", f"{BASE}/wxa/modify_domain?access_token={token}", {"action": "get"})
    show("3. 服务器域名配置（request/uploadFile/socket/downloadFile）", status, dom)

    # 4. 类目
    status, cat = http_json("GET", f"{BASE}/cgi-bin/wxopen/getcategory?access_token={token}")
    show("4. 小程序已设置类目", status, cat)

    # 5. 云开发环境列表（未开通会报错）
    status, env = http_json("POST", f"{BASE}/tcb/describecloudbaseenvs?access_token={token}", {})
    show("5. 云开发环境列表", status, env)

    print("=" * 60)
    print("检查完毕。提醒：这组 AppSecret 已在聊天中出现过，建议到后台重置后再长期使用。")


if __name__ == "__main__":
    main()
