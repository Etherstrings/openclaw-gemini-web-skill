# OpenClaw Gemini Web Skill

一个通过 OpenClaw 托管浏览器驱动 Gemini 网页版的 skill 项目。

## <a id="donate"></a>赞助支持

如果这个项目对你有帮助，欢迎赞助支持继续迭代。

- GitHub 页面右上角可直接点击 `Sponsor`
- 如果你更习惯国内付款方式，可以直接扫码赞助

<div>
  <img src="docs/assets/donate/alipay.jpg" alt="Alipay QR" width="260" />
  <img src="docs/assets/donate/wechat.jpg" alt="WeChat Pay QR" width="260" />
</div>

支持会优先用于浏览器自动化测试、模型调用和后续功能迭代。

## 功能简介

- 复用 OpenClaw 浏览器档案中的 Gemini 登录状态
- 当 OpenClaw 当前运行上下文里已经有密钥时，执行尽力而为的自动登录
- 无需第三方依赖即可生成 TOTP / 2FA 验证码
- 支持 Gemini 文本对话、线程续接、文件和图片上传、分析与起草任务、图片生成以及下载处理

## 已验证流程

这个项目已经在干净的 OpenClaw 浏览器档案中完成过端到端实测：

- Google 账号邮箱输入步骤
- Google 密码输入步骤
- Google Authenticator TOTP / 两步验证步骤
- 成功进入 `https://gemini.google.com/app`
- 在 Gemini 内成功完成一轮提示词与回复闭环

## 项目结构

```text
skills/openclaw-gemini-web/
  SKILL.md
  scripts/totp.py
tests/
  test_totp.py
```

## 本地验证

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
openclaw skills list
openclaw skills info openclaw-gemini-web
```

请在仓库根目录运行 OpenClaw 命令，这样工作区级别的 `skills/` 目录才能被正确识别。

## TOTP 辅助工具

示例：

```bash
python3 skills/openclaw-gemini-web/scripts/totp.py --secret JBSWY3DPEHPK3PXP
python3 skills/openclaw-gemini-web/scripts/totp.py --env GEMINI_WEB_TOTP_SECRET
python3 skills/openclaw-gemini-web/scripts/totp.py --uri 'otpauth://totp/Gemini:me@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Gemini'
```

## 发布到 ClawHub

```bash
clawhub publish skills/openclaw-gemini-web \
  --slug openclaw-gemini-web \
  --name "OpenClaw Gemini Web" \
  --version 0.1.4 \
  --changelog "将仓库文档与技能说明切换为中文"
```
