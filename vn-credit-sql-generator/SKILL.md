---
name: vn-sql-generator
description: 根据越南信贷常用表结构和明确业务口径生成 MySQL 日常分析 SQL。只在用户明确给出指标、粒度、时间字段和过滤条件后输出 SQL；缺信息时必须追问，不自动猜测。
---

# 越南信贷日常 SQL 生成器

## 目标

用于越南信贷项目的日常分析 SQL 生成。该 skill 的职责只有一个：基于已确认的表结构和已明确的分析口径，输出可执行的 MySQL SQL。

默认行为是“先确认，再生成”。如果需求里缺少分析对象、主事实表、时间字段、粒度、去重口径、过滤条件或指标定义，必须先追问，不允许自行补全。

## 强制规则

- 只生成 `MySQL` SQL。
- 默认只输出 SQL，不输出解释性文字。
- 不自动猜测分析粒度。
- 不自动猜测时间字段。
- 不自动猜测去重 key。
- 不自动猜测过滤条件。
- 不自动把 `deleted=1` 排除条件当作默认口径，是否排除必须由需求确认。
- 金额字段默认保留原始单位，当前表结构里大量金额以“分”为单位存储；如需转元，必须由用户明确说明。
- 只使用当前已确认的表结构和字段，不虚构字段名，不臆造关联键。
- 尽量用单条 SQL 完成；如果必须拆分，优先使用 CTE，仍然只输出 SQL。

## 字段值口径与枚举说明

这一节收纳最容易影响 SQL 口径判断的字段取值含义。凡是引用这些字段做过滤、分组、去重或统计时，必须先按这里的语义理解，不要只看数字值。

### 1. 用户与画像

- `t_borrower.status`
  - `NORMAL`：正常
  - `FROZEN`：冻结
  - `BLACKLIST`：黑名单

- `t_borrower.kyc_status`
  - `0`：完成注册 / 验证码登录
  - `1`：基础信息
  - `2`：工作信息
  - `3`：联系人
  - `4`：身份证
  - `5`：活体
  - `6`：绑卡 / 完件
  - 说明：状态值按完件进度递增，数值越大代表完成度越高

- `t_borrower_account.account_type`
  - `wallet`：钱包
  - `bankcard`：银行卡

- `t_borrower_account.status`
  - `ACTIVE`：有效

- `t_borrower_account.is_default`
  - `1`：默认账户
  - `0`：非默认账户

- `t_borrower.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_borrower_profile.has_house`
  - `1`：有房
  - `0`：无房

- `t_borrower_profile.has_car`
  - `1`：有车
  - `0`：无车

- `t_borrower_profile.ocr_status`
  - `1`：成功
  - `-1`：失败

- `t_borrower_profile.liveness_status`
  - `1`：认证成功
  - `-1`：认证失败

- `t_detection_record.detection_type`
  - `ocr`：OCR 认证
  - `liveness`：活体认证

- `t_detection_record.status`
  - `init`：初始化
  - `success`：成功
  - `fail`：失败

- `t_detection_record.result`
  - `1`：pass
  - `0`：nopass

- `t_detection_record.deleted`
  - `0`：未删除
  - `1`：已删除

### 2. 授信申请与决策

- `t_credit_application.status`
  - `PENDING`：待审批
  - `APPROVED`：已批准
  - `REJECTED`：已拒绝
  - `CANCELLED`：已取消

- `t_credit_application.decision_status`
  - `PENDING`：待处理
  - `SUCCESS`：成功
  - `FAILED`：失败
  - `TIMEOUT`：超时

- `t_credit_application.need_manual_review`
  - `1`：需要人工复审
  - `0`：不需要人工复审

- `t_credit_approval.approval_result`
  - `PASS`：通过
  - `REJECT`：拒绝

- `t_decision_result.decision_type`
  - `CREDIT`：授信
  - `LOAN`：贷款

- `t_decision_result.status`
  - `PENDING`：待处理
  - `SUCCESS`：成功
  - `FAILED`：失败
  - `TIMEOUT`：超时

- `t_decision_result.decision`
  - `APPROVED`：批准
  - `REJECTED`：拒绝
  - `MANUAL_REVIEW`：人工复审

- `yn_apply_feature_table.Adm`
  - `1`：通过
  - `0`：拒绝
  - 说明：本 skill 采用用户确认口径，后续按此含义解释拒绝/通过结果；如历史表存在其他编码，仍以该口径为准

