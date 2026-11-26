# 00_INDEX.md · AI 资料包全量索引

> STATUS 说明：`ACTIVE` = 现行依据 ｜ `EVIDENCE` = 原始依据（只读查证）｜ `DERIVED` = 由 ACTIVE 派生的导航/摘要 ｜ `DEPRECATED` = 历史，仅供追溯，**禁止作为现行需求**。
> 所有相对路径以仓库根目录为基准。最后整理：2026-11-25。

## 入口层（仓库根）

| 文件 | STATUS | 用途 | 何时读 |
|---|---|---|---|
| `llms.txt` | DERIVED | 标准 AI 入口：文件地图 + 阅读顺序 + 废弃清单 | 任何 AI 首次接入，**第一份** |
| `AGENTS.md` | DERIVED | 硬约定：真相源、禁写死规则、编号体系、安全红线 | 写代码 / 改 PRD 前必读 |
| `README.md` | DERIVED | 项目总览（人 + AI 双读） | 快速了解项目 |
| `AI_CONTEXT.md` | DERIVED | 单文件自包含版 | 上下文受限、只能读一个文件时 |
| `PRD_物业小程序一期_V0.3_2026-11-24.md` | ACTIVE | PRD V0.3.4 人工面板镜像（与 `02_PRD.md` 字节一致） | 人在面板里审文档 |

## 核心层（`ai-context/`）

| 文件 | STATUS | 用途 | 何时读 |
|---|---|---|---|
| `01_SUMMARY.md` | DERIVED | 约 10 KB 浓缩版：范围、模型、决策、约束、待确认 | **先读这个**，再按任务深入 |
| `02_PRD.md` | **ACTIVE · 唯一真相源** | PRD V0.3.4 全文（修订 1 一致性勘误），14 章 + 附录 A~J、FR-01~93 | 需要章节细节、字段、状态机、验收口径时 |
| `03_DECISIONS.md` | DERIVED | 11 条已裁决 + 6 条仍存冲突 + 用户 U-D 决策 9 条 | 判断「某结论是否已拍板」 |
| `04_OPEN_QUESTIONS.md` | DERIVED | 全部待确认项与硬规则 | 编码前确认哪些值不能写死 |
| `05_GLOSSARY.md` | DERIVED | 编号体系 + 术语消歧 + 角色 + 枚举 | 遇到 `L-/AC-/FR-` 等编号或术语歧义 |
| `06_CHANGELOG.md` | DERIVED | V0.2 → V0.3.4 版本链、在线/本地版本差 | 追溯某结论是哪一版引入的 |
| `07_EVIDENCE_MAP.md` | DERIVED | 依据台账导览：每条结论去哪查证 | 需要「有依据来源」的证明链 |

## 结构化数据（`ai-context/data/`）

| 文件 | STATUS | 内容 | 程序消费方式 |
|---|---|---|---|
| `requirements.json` | EVIDENCE | `items` 31 条待调研项、`standards` 16 行消防标准、`answered` 18 条已答 | JSON.parse，按 `id` / `item` 索引 |
| `fr_index.json` | DERIVED | FR-01~93 逐条索引（含原始表格行 `raw`） | 按 `id` 查功能需求，回 `02_PRD.md §5` 看全文 |
| `open_questions.json` | DERIVED | `U1`~`U13`，含 `question` / `impact` / `default_value` / `status=OPEN` | **编码前过滤 OPEN 项**，禁止写死 |
| `versions.json` | DERIVED | `active_version` + 7 个版本节点与在线文档 ID | 判断当前应引用哪一版 |

## 依据台账（`ai-context/evidence/`）

| 文件 | STATUS | 来源 | 用途 |
|---|---|---|---|
| `01_待调研清单_v37.md` | EVIDENCE | 资料库《待调研清单》v37 全量提取 | 所有 `L-` 条目原文 |
| `02_会议纪要依据.md` | EVIDENCE | 8 份纪要，26 条 `MM-` 交叉印证 + 63 条 `MI-` 依据 | 会议结论与冲突查证 |
| `03_规范文档依据.md` | EVIDENCE | 14 份 xlsx/docx/doc 解析 + 字段启示 | 表单字段、排班、考核口径 |
| `04_既有需求基线.md` | EVIDENCE | V0.1 章节反推、设计盲区摘录、项目约束 | `BP-` 基线出处 |
| `05_遗漏分析.md` | EVIDENCE | 38 条 `AG-` 遗漏、12 条 `AC-` 矛盾、24 条未闭环 | 遗漏审计逐条论证 |
| `06_标准规范对照表.md` | EVIDENCE | 一手消防原件 + GB 国标逐行对照（v2） | 16 行标准、双阈值、N-1~N-8 |
| `07_P0建模.md` | EVIDENCE | 状态机 / 数值判定 / 16 动作 RACI 完整建模 | §4 三块 P0 的推导过程 |
| `08_backlog模块标准流程.md` | EVIDENCE | 物品放行 / 日常任务 / 会议预约 / 投诉建议 4 流程 | backlog 模块细节 |
| `09_巡查分类与大型设施台账.md` | EVIDENCE | `U-D7` 二维模型 + `S-17` 三份设备清单实读 | `patrol_type`、消防四子域、G1~G9 |
| `10_应急预案及处置流程.md` | EVIDENCE | `应急预案及处置流程_重做版_v1.docx` 纯文本转写 | 第五节（高空坠物）补齐内容 |
| `11_交付说明_V0.2_历史.md` | **DEPRECATED** | V0.2 交付说明 | **仅供追溯版本史，不作现行结论** |

## 禁止引用

- `_archive/`（本地归档，不入库）：10 月采购立项旧资料、V0.2 回填稿、PRD 草稿、在线导出与读回快照。
- `ai-context/evidence/11_交付说明_V0.2_历史.md`：状态 DEPRECATED。
- 在线资料库 `sTPpmvwNkeCZCxpWNtBoI9`（V0.3.3）：落后于本仓库，冲突时以 `02_PRD.md` 为准。
- `.workbuddy/memory/`、`_ref/`：前者含凭据记录，后者是第三方源码，均不入库也不可引用。
