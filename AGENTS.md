# AGENTS.md

## 项目概述
跨项目复用的通用研发协作规范仓库（coze-guize-V1）。无业务代码，是一套「稳定、可信、可长期运营」的研发规则底座。结构为五层：core（规则权威源）/ workflows（流程框架）/ checklists（强制闸门）/ templates（可复制模板）/ references（参考依据）+ 顶层 INDEX/VERSION/工作习惯/规范验证。其他项目初始化时参阅本仓库接入各自 AGENTS.md。

## 技术栈
无技术栈、无源码、无运行入口、无依赖、无构建产物。纯 Markdown + 模板文件。

## 目录结构
```
.
├── README.md                 # 门面：本项目说明 + 生命周期主线
├── INDEX.md                  # ★AI 导航总索引（情况→文件→协议节→checklist）；AI 每任务先读
├── VERSION.md                # 版本登记（git commit 绑定）+ 文件依赖关系 + 变更影响检查
├── core/
│   ├── 通用研发协议.md        # ★唯一权威源（全部条款原文，其他文件只索引引用，防双源漂移）
│   └── 任务执行与恢复.md      # AI 无人值守执行入口（执行循环/授权裁决/中断恢复）
├── workflows/
│   ├── 需求与计划.md          # 阶段①②
│   ├── 开发测试与排障.md      # 阶段③
│   ├── Git与CI.md            # 阶段④（原 推送与CI交接.md）
│   └── 交付上线与维护.md      # 阶段⑤-⑧
├── checklists/
│   ├── 交付前检查.md          # 每轮改动强制闸门（原 交付前规定.md）
│   └── 上线前后检查.md        # 上线评估+对抗测试+上线后核对（原 上线前规定.md）
├── templates/
│   ├── AGENTS.md.template
│   ├── 项目接入.md            # 可复制接入协议（原 接入模板.md）
│   ├── 执行计划.md.template
│   └── 交付报告.md.template  # 【新增】
├── references/
│   ├── 官方依据.md            # 各规则官方依据（原 _依据核实.md）
│   └── 平台专项规则.md        # 【新增】平台/技术栈专项（取证原则，不凭空起草）
├── 工作习惯.md               # 常用工作规则（接入时复制进项目 AGENTS.md，与协议分离）
├── 规范验证.md               # 元治理：验证规则是否真被读取/执行
├── .coze                     # 项目配置（纯文档，无部署/无预览；sub_id 8a5f35c0）
└── .gitignore
```

## 关键入口 / 核心模块
- **AI 导航入口**：`INDEX.md`（每次开工先读）
- **规则权威源**：`core/通用研发协议.md`（其他文档的条款都以它为源，避免双源漂移）
- **无人值守执行入口**：`core/任务执行与恢复.md`
- **展示与定位入口**：`README.md`
- **落地与验收**：`templates/`、`checklists/`、`VERSION.md`

## 运行与预览
- 非预览型项目（`project_type = ""`），`preview_enable = "disabled"`，不写 `[dev]`。
- 无可部署产物，`general-deploy` 判定不命中任何 deploy profile，故 `.coze` 不含 `[deploy]`。
- 验证方式：文档内容与 git 版本管理，无运行/构建/测试链路。

## 用户偏好与长期约束
- 文档互为引用时以 `core/通用研发协议.md` 为准，不手抄细则，避免双源漂移。
- 平台硬约束（端口 5000、pnpm/uv、`.coze` 落点、`sub_id` 不可改）与仓库规则冲突时以平台约束为准。
- **图片/截图/临时附件一律不进 git（尤其在未 push 的历史里），已入库的需改写历史剥离，避免污染 commit 历史**；`.gitignore` 已固化 `assets/` 与图片后缀，遗漏时务必补记。
- **改写 git 历史（reset --hard / 改写 commit）属高危操作，执行前必须经用户明确授权**；未 push 的本地历史改写安全，push 后禁止破坏性改写。
- 本仓库自 `旧 coze-guide（coze-guide）` 迁移而来，旧仓库冻结不动作；本地工作区绑定 `coze-guize-V1` remote，版本以 git commit 为准（见 `VERSION.md`）。

## 常见问题和预防
- 新项目接入本仓库规范时，应把「规则基线」（来源仓库 + 登记版本/commit）写入目标项目 AGENTS.md，协议后续变更须经项目所有者确认后才生效，不自动覆盖既有基线。
- 创建/修改文件先读最新状态再动手；改动规则或文件路径后同步更新 `INDEX.md`、`README.md` 与本文件目录树，避免引用失效（见 `VERSION.md` 变更影响检查）。