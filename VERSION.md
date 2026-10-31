# VERSION（版本登记与依赖）

> **唯一可信版本标识 = Git Commit SHA**。下面 `V13` 仅作人类易读的协议别名，实际内容以对应 commit 为准；当同名版本（V13）指向的 commit 变更时，以 commit 为准判断内容差异。

## 当前基线

| 项 | 值 |
|---|---|
| 仓库 | `abang159357-cell/coze-guize-V1` |
| 协议别名 | `V13` |
| 协议权威源 | `core/通用研发协议.md` |
| 记录 commit | `2dcb6f4`（当前正式基线）｜上一基线 `82d56c8`（结构重组提交）；结构重组前 `28470f9`（旧 coze-guize） |
| 结构版本 | 本仓库重组为「五层结构」（core/workflows/checklists/templates/references + INDEX/VERSION/工作习惯/规范验证）所在 commit：`82d56c8`（结构重组后内容变更以「记录 commit」为准） |

> 每次结构性变更、协议条款调整、文件迁移后，在此记录新 commit，并同步 `INDEX.md` 中的引用路径与 `AGENTS.md` 目录树。

## 文件依赖关系

> 规则以 `core/通用研发协议.md` 为唯一权威源；其余文件**索引引用它、不复制细则**。改动协议会连带影响下列"依赖它的文件"——引用本表判断影响面。

```
core/通用研发协议.md  ◄── 权威源
   ├── core/任务执行与恢复.md        （执行化摘要，引用协议小节）
   ├── workflows/*（4份）            （阶段路标，引用协议章节）
   ├── checklists/*（2份）           （强制闸门，条款源自协议§四/§五）
   ├── templates/*                   （骨架，含协议摘要/索引）
   ├── references/官方依据.md        （协议条款的官方出处）
   ├── INDEX.md                      （导航表，引用所有以上路径）
   └── AGENTS.md / README.md         （仓库自身，含目录树与摘要）
```

改哪份 / 需同步：
- 改 `core/通用研发协议.md` → 检查「文件依赖关系」下游是否需描述更新；旧项目基线不变（见下）。
- 改文件路径 / 重命名 → 必须同步 `INDEX.md` 引用、`AGENTS.md` 目录树、`README.md` 目录树、本表。
- 改 `checklists/` 条款 → 属协议强制条款延伸，同步协议§四/§五总纲表述。

## 变更影响检查（每次改动前/后）

> 涉及规则/结构的重要变更（新增、删除、移动、改写规则条款）时填写本检查，判断影响范围与需重新验证的内容。

| 项 | 填空 |
|---|---|
| 本次变更内容 | — |
| 影响的文件 / 模板 / 项目 | 依据「文件依赖关系」判断 |
| 兼容性（是否破坏既有阅读/执行） | 是 / 否 / 需说明 |
| 需重新验证的内容 | 受影响文件的 INDEX 引用、交叉引用是否仍有效 |
| 旧项目基线是否受影响 | 是（需项目所有者确认升级）/ 否 |
| 处理结果 / 备注 | — |

## 规则基线登记（新项目接入用）

新项目接入时，把以下基线写入目标项目 `AGENTS.md`（来源仓库 + commit + 别名），协议后续变更须经目标项目所有者确认后才生效，不自动覆盖既有基线。

```markdown
## 变更记录
- 登记日期：<YYYY-MM-DD>
- 规则基线：来源仓库 `coze-guize-V1`，协议版本 `V13`，登记时 commit `<git rev-parse HEAD>`
- 后续协议变更须经项目所有者确认后升版本号，登记处同步更新，不自动覆盖既有基线
```

## 变更记录

| 日期 | commit | 变更内容 | 影响 | 
|---|---|---|---|
| 2026-11-01 | `9be18e7` | 从 `coze-shenghuopindao`（`dev-general-rules` + `ai-collab-protocol` + `docs/ci-security-baseline` + `AGENTS.md` 可复用纪律）与 `arcade-meter-bot-test`（无通用内容）提取通用方法，沉淀为 `references/依赖与CI治理.md`（依赖告警处置/升级验证/技术债防护/交付硬闸门/发布探针铁律/E2E范式/CI安全基线/上线前环境变量核对）；并在 `core/通用研发协议.md` §六.7、`checklists/上线前后检查.md` §36、`INDEX.md`/`README.md`/`workflows/Git与CI.md` 加索引与精简引用 | `references/依赖与CI治理.md`（新增）、`core/通用研发协议.md`、`checklists/上线前后检查.md`、`INDEX.md`、`README.md`、`workflows/Git与CI.md`，见「文件依赖关系」 |
| 2026-11-01 | `260e4c9` | 统一全仓仓库名：`coze-guide`（拼写错误）与作为接入对象的 `coze-guize` 一律改为 `coze-guize-V1`（仅保留"旧 coze-guize"对比说明） | `AGENTS.md`/`VERSION.md`/`references/官方依据.md`/`templates/项目接入.md`，见「文件依赖关系」 |
| 2026-11-01 | `048c659` | 对上一批沉淀做复查自检收口：核对 `references/依赖与CI治理.md` 对源仓库 `coze-shenghuopindao` 三份可复用文件的覆盖完整性（ai-collab-protocol 六章↔§一~六、ci-security-baseline↔§七、上线配置清单核对法↔§八），剔除项目专属内容 | `references/依赖与CI治理.md` 及全仓交叉引用，见「文件依赖关系」 |
| 2026-11-01 | `2dcb6f4` | 修正 `templates/AGENTS.md.template` 中残留的旧文件名引用（`推送与CI交接.md`→`Git与CI.md`、`上线前规定.md`→`上线前后检查.md`、`_依据核实.md`→`官方依据.md`） | `templates/AGENTS.md.template` |
| 2026-11-01 | `2dcb6f4`后续（本次） | ①更新当前基线至 `2dcb6f4`（此前误记为 `82d56c8`，导致与真实版本不一致）；②回填变更记录占位符；③裁定接入哲学为「固定基线」，删除 `AGENTS.md.template`/`项目接入.md` 中"完整版见仓库并按最新版执行"的双轨表述 | `VERSION.md`、`templates/AGENTS.md.template`、`templates/项目接入.md` |