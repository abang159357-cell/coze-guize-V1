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
   ├── scripts/verify-references.py  （引用有效性校验，守护索引/交叉引用不失效）
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
| 本次变更内容 | ①`references/平台专项规则.md` 占位降级（`[DRAFT-待补]` 标记，未定稿不视为现行规则，验证记录表 `（示例）`→`（待填）`）②`references/官方依据.md` 增加「核实基准与复核周期」（锚定 commit、日期 2026-11-01）③新增 `scripts/verify-references.py` 引用有效性校验并登记进 `规范验证.md` |
| 影响的文件 / 模板 / 项目 | 按「文件依赖关系」：`references/平台专项规则.md`、`references/官方依据.md`、`scripts/verify-references.py`（新增）、`规范验证.md`、`VERSION.md`，以及引用以上文件的 `INDEX.md`/`README.md`/`AGENTS.md`（本轮不改，交由校验脚本守护） |
| 兼容性（是否破坏既有阅读/执行） | 否；新增 DRAFT 标注与校验脚本均不改变既有条款语义，仅显式化草稿边界与机器校验入口 |
| 需重新验证的内容 | 跑 `python3 scripts/verify-references.py` 确认无死链；`INDEX.md`/`README.md`/`AGENTS.md` 对 `references/`、`scripts/` 引用是否仍有效 |
| 旧项目基线是否受影响 | 否（本轮为草稿降级与校验增强，不改变已定稿规则基线；若要纳入旧项目基线由项目所有者确认） |
| 处理结果 / 备注 | 校验脚本实测通过（147 条引用全有效）；待本次 commit 后回填变更记录 commit |

## 规则基线登记（新项目接入用）

新项目接入时，把以下基线写入目标项目 `AGENTS.md`（来源仓库 + commit + 别名），协议后续变更须经目标项目所有者确认后才生效，不自动覆盖既有基线。

```markdown
## 变更记录
- 登记日期：<YYYY-MM-DD>
- 规则基线：来源仓库 `coze-guize-V1`，协议版本 `V13`，登记时 commit `<git rev-parse HEAD>`
- 后续协议变更须经项目所有者确认后升版本号，登记处同步更新，不自动覆盖既有基线
```

## 变更必须同步项（每次改规则后逐项过，防跨层失同步）

> 单一权威源承诺靠"改一处、同步其余"落地。任何改动（尤其动 `core/通用研发协议.md`、`INDEX.md`、`README.md`、`AGENTS.md`、`references/` 引用）后，按下表逐项核对；无法同步的在本次变更影响栏写明"无需同步 + 原因"，不留默认的空洞。

| 变更类型 | 必须同步 | 校验方法 |
|---|---|---|
| 改动核心协议条文 | 本条同步进 `INDEX.md`（情况→文件→协议节→checklist 映射）、`README.md`（主线段落如有引用）、`AGENTS.md`（仓库自身记忆）、`references/官方依据.md`（如有官方依据）、本变更记录、目标项目 `AGENTS.md` 基线需项目所有者确认 | `python3 scripts/verify-references.py` + 人工核对映射 |
| 增删改文件 / 改路径 | `INDEX.md`、`README.md` 目录树、`AGENTS.md` 目录树、本变更记录 | `scripts/verify-references.py` 检出死链 |
| 改动引用 / 重组引用 | `INDEX.md`、`README.md`、`AGENTS.md`、受影响文件、本变更记录 | `scripts/verify-references.py` |
| 新增/修改证据 | `references/官方依据.md`（更新核实基准 commit/日期）、本变更记录 | 人工 + 复核周期 |

### 协议变更后的回归要求

1. 协议 (或任一被引用文件) 变更后，先按「**文件依赖关系**」识别影响范围。
2. 使受影响范围内的既有验证结论失效（见 `规范验证.md`「证据绑定版本」）。
3. 对失效范围跑一次 `python3 scripts/verify-references.py` **必过**，再做定向人工回归（`规范验证.md`「受控验证场景」选 2~3 个相关项）。
4. 所有回归结果记入 `规范验证.md`「结论记录」并绑定 commit，**不以"已改文档"当"已验证"**。

