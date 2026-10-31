# 依赖治理与 CI 安全基线（通用方法）

> **层级**：references（参考依据）· **性质**：跨项目可复用的「依赖告警处置、依赖升级验证、交付硬闸门、发布类探针、E2E 范式、CI 安全基线」方法。基于真实项目线上实测沉淀（大其力生活平台、arcade-meter-bot-test），其余项目照此执行即可，无需从零踩坑。
>
> **取证原则**：文内涉官方机制处均标注「官方/实测」；未核实项标「待核实」，不充当可信规则。规则不含具体项目版本号——那是项目快照，落地时结合各项目 `AGENTS.md` 依赖记录执行。

---

## 一、依赖安全告警处置：面板数字 ≠ 实际风险

安全工具面板（如 `pnpm audit --prod`）的告警数量**不等于实际运行时攻击面**。逐项判定后再处置，按以下优先级（实测沉淀）：

| 告警类型 | 判定依据 | 处置 |
|---|---|---|
| **直接 runtime 依赖** | `pnpm why` 定位到 `dependencies`（production）；`src/` 确有引用 | **优先升级**，目标命中 advisory 声明的修复门槛（"需 ≥ X.Y.Z"） |
| **未使用资源** | 依赖仅存在于某 SDK 嵌套链，`src/` 零 import（如模板残留的 S3/builder） | 记录"不适用"，**不 override、不升级**；新增引用时触发技术债防护重估 |
| **构建链 / dev-only** | 仅在框架→babel 编译链或 dev 环境加载，runtime 不引用 | 记录"不适用"，不处理；进 runtime 时重估 |
| **确在生产链的传递依赖** | `pnpm why` 确认来自生产 SDK 嵌套链 | 用 `pnpm.overrides` **精确升到修复版本**（impact 最小化） |
| **工具大版本升级**（CI setup-node 等） | 多为 warning 非 error | **推迟**：跨 N 大版本需重新 pin + 同步安全基线脚本，收益(去警告) < 风险(CI 行为变化) |

**验证升级**：升级后必须核 `pnpm-lock.yaml` 实际解析版本（`grep '^  <pkg>@'`），只改 package.json 不同步 override 会不生效或产生脏 lock。

---

## 二、依赖升级验证流程（勿仅凭 build 绿判定）

跨 N 个 minor 的升级按序执行，逐步留证：

1. **查告警**：`pnpm audit --prod` 定位命中项与修复门槛。
2. **确认依赖身份**：是 runtime 还是 dev；读 package.json 看是否受 `pnpm.overrides` 约束。
3. **升级 / 加 override**：runtime 依赖用 `pnpm add`（勿用 `-D` 降级）；受 override 约束的同时更新 override。
4. **静态**：`ts-check` + `lint` + 单元测试。
5. **真实构建**：跑完整框架构建（如 `next build`）+ 服务端产物构建（如 tsup）——`ts-check` 绿 ≠ `build` 绿（前者不编译 RSC/serialization/服务端产物）。
6. **真实链路冒烟**：重启 dev 后走通真实链路（登录→写库→发布→读详情→越权/伪造被拒），自建自清。

**关键教训**：`build 绿` 只能证明可编译，不能证明依赖升级的运行时行为符合预期；生产链路（鉴权/写库/读接口）必须真实冒烟。

---

## 三、技术债防护（"不适用"结论的失效条件）

"不适用 / 推迟"的判定**基于当时代码快照**。以下任一条件满足即令旧结论失效，需重估是否 override 或升级：

- 新增 / 启用了曾被标记为未使用的依赖（如启用某 SDK）；
- `src/` 新增对被标记"不适用"依赖的 import（将其引入 runtime/build）；
- 上游 SDK 或框架升级改变了对应依赖的引入方式；
- 主动发起被延期的工具大版本升级。

触发时：重跑 `pnpm audit --prod` + `pnpm why` 复核来源，再决定 override 或升级，**勿沿用旧"不适用"结论**。

---

## 四、交付硬闸门：真实 build + 工作区干净

"代码改动可交付"判定的最后一步，除静态检查 / 单测 / 服务探活外：

