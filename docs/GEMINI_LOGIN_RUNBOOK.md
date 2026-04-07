# Gemini 登录与地区排查手册

这份手册沉淀的是已经实测跑通的一条稳定路径，目标是避免以后把“没登录成功”“浏览器被 Google 风控”“Gemini 真正的地区限制”混在一起误判。

## 结论先行

- 只要 `https://gemini.google.com/app` 能正常打开，且页面没有直接显示“当前地区不支持 Gemini”之类的文案，就不要提前判定为地区问题。
- 在这次实测里，真正稳定的路径不是“新起一个自动化浏览器直接登 Google”，而是“真 Chrome 或 OpenClaw 托管浏览器 + 复用现成会话 + 必要时用 TOTP 补 2FA”。
- Gemini 不只是能打开首页，而是已经实测完成过一次真实消息往返：发送 `Reply with exactly: READY`，页面返回 `READY`。

## 已验证通过的基线

这轮排查中，以下条件组合已经验证成功：

- 代理出口位于美国
- Gemini 首页可正常打开
- Google 邮箱与密码步骤可完成
- 二步验证可切到 Google Authenticator 路径
- TOTP 页真实输入框为 `#totpPin`
- 用仓库自带的 `scripts/totp.py` 生成 6 位验证码后可提交成功
- 提交后能够进入 Gemini 会话页
- `https://myaccount.google.com/personal-info` 可正常打开
- 在 Gemini 会话里发送测试 prompt 后收到有效回复

## 推荐判断顺序

### 1. 先分清是“未登录”还是“被地区拦截”

优先看 `https://gemini.google.com/app` 的实际页面内容：

- 如果看到 `登录` 按钮、账号表单、账号选择器，说明当前主要问题还是登录态。
- 如果已经有聊天输入框或会话界面，说明 Gemini 基本可用。
- 只有当页面明确出现地区不支持文案时，才把它归类为地区问题。

不要仅凭“打不开对话”“跳回登录页”“新浏览器出现 502”就直接认定是地区限制。

### 2. 优先复用真实浏览器会话

优先级建议：

1. OpenClaw 托管浏览器里已经登录的 Gemini 标签页
2. OpenClaw 托管浏览器里的同一档案继续登录
3. 真 Chrome + CDP 接管现有会话

不推荐把“全新自动化浏览器直接登录 Google”作为首选，因为这次实测里它更容易触发：

- `This browser or app may not be secure`
- 页面空白或 502

这些现象更像 Google 的浏览器风控，不等于 Gemini 地区不支持。

### 3. 遇到 2FA 时直接走 TOTP

当 Google 进入二步验证并提供“从 Google 身份验证器应用获取验证码”时：

1. 切到该验证方式
2. 用仓库脚本即时生成验证码
3. 把验证码填入 `#totpPin`
4. 立刻提交，避免验证码过期

示例：

```bash
python3 skills/openclaw-gemini-web/scripts/totp.py --env GEMINI_WEB_TOTP_SECRET
```

### 4. 登录成功后做双重确认

不要停留在“好像进去了”。至少做下面两步：

1. 打开 `https://myaccount.google.com/personal-info`
   这一步用来确认 Google 账号本身已经真的登录。
2. 回到 `https://gemini.google.com/app` 发一条最小测试消息
   推荐：`Reply with exactly: READY`

只有当 Gemini 确实返回内容时，才说明“登录 + Gemini 交互”这条链路都通了。

## 这次排查中容易误判的点

### Playwright 直接新开浏览器失败

这次排查里，直接 `launch()` 新浏览器去登 Google，曾多次出现：

- `This browser or app may not be secure`
- Gemini 首屏 502

这不应被解释成账号坏了，也不应直接解释成地区限制。更合理的动作是切回真 Chrome 或 OpenClaw 托管浏览器，继续复用已有会话环境。

### Lightpanda 返回 502

这次实测中，Lightpanda 打开 Gemini 直接 502，因此不适合作为这条登录链路的唯一依据。它更适合做轻量 DOM 任务，不适合作为 Google 登录问题的最终判官。

### 账号资料页地区为空

这次确认过 Google 账号资料页中的地址项均为未设置，因此“资料页里绑了中国地址导致 Gemini 被封地区”并不是这次的根因。

## 最后该怎么归因

如果满足下面三件事：

- Google 账号已经成功登录
- Gemini 已经完成最小消息往返
- 页面没有出现地区不支持文案

那就应把问题归类为“之前的浏览器环境或出口环境不稳定”，而不是“账号本身无法使用 Gemini”。

只有在登录完成之后，Gemini 仍然明确显示地区不支持页面，才应继续按地区策略问题追查。