- `yn_apply_feature_table.biz_action_type`
  - `01`：首次授信【P1 产品授信】
  - `02`：P1 产品提额 - L2 场景
  - `03`：P1 产品提额 - L3 / L3+ 场景
  - `04`：产品为开 API 申请
  - `05`：除 P1 产品提额

- `yn_apply_feature_table.decision_status`
  - 语义同决策是否成功运行，具体值以当前数据口径为准；生成 SQL 前若要按值过滤，必须先确认取值全集

- `yn_apply_feature_table.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_credit_application.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_credit_approval.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_decision_result.deleted`
  - `0`：未删除
  - `1`：已删除

### 3. 授信额度

- `t_credit_limit.status`
  - `NORMAL`：正常
  - `FROZEN`：冻结
  - `EXPIRED`：已过期

- `t_credit_limit.limit_type`
  - `REVOLVING`：循环额度
  - `ONE_TIME`：一次性额度

- `t_credit_limit.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_credit_adjustment.adjustment_type`
  - `INCREASE`：提额
  - `DECREASE`：降额
  - `FREEZE`：冻结
  - `UNFREEZE`：解冻
  - `OCCUPY`：占用
  - `OCCUPY_CONFIRM`：占用确认
  - `RELEASE`：释放

- `t_credit_adjustment.deleted`
  - `0`：未删除
  - `1`：已删除

### 4. 贷款、放款与还款

- `t_loan_application.status`
  - `PENDING`：待审批
  - `APPROVED`：已批准
  - `REJECTED`：已拒绝
  - `CONTRACTED`：已签约
  - `DISBURSED`：已放款
  - `CANCELLED`：已取消

- `t_loan_contract.status`
  - `DRAFT`：草稿
  - `SIGNED`：已签约
  - `CANCELLED`：已取消

- `t_loan_account.status`
  - `PENDING_DISBURSEMENT`：待放款
  - `NORMAL`：正常
  - `OVERDUE`：逾期
  - `SETTLED`：已结清
  - `CANCELLED`：已取消
  - `CHARGED_OFF`：已核销

- `t_loan_account.product_type`
  - `CONSUMER`：消费贷
  - `REVOLVING`：循环贷

- `t_loan_account.interest_accrual_mode`
  - `INCLUDE_START_EXCLUDE_END`：算头不算尾
  - `EXCLUDE_START_INCLUDE_END`：算尾不算头
  - `INCLUDE_BOTH`：算头又算尾
  - `EXCLUDE_BOTH`：不算头不算尾

- `t_loan_account.initial_penalty_type`
  - `FIXED`：固定金额
  - `PERCENT`：比例

- `t_loan_account.penalty_base_type`
  - `REMAINING_PRINCIPAL`：剩余本金
  - `REMAINING_TOTAL_AMOUNT`：剩余应还总额

- `t_loan_account.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_disbursement.status`
  - `PENDING`：待放款
  - `SUCCESS`：成功
  - `FAILED`：失败

- `t_disbursement.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_disbursement_fee_record.fee_type`
  - `FIXED`：固定金额
  - `PERCENT`：百分比

- `t_repayment_plan.status`
  - `UNPAID`：未还款
  - `PARTIAL_PAID`：部分还款
  - `PAID`：已还款

- `t_repayment_plan.overdue_status`
  - `NORMAL`：正常
  - `OVERDUE`：逾期

- `t_repayment_plan.overdue_level`
  - `NORMAL`：正常
  - `M0`：30 天内
  - `M1`：31-60 天
  - `M2`：61-90 天
  - `M3`：91-120 天
  - `M4`：121-150 天
  - `M5`：151-180 天
  - `M6+`：180 天以上

- `t_repayment_plan.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_repayment_record.repayment_type`
  - `NORMAL`：正常还款
  - `PREPAYMENT`：提前还款
  - `PARTIAL`：部分还款

- `t_repayment_record.status`
  - `SUCCESS`：成功
  - `FAILED`：失败

- `t_repayment_record.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_interest_accrual.accrual_type`
  - `NORMAL`：正常
  - `OVERDUE`：逾期

- `t_interest_accrual.is_overdue`
  - `1`：逾期状态下计提
  - `0`：非逾期状态下计提

- `t_interest_accrual.deleted`
  - `0`：未删除
  - `1`：已删除

- `t_pay_record.account_type`
  - `wallet`：钱包
  - `bank`：银行卡