1. **必须真实跑完整 `pnpm build`**（含框架构建 + 服务端产物）。注意：交付验收工具（如 web 的 `test_run`）只跑 lint/ts-check/探活，**不含 build**；`ts-check` 绿 ≠ build 绿。
2. **清理 build 副作用**：如 `next build` 会改动 `next-env.d.ts` 等被跟踪文件，交付前 `git restore --staged --worktree next-env.d.ts` 等清掉，确保工作区干净、不污染提交。
3. **检查空 / 重复提交**：同一会话多次收尾可能生成同 message 的空提交（`git diff-tree --no-commit-id --name-only -r <sha>` 文件数为 0 即空提交）。交付前 `git log --oneline -3` 检查，有则移除（仅限未推送本地历史用 `git reset --soft HEAD~1`）。
4. **最终自检**：确认无空提交、无重复、本地与远端同步（`git status` 干净）、最新 HEAD 的远端 CI 为绿，才收口。

---

## 五、发布类探针铁律：覆盖全角色 + 跳转闭环

**反例（真实项目已发生）**：发布探针只测单个角色、且只断言「发布接口 200」，从不发布后跟随跳转验详情页——结果另一角色发布写 A 表、却跳 B 角色详情页（只查 B 表）→ **上线后真实用户发布即 404**，而全部自动化 check（单测/ts-check/build/接口探针）全绿。

**沉淀结论**——凡"发布类"探针/冒烟必须满足：

1. **全角色覆盖**：所有发布入口分支都要测，不能只测最容易的角色。
2. **跳转闭环断言**：发布成功后，`fetch` 服务端返回的 `data.id` 拼接跳转 URL 并**断言详情页非 404**。**"写库 200" 不等价于 "详情页可渲染"** ——接口返回成功 ≠ 用户页面能打开，两者必须分开断言。
3. **用户旅程视角**：验证以「用户真实走通」（发布 → 跟随跳转 → 页面渲染）为验收，而非仅「后端接口正确性」。接口对、不等于用户点起来对。

**通用教训**：任何涉及「写入后跳转到某页面」的功能，检查机制必须在跳转目标处也断言——层级间的"界面↔数据表"错位（如跳转路由与查询表不匹配）只会被"发布后跟随跳转验 200"逮住，单测与接口探针都覆盖不到。

---

## 六、发布/跳转类验证：官方 E2E 范式优先（复用，非自研）

**原则**：涉及"用户真实走通"（登录 → 提交 → 跳转 → 页面渲染）的验证，**优先复用官方 E2E 框架**（Playwright / Cypress），不手写接口探针充当用户旅程。判断是否该用 E2E：验证目标是否为「界面状态/跳转目标/页面可渲染」——是则 E2E，接口探针只承担"后端契约正确性"。

**E2E 关键断言**：用框架的**导航等待 + DOM/URL 断言**捕捉层级错位：
- `waitForURL('/目标/**')` 天然抓「跳转目标路由错误」（发布后跳错页 → 立即红）
- 断言目标页**真实渲染出业务实体**（名称/关键按钮可见），而非仅 HTTP 200
- 诀窍：**"写库 200" 与 "页面能渲染" 是两件事**，必须分开断言

**CI 接入标准骨架**：
- E2E job 用官方 checkout/setup-node/包管理器 action（pin 可信 SHA），显式 `install --frozen-lockfile` + 构建 + 起服务
- **secrets 守卫**：`${{ secrets.X }}` 缺失时 job 安全跳过不红、配好即启用——骨架可先入库不阻塞 CI
- 测试数据用 **secrets 注入**，不落仓库明文

**环境隔离（硬红线）**：E2E 探针会「自建数据→写→删」，**必须连独立测试数据库/服务**（可反复清空），**绝不连线上或开发库**——否则每次构建都往真实数据旁灌假数据再删，污染且不可回退。

**回归价值**：E2E 用例承担「界面↔数据层耦合」的回归守卫，任何一侧改动（路由、查表逻辑、隐私字段）都可能打破它而变红；修复某类 bug 后，把对应路径固化成 E2E 用例，防止同类问题复发。

---

## 七、CI 安全基线（repo 标准模板）

