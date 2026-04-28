---
name: vn-sql-loan-domain-
description: 越南信贷借据域。仅提供借据全链路表结构、字段语义与域内关联，不承载跨域场景路由。
---

# 借据域（V2 子 Skill）

跨域关联统一见主 Skill：`..\\..\\SKILL.md` 的“跨场景关联目录”。

## 本域表结构

### `t_loan_application`

- 主键：`id`
- 业务键：`loan_apply_no`
- 常用字段：`product_code`、`loan_amount`、`loan_term`、`annual_rate`、`repayment_method`、`apply_time`、`status`、`risk_data`、`risk_check_result`、`reject_reason`、`created_at`、`updated_at`、`deleted`、`strategy_code`、`loan_purpose`

### `t_loan_contract`

- 主键：`id`
- 业务键：`contract_no`
- 关键关联键：`loan_apply_no`、`borrower_no`
- 常用字段：`contract_content`、`contract_template`、`contract_vars`、`sign_time`、`status`、`created_at`、`updated_at`、`deleted`

### `t_loan_account`

- 主键：`id`
- 业务键：`loan_no`
- 关键关联键：`contract_no`、`borrower_no`、`credit_no`
- 常用字段：`product_code`、`loan_amount`、`outstanding_principal`、`outstanding_interest`、`loan_term`、`annual_rate`、`repayment_method`、`disbursement_date`、`first_repayment_date`、`final_repayment_date`、`status`、`overdue_days`、`created_at`、`updated_at`、`deleted`

### `t_loan_product_snapshot`

- 主键：`id`
- 关键关联键：`loan_no`、`product_code`、`product_param_version`
- 常用字段：`full_config`、`created_at`、`updated_at`、`deleted`

### `t_disbursement`

- 主键：`id`
- 业务键：`disbursement_no`
- 关键关联键：`loan_no`、`borrower_no`、`contract_no`、`loan_apply_no`
- 常用字段：`disbursement_amount`、`payment_channel`、`pay_state`、`status`、`disbursement_time`、`created_at`、`updated_at`、`deleted`、`product_code`

### `t_disbursement_fee_record`

- 主键：`id`
- 业务键：`fee_record_no`
- 关键关联键：`disbursement_no`、`loan_no`
- 常用字段：`fee_name`、`fee_type`、`fee_value`、`calculated_amount`、`charge_moment`、`charge_time`、`created_at`、`updated_at`、`deleted`

### `t_repayment_plan`

- 主键：`id`
- 逻辑键：`loan_no + period_no`
- 常用字段：`plan_principal`、`plan_interest`、`plan_amount`、`plan_date`、`repaid_amount`、`overdue_days`、`overdue_penalty`、`status`、`overdue_status`、`overdue_level`、`actual_repay_date`、`created_at`、`updated_at`、`deleted`

### `t_repayment_record`

- 主键：`id`
- 业务键：`repayment_no`
- 关键关联键：`loan_no`、`borrower_no`
- 常用字段：`repayment_type`、`repayment_amount`、`principal_amount`、`interest_amount`、`penalty_amount`、`compound_amount`、`fee_amount`、`payment_channel`、`payment_order_no`、`repayment_time`、`status`、`created_at`、`updated_at`、`deleted`

### `t_interest_accrual`

- 主键：`id`
- 逻辑键：`loan_no + business_date`
- 常用字段：`accrual_type`、`is_overdue`、`accrued_interest`、`penalty_accrued`、`compound_accrued`、`overdue_days`、`total_outstanding`、`created_at`、`updated_at`、`deleted`

### `t_pay_record`

- 主键：`id`
- 业务键：`order_no`、`pay_serial_no`
- 常用字段：`order_type`、`account_type`、`account_no`、`user_no`、`pay_amount`、`pay_channel`、`bank_code`、`bank_name`、`state`、`created_time`、`updated_time`、`currency`

## 本域各表含义

- `t_loan_application`：借款申请主表，记录用户借款意图、申请参数与贷前风控结果。
- `t_loan_contract`：借款合同表，保存签约状态、合同模板内容与合同变量。
- `t_loan_account`：借据/贷款账户核心表，反映放款后余额、状态、期限与逾期表现。
- `t_loan_product_snapshot`：放款时产品参数快照，保证历史借据按当时配置回溯。
- `t_disbursement`：放款流水表，记录放款金额、通道、状态与放款时间。
- `t_disbursement_fee_record`：放款相关费用明细，记录费用类型、费值与实收金额。
- `t_repayment_plan`：还款计划表，按期记录应还、已还、逾期与账龄信息。
- `t_repayment_record`：实还流水表，记录每笔还款入账及本息罚等拆分。
- `t_interest_accrual`：计提流水表，记录按日计息/罚息/复利及应收余额变化。
- `t_pay_record`：支付通道订单表，记录渠道支付请求、状态与外部流水号。

## 本域字段语义

- `t_loan_application.status`：`PENDING`，`APPROVED`，`REJECTED`，`CONTRACTED`，`DISBURSED`，`CANCELLED`
- `t_loan_contract.status`：`DRAFT`，`SIGNED`，`CANCELLED`
- `t_loan_account.status`：`PENDING_DISBURSEMENT`，`NORMAL`，`OVERDUE`，`SETTLED`，`CANCELLED`，`CHARGED_OFF`
- `t_disbursement.status`：`PENDING`，`SUCCESS`，`FAILED`
- `t_repayment_plan.status`：`UNPAID`，`PARTIAL_PAID`，`PAID`
- `t_repayment_plan.overdue_status`：`NORMAL`，`OVERDUE`
- `t_repayment_record.status`：`SUCCESS`，`FAILED`
- `t_interest_accrual.accrual_type`：`NORMAL`，`OVERDUE`
- `t_interest_accrual.is_overdue`：`1` 逾期计提，`0` 非逾期计提

## JSON / 半结构化字段（本域）

- `t_loan_application.risk_data`
- `t_loan_application.risk_check_result`
- `t_loan_contract.contract_vars`
- `t_loan_product_snapshot.full_config`

## 本域关联逻辑

- `t_loan_application.loan_apply_no = t_loan_contract.loan_apply_no`
- `t_loan_account.loan_no = t_repayment_plan.loan_no`
- `t_loan_account.loan_no = t_repayment_record.loan_no`
- `t_loan_account.loan_no = t_interest_accrual.loan_no`
- `t_loan_account.loan_no = t_disbursement.loan_no`
- `t_disbursement.disbursement_no = t_disbursement_fee_record.disbursement_no`
- `t_loan_account.loan_no = t_loan_product_snapshot.loan_no`
- `t_loan_account.product_code = t_loan_product_snapshot.product_code`