- `t_pay_record.deleted`
  - 该表未在当前工作簿中给出 `deleted` 字段，不默认假设存在

## 表结构总览

以下表结构来自当前越南信贷常用表结构梳理文件。skill 只把它们当作分析依据，不假设任何未明确写出的关联。

### 1. 用户域

- `t_borrower`：借款人基础信息表，主键 `id`，核心键 `borrower_no`
- `t_borrower_account`：借款人账户信息表，核心键 `borrower_no`
- `t_borrower_profile`：借款人画像表，核心键 `borrower_no`
- `t_borrower_relationship`：借款人联系人表，核心键 `borrower_no`
- `t_detection_record`：OCR / 活体检测记录，核心键 `borrower_no`
- `t_trace_record`：信息采集 / 埋点记录，核心键 `borrower_no`

### 2. 申请与决策域

- `t_credit_application`：授信申请表，核心键 `application_no`，关联键 `borrower_no`
- `t_credit_approval`：授信审批记录表，核心键 `application_no`
- `t_decision_result`：决策引擎结果表，核心键 `application_no`，关联键 `request_id`
- `yn_apply_feature_table`：贷前特征宽表，核心键 `application_no`、`borrower_no`、`product_code`
- `t_credit_limit`：授信额度表，核心键 `credit_no`，关联键 `borrower_no`
- `t_credit_adjustment`：授信额度调整记录表，核心键 `credit_no`

### 3. 贷款、放款与还款域

- `t_loan_application`：贷款申请表，核心键 `loan_apply_no`
- `t_loan_contract`：贷款合同表，核心键 `contract_no`
- `t_loan_account`：贷款账户 / 借据表，核心键 `loan_no`
- `t_loan_product_snapshot`：贷款产品快照表
- `t_disbursement`：放款记录表，核心键 `disbursement_no`
- `t_disbursement_fee_record`：放款手续费记录表，核心键 `fee_record_no`
- `t_repayment_plan`：还款计划表
- `t_repayment_record`：实际还款流水表，核心键 `repayment_no`
- `t_interest_accrual`：利息计提记录表
- `t_pay_record`：支付记录表
- `t_atom_data`：原子表（当前仅有表名，字段待补充）

## JSON / 半结构化字段清单

这一节专门收纳可能需要按 JSON 解析、或者虽然是 `text` / `longtext` 但实际承载结构化内容的字段。生成 SQL 时，如果用户要求读取内部字段，必须先确认键名和语义，再展开。

### 1. 贷前特征与风控结果

- `yn_apply_feature_table.risk_data`
- `t_credit_application.risk_data`
- `t_decision_result.result_data`
- `t_loan_application.risk_data`
- `t_loan_application.risk_check_result`

### 2. 画像与标签

- `t_borrower_profile.tags`

### 3. 合同、埋点与快照

- `t_loan_contract.contract_content`
- `t_loan_contract.contract_vars`
- `t_trace_record.ext_params`
- `t_detection_record.response_data`
- `t_loan_product_snapshot.full_config`

### 4. 解析原则

- 只要字段被归入这一节，后续生成 SQL 时就默认它可能需要 JSON / 半结构化解析。
- 如果结构已经明确，可以直接给出简要字段说明。
- 如果结构尚不明确，只能写“结构待补充”，不能臆造键名。
- 如果用户要求统计 JSON 内部字段，优先使用 `JSON_EXTRACT`、`JSON_UNQUOTE`、`JSON_VALID` 等函数；如果源字段不是标准 JSON，则先追问格式，不要直接展开。

## 关键关联链路

### 1. 借款人链路

- `borrower_no` 是用户域最核心的连接键。
- 常见关联：`t_borrower`、`t_borrower_account`、`t_borrower_profile`、`t_borrower_relationship`、`t_detection_record`、`t_trace_record`、`t_credit_application`、`t_credit_limit`、`t_loan_application`、`t_loan_contract`、`t_loan_account`、`t_disbursement`、`t_repayment_record`。

### 2. 申请链路

- `t_credit_application.application_no = t_credit_approval.application_no`
- `t_credit_application.decision_request_id = t_decision_result.request_id`
- `t_credit_application.application_no = yn_apply_feature_table.application_no`
- `t_credit_application.borrower_no = yn_apply_feature_table.borrower_no`
- `t_credit_application.product_code = yn_apply_feature_table.product_code`

### 3. 贷款链路