> 用途：GitHub Actions workflow 的**统一安全基线**。新增/修改 workflow 必须满足本模板，由 zizmor 常驻 job 做机器校验兜底（CI 红即违约）。

### 1. 必守基线（违反即 zizmor/CI 红）

| # | 规则 | 模板写法 | zizmor 校验 |
|---|---|---|---|
| 1 | 顶层 `permissions: {}`（关闭默认权限） | `permissions: {}` | `excessive-permissions` |
| 2 | job 级最小权限（每 job 只给需要的一项） | 例 `test` job: `permissions: contents: read` | `excessive-permissions` |
| 3 | 第三方 action 一律 pin commit SHA（+ 注释 tag） | `uses: actions/checkout@11d5960a…# v4.x.x` | `unpinned-threshold` |
| 4 | checkout 不带凭据进产物 | `with: persist-credentials: false` | `artipacked` |
| 5 | 容器/镜像不用 `latest`，pin 版本 | 容器可用时 pin digest | `unpinned-images` |
| 6 | 固定工具版本（不用漂移的 latest） | 如 `pip install semgrep==x.y.z` | — |

### 2. action → SHA 对照（升级时同步更新，勿重写裸 `@vN`）

> 表中 SHA 为示例占位；实际以官方发布为准。升级流程：Dependabot 开 PR → PR 中同时更新 SHA（GitHub UI 会提示）→ 本地静态检查 + 真实 build → 云端双绿。**勿手写裸 tag。**

| action | 方式 | 何时升级 |
|---|---|---|
| `actions/checkout` | pin commit SHA + 注释 tag | Dependabot PR |
| 包管理器 action-setup（如 pnpm/action-setup） | pin commit SHA + 注释 tag | Dependabot PR |
| `actions/setup-node` / `setup-python` 等 | pin commit SHA + 注释 tag | Dependabot PR |
| `github/codeql-action/*` | pin commit SHA | 一等更新 |

### 3. 工具栈边界（最小必要，勿无脑叠加）

> 定型扫描工具时覆盖明确、足够即可，**不加多余第 N 个**除非风险缺口被证明。

| 工具 | 覆盖 |
|---|---|
| zizmor | workflow 配置安全 |
| Semgrep | 代码静态分析（通用+安全） |
| CodeQL | JS/TS 深度分析（需 GHAS 许可，无许可 403，仅作受控增强层预留） |

### 4. 免费档许可边界（勿重复评估）

- 私有免费仓库**无 rulesets（403），无 branch protection**（需 Pro/公共）。
- 因此"PR 必需检查强制合并"不可用；**CI 红 = run 失败**已是免费档的机器强制上限。
- CodeQL/Code Scanning 需 GHAS 许可，仅作受控增强层预留。

### 5. 维护规则

- 新增 workflow：复制本模板基线，满足 1/2/3，**必跑 `zizmor .github/workflows/` 过关**才合并。
- 升级 action：更新 SHA 对照表 + 云端双绿。
- 本节与项目 `AGENTS.md` 同源，改一处时同步另一处。

---

## 八、上线前环境变量核对法（web 项目通用）

> 主体可见 `checklists/上线前后检查.md`。此处沉淀跨项目可复用的核对方法（实测沉淀）：

1. **每个环境变量必须有明确的代码读取点**：上线前逐项 `grep` 真实读取处核实，缺配后果写明（如"SITE_URL 缺失回退 localhost → sitemap/robots/metadata 全污染收录"）。
2. `NEXT_PUBLIC_` 前缀变量在 Next.js 是**构建时内联**、非运行时读取——若平台只在运行时注入 env，凡构建期求值的静态文件（sitemap/robots/JSON-LD）会拿空回退默认值。修法：用规范化函数（缺协议头补 `https`、去尾斜杠）拼出 URL + 放进函数体（非模块顶层常量）+ 加 `force-dynamic`。
3. **构建注入的变量必须在 CI 构建步骤也带上**，否则线上镜像用的是回退值。
4. 管理员/敏感身份**只从服务端 env 判定**，前端传入的任何管理标志一律忽略，防越权。
5. 平台保留注入项（如 `COZE_` 前缀变量）**不要手动新建同名变量**，可能被系统保留或被禁止。