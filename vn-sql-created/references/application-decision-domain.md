---
name: vn-sql-application-decision-domain
description: 越南信贷申请与决策域。仅提供申请/审批/决策/贷前特征表结构与域内关联，不承载跨域路由规则。
---

# 申请与决策域（V2 子 Skill）

跨域关联统一见主 Skill：`..\\..\\SKILL.md` 的“跨场景关联目录”。

## 本域表结构

### `t_credit_application`

- 主键：`id`
- 业务键：`application_no`
- 关键关联键：`borrower_no`、`decision_request_id`
- 常用字段：`product_code`、`apply_amount`、`apply_term`、`risk_data`、`risk_score`、`risk_level`、`status`、`reject_reason`、`approval_time`、`approver`、`created_at`、`updated_at`、`decision_status`、`suggested_limit`、`suggested_rate`、`need_manual_review`、`manual_review_reason`、`suggested_validity_period`、`strategy_code`

### `t_credit_approval`

- 主键：`id`
- 业务键：`application_no`
- 常用字段：`approval_node`、`approver`、`approval_result`、`approval_opinion`、`approval_time`、`created_at`、`updated_at`、`deleted`

### `t_decision_result`

- 主键：`id`
- 业务键：`application_no`
- 关键关联键：`request_id`
- 常用字段：`decision_type`、`status`、`risk_score`、`risk_level`、`decision`、`suggested_limit`、`suggested_rate`、`reject_reason`、`result_data`、`callback_time`、`created_at`、`updated_at`、`deleted`、`suggested_validity_period`

### `yn_apply_feature_table`

- 业务键：`application_no`、`borrower_no`、`product_code`
- 常用字段：`created_at`、`decision_request_id`、`strategy_code`、`decision_status`、`biz_action_type`、`risk_data`、`Adm`、`reject_code`、`dt`

## 本域各表含义

- `t_credit_application`：授信申请主表，承载申请输入、流程状态、决策请求与审批结果摘要。
- `t_credit_approval`：人工/节点审批流水，记录审批节点、审批人、审批结论与意见。
- `t_decision_result`：决策引擎回传结果，记录决策类型、状态、风险等级与建议额度利率。
- `yn_apply_feature_table`：贷前特征快照表，沉淀策略入参、规则结果与 `risk_data` JSON 特征。

## 本域字段语义

### `t_credit_application`

- `status`：`PENDING`，`APPROVED`，`REJECTED`，`CANCELLED`
- `decision_status`：`PENDING`，`SUCCESS`，`FAILED`，`TIMEOUT`
- `need_manual_review`：`1` 需要人工复审，`0` 不需要

### `t_credit_approval`

- `approval_result`：`PASS` 通过，`REJECT` 拒绝

### `t_decision_result`

- `decision_type`：`CREDIT` 授信，`LOAN` 贷款
- `decision`：`APPROVED`，`REJECTED`，`MANUAL_REVIEW`
- `status`：`PENDING`，`SUCCESS`，`FAILED`，`TIMEOUT`

### `yn_apply_feature_table`

- `Adm`：`1` 通过，`0` 拒绝
- `biz_action_type`：`01/02/03/04/05` 对应授信与提额动作类型
- `reject_code`：命中规则编码集合
- `risk_data`：贷前特征主存储字段（JSON）

## JSON / 半结构化字段（本域）

- `t_credit_application.risk_data`
- `t_credit_application.manual_review_reason`（自由文本，默认不按 JSON 解析）
- `t_decision_result.result_data`
- `yn_apply_feature_table.risk_data`

## 本域关联逻辑

- `t_credit_application.application_no = t_credit_approval.application_no`
- `t_credit_application.decision_request_id = t_decision_result.request_id`
- `t_credit_application.application_no = yn_apply_feature_table.application_no`
- `t_credit_application.borrower_no = yn_apply_feature_table.borrower_no`
- `t_credit_application.product_code = yn_apply_feature_table.product_code`