- `t_loan_application.loan_apply_no = t_loan_contract.loan_apply_no`
- `t_loan_application.borrower_no = t_loan_contract.borrower_no`
- `t_loan_application.credit_no = t_loan_account.credit_no`
- `t_loan_account.loan_no = t_repayment_plan.loan_no`
- `t_loan_account.loan_no = t_repayment_record.loan_no`
- `t_loan_account.loan_no = t_interest_accrual.loan_no`
- `t_loan_account.loan_no = t_disbursement.loan_no`
- `t_disbursement.disbursement_no = t_disbursement_fee_record.disbursement_no`
- `t_loan_account.loan_no = t_loan_product_snapshot.loan_no`
- `t_loan_account.product_code = t_loan_product_snapshot.product_code`
- `t_loan_account.product_param_version = t_loan_product_snapshot.product_param_version`

### 4. 授信链路

- `t_credit_limit.credit_no` 是授信链路主键。
- `t_credit_adjustment.credit_no = t_credit_limit.credit_no`
- `t_loan_application.credit_no = t_credit_limit.credit_no`
- `t_loan_account.credit_no = t_credit_limit.credit_no`

## 时间字段口径

skill 不会自动选择时间字段，但会在追问时给出可选项。下面是当前表结构里最常见的时间字段语义：

- `t_borrower.created_at`：用户注册时间
- `t_borrower_profile.created_at`：画像记录创建时间
- `t_borrower_account.created_at`：账户创建时间
- `t_borrower_relationship.created_at`：联系人新增时间
- `t_detection_record.created_at`：检测请求时间
- `t_trace_record.created_at`：行为事件时间
- `t_credit_application.created_at`：申请时间
- `t_credit_application.approval_time`：授信审批时间
- `t_credit_approval.approval_time`：审批节点时间
- `t_decision_result.created_at` / `callback_time`：决策记录生成 / 回调时间
- `yn_apply_feature_table.created_at`：申请日
- `yn_apply_feature_table.dt`：日期分区字段
- `t_credit_limit.effective_date`：授信生效日期
- `t_credit_limit.expire_date`：授信到期日期
- `t_credit_adjustment.created_at`：额度调整时间
- `t_loan_application.apply_time`：贷款申请时间
- `t_loan_contract.sign_time`：签约时间
- `t_loan_account.created_at`：借据创建 / 支用时间
- `t_loan_account.disbursement_date`：放款日期
- `t_loan_account.settlement_date`：结清日期
- `t_disbursement.disbursement_time`：放款成功时间
- `t_disbursement.created_at`：放款记录创建时间
- `t_disbursement_fee_record.charge_time`：扣费时间
- `t_repayment_plan.plan_date`：计划还款日
- `t_repayment_plan.actual_repay_date`：实际还款日
- `t_repayment_record.repayment_time`：实际还款时间
- `t_interest_accrual.business_date`：计提业务日期

## SQL 生成流程

当用户要生成 SQL 时，严格按以下顺序处理：

1. 确认分析主题，例如申请、审批、决策、额度、放款、还款、画像、行为、检测。
2. 确认主事实表，不能自动替代。
3. 确认时间字段，不能自动替代。
4. 确认统计粒度，例如按天、按周、按月、按产品、按渠道、按用户、按申请、按借据。
5. 确认去重口径，例如 `COUNT(*)`、`COUNT(DISTINCT application_no)`、`COUNT(DISTINCT loan_no)`。
6. 确认过滤条件，例如产品、状态、渠道、日期范围、是否排除删除记录。
7. 确认指标定义，例如申请数、通过数、拒绝数、通过率、放款金额、还款金额、逾期率、平均金额。
8. 确认是否需要联表，以及联表后的行粒度是否会被放大。
9. 输出 MySQL SQL，仅输出 SQL。

如果任一步缺信息，必须先追问，不能“先按经验补齐再说”。

## FPDn+ 通用定义（默认口径，可配置字段）

当用户需求涉及 `FPD1+`、`FPD3+`、`FPD7+` 或任意 `FPDn+` 时，默认按以下通用口径生成：

- 观察点定义：`<首期应还日字段> + N 天`。
- 表现期判定（踢掉未到表现期）：`<观察日> >= DATE_ADD(<首期应还日字段>, INTERVAL N DAY)`。
- 逾期命中条件（默认）：在满足表现期判定后，再叠加“在逾”条件（如 `<结清标志字段> IS NULL` 或用户明确的状态口径）。
- `N` 必须由需求明确给出；未给出 `N` 时必须追问，不允许默认写死为 `1`。
- 除非用户明确要求其他观察日，默认观察日使用 `CURRENT_DATE()`。
- 若表结构字段命名发生变化，先做字段映射确认，再生成 SQL；不把 `first_repayment_date`、`settlement_date` 视为永久固定字段名。

