# 投资记录面板

一个纯静态的个人投资记录面板：手工维护 JSON 数据，页面展示总资产、累计收益走势、资产配置、持仓基金卡片与交易明细。无后端、无框架依赖，单个 `index.html` 即是全部前端。

> **说明**
> - 仓库内的数据（`trading_records/` 等四个目录）**全部为虚构示例数据**，仅用于演示，不代表任何真实投资。
> - 文档与配置中的域名、邮箱等均为占位符；真实部署信息已脱敏。
> - 仓库不包含任何凭据。部署所需的 `cf_token.txt` / `cf_account.txt` 已在 `.gitignore` 中排除，需自行创建。

## 功能

- 总资产 / 累计收益 / 收益率等指标卡
- 累计收益走势图（可按区间缩放）
- 资产配置环形图（含「现金宝」现金资产）
- 持仓基金卡片 → 点击进入单基金详情（收益走势 + 交易明细）
- 交易 / 分红 / 出入金记录表

## 本地预览

双击 `start.bat`（或 `python serve.py 8686`），浏览器打开 http://localhost:8686/index.html 。
服务已禁用缓存，改数据后 F5 刷新即可。

## 数据格式

四个数据目录，手工编辑 JSON：

| 目录 | 内容 | 文件组织 |
|---|---|---|
| `trading_records/` | 基金买卖流水 | `YYYY/YYYY_MM.json` + `index.json` |
| `dividend_records/` | 分红记录 | 同上 |
| `payment_records/` | 现金宝充值/收益 | 同上 |
| `navs/` | 每日净值 | `YYYY-MM.json` + `index.json` |

**新增月份文件后必须登记到对应 `index.json` 的 `files` 数组**，否则不会加载。字段细节见 [数据说明.md](数据说明.md)。

## 部署

### 任意静态托管

`python build_publish.py` 会把 `index.html` + 四个数据目录打包到 `invest-publish/`（并注入 noindex 标签），把这个目录丢到任何静态托管即可。

### Cloudflare Pages（含 Access 访问锁）

1. 准备两个文件（不会入库）：
   - `cf_token.txt`：Cloudflare API Token（需 Pages Edit 权限）
   - `cf_account.txt`：Account ID
2. 修改 `更新面板.bat` 中 `--project-name=your-project-name` 为你自己的项目名
3. 双击 `更新面板.bat`：自动打包并调用 `wrangler pages deploy` 上传（注意 wrangler 主版本需与你的 Node 版本匹配，脚本锁定 `@3` 适配 Node 18）
4. （可选）在 Cloudflare Zero Trust 中创建 Access 应用罩住你的域名，策略按邮箱放行——即可实现「输邮箱收验证码才能看」的私密面板

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 全部前端（样式 + 逻辑） |
| `build_publish.py` | 打包到 `invest-publish/` |
| `更新面板.bat` | 一键部署到 Cloudflare Pages（Windows） |
| `serve.py` / `start.bat` | 本地预览（禁缓存） |
| `数据说明.md` | 数据 JSON 字段详解 |