## 变更记录

| 日期 | commit | 变更内容 | 影响 | 
|---|---|---|---|
| 2026-11-01 | `9be18e7` | 从 `coze-shenghuopindao`（`dev-general-rules` + `ai-collab-protocol` + `docs/ci-security-baseline` + `AGENTS.md` 可复用纪律）与 `arcade-meter-bot-test`（无通用内容）提取通用方法，沉淀为 `references/依赖与CI治理.md`（依赖告警处置/升级验证/技术债防护/交付硬闸门/发布探针铁律/E2E范式/CI安全基线/上线前环境变量核对）；并在 `core/通用研发协议.md` §六.7、`checklists/上线前后检查.md` §36、`INDEX.md`/`README.md`/`workflows/Git与CI.md` 加索引与精简引用 | `references/依赖与CI治理.md`（新增）、`core/通用研发协议.md`、`checklists/上线前后检查.md`、`INDEX.md`、`README.md`、`workflows/Git与CI.md`，见「文件依赖关系」 |
| 2026-11-01 | `260e4c9` | 统一全仓仓库名：`coze-guide`（拼写错误）与作为接入对象的 `coze-guize` 一律改为 `coze-guize-V1`（仅保留"旧 coze-guize"对比说明） | `AGENTS.md`/`VERSION.md`/`references/官方依据.md`/`templates/项目接入.md`，见「文件依赖关系」 |
| 2026-11-01 | `048c659` | 对上一批沉淀做复查自检收口：核对 `references/依赖与CI治理.md` 对源仓库 `coze-shenghuopindao` 三份可复用文件的覆盖完整性（ai-collab-protocol 六章↔§一~六、ci-security-baseline↔§七、上线配置清单核对法↔§八），剔除项目专属内容 | `references/依赖与CI治理.md` 及全仓交叉引用，见「文件依赖关系」 |
| 2026-11-01 | `2dcb6f4` | 修正 `templates/AGENTS.md.template` 中残留的旧文件名引用（`推送与CI交接.md`→`Git与CI.md`、`上线前规定.md`→`上线前后检查.md`、`_依据核实.md`→`官方依据.md`） | `templates/AGENTS.md.template` |
| 2026-11-01 | `2dcb6f4`后续（本次） | ①更新当前基线至 `2dcb6f4`（此前误记为 `82d56c8`，导致与真实版本不一致）；②回填变更记录占位符；③裁定接入哲学为「固定基线」，删除 `AGENTS.md.template`/`项目接入.md` 中"完整版见仓库并按最新版执行"的双轨表述 | `VERSION.md`、`templates/AGENTS.md.template`、`templates/项目接入.md` |
| 2026-11-01 | `32f71e1` | 审查整改三处：①`references/平台专项规则.md` 占位降级（`[DRAFT-待补]`，未定稿不视为现行规则，验证记录表 `（示例）`→`（待填）`）②`references/官方依据.md` 增加「核实基准与复核周期」（锚定 commit、日期）③新增 `scripts/verify-references.py` 引用有效性校验并登记进 `规范验证.md` | `references/平台专项规则.md`、`references/官方依据.md`、`scripts/verify-references.py`（新增）、`规范验证.md`、`VERSION.md` |
| 2026-11-01 | 本次 | **定位校准 + 结构与回归机制加固**：A①官方依据"两部分→五分类"表述对齐（含结论可信度层级语境）；A②README/AGENTS 增「定位声明」与「局限」（明确=模板库+平台实践，非官方标准/不构成对外正式制度）；A③`规范验证.md` 补「结论记录」表（目标/步骤/结果/失败原因/commit）+ 失败记录优先原则；B④协议「四件事分开」总纲 + 标签即证据归属；B⑤VERSION 增「变更必须同步项清单 + 协议变更回归要求」 | `references/官方依据.md`、`README.md`、`AGENTS.md`、`规范验证.md`、`core/通用研发协议.md`、`VERSION.md` |