标准判断骨架（仅口径模板）：

```sql
CASE
  WHEN <观察日> >= DATE_ADD(<首期应还日字段>, INTERVAL N DAY)
   AND <在逾条件>
  THEN 1 ELSE 0
END
```

## 必须追问的最小信息集

当需求不完整时，至少要问清楚下面这些内容：

- 分析对象是什么。
- 主事实表是哪一张。
- 统计粒度是什么。
- 时间字段用哪一个。
- 是否需要去重，去重 key 是什么。
- 是否需要联表，联哪些表。
- 指标的分子和分母分别是什么。
- 金额单位是分还是元。
- 是否排除 `deleted=1`。
- 是否限定 `status`、`decision_status`、`approval_result`、`pay_state`、`repayment status` 等业务状态。
- 如涉及 `FPDn+`：`N` 的取值是多少，观察日是否用 `CURRENT_DATE()` 还是指定业务日。

## 常用场景映射

以下映射只用于帮助识别业务方向，不代表默认口径。

- 申请通过率、审批时长、审批节点分析
  - 主要表：`t_credit_application`、`t_credit_approval`、`t_decision_result`

- 贷前策略命中、拒绝码、特征分布
  - 主要表：`yn_apply_feature_table`、`t_credit_application`、`t_decision_result`

- 授信额度、提额、冻结、释放
  - 主要表：`t_credit_limit`、`t_credit_adjustment`

- 贷款申请、签约、放款
  - 主要表：`t_loan_application`、`t_loan_contract`、`t_loan_account`、`t_disbursement`

- 计划还款、实际还款、逾期、罚息、复利
  - 主要表：`t_repayment_plan`、`t_repayment_record`、`t_interest_accrual`

- 用户画像、认证、联系人、行为采集
  - 主要表：`t_borrower`、`t_borrower_profile`、`t_borrower_account`、`t_borrower_relationship`、`t_detection_record`、`t_trace_record`

## 代码风格抽象（口径优先、最小充分）

生成 SQL 时，默认遵循以下风格：

- 先定口径，再写 SQL：优先确认分子、分母、去重 key、时间字段、时间窗。
- 结果可审计：率类指标默认同时输出分子与分母，不只输出比例。
- 默认保守统计：计数优先使用与业务对象一致的 `COUNT(DISTINCT ...)`，避免重复放大。
- 表现期严格处理：涉及 FPDn+ 时，未到表现期样本必须剔除。
- 简洁优先：无联表或无歧义时，不滥用表别名与字段前缀。
- 字段最小化：只选择计算必需字段，不做无关扩列。
- 结构轻量：能单层子查询解决就不堆叠 CTE；必要窗口函数可保留。
- 过滤显式：`deleted`、状态、时间边界必须明确写出，不依赖隐式默认。
- 命名语义化：建议使用 `denominator_*`、`numerator_*`、`*_rate` 命名统计字段。
- 安全除法：比例统一使用 `... / NULLIF(denominator, 0)`，避免除零错误。
- 通式优先：口径逻辑应抽象为可迁移通式，避免写死单一业务字段名。

## 输出规范

- 默认只给 SQL。
- SQL 里尽量使用清晰别名。
- 不要用 `SELECT *`。
- 不要在 SQL 里加入业务解释文字。
- 如需多段结果，优先使用 CTE 组织成一条 SQL。
- 金额、计数、比例字段要显式命名，避免歧义。
- 对于率类指标，必须在 SQL 中明确分子和分母。
- 对于金额类指标，必须明确原始单位和是否转换。

## 审查重点

在生成 SQL 前，优先检查以下风险：

- 关联是否会造成行数重复。
- 统计口径是否与用户描述一致。
- 时间字段是否真的是业务发生时间，而不是记录写入时间。
- 是否把计提、申请、审批、放款、还款混用了。
- 是否把金额单位错误地当成元。
- 是否把 `status` / `deleted` 当成默认过滤条件。

## 默认响应方式

当信息完整时：

- 直接输出 SQL。

当信息不完整时：

- 直接追问，不生成 SQL。
- 追问尽量一次性收敛到能执行 SQL 的最小必要信息。