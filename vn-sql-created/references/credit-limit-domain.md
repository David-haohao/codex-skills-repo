---
name: vn-sql-credit-limit-domain
description: 越南信贷额度域。仅提供额度与额度调整表结构、字段语义与域内关联，不承载跨域路由规则。
---

# 额度域（V2 子 Skill）

跨域关联统一见主 Skill：`..\\..\\SKILL.md` 的“跨场景关联目录”。

## 本域表结构

### `t_credit_limit`

- 主键：`id`
- 业务键：`credit_no`
- 关键关联键：`borrower_no`、`application_no`
- 常用字段：`product_code`、`total_limit`、`available_limit`、`used_limit`、`frozen_limit`、`status`、`effective_date`、`expire_date`、`created_at`、`updated_at`、`deleted`、`version`、`limit_type`、`risk_level`、`annual_rate`

### `t_credit_adjustment`

- 主键：`id`
- 业务键：`credit_no`
- 常用字段：`adjustment_type`、`before_limit`、`after_limit`、`adjustment_amount`、`reason`、`operator`、`created_at`、`updated_at`、`deleted`

## 本域各表含义

- `t_credit_limit`：额度主表，记录授信额度总额、可用额、已用额、冻结额与有效期状态。
- `t_credit_adjustment`：额度调整流水表，记录提额/降额/冻结/释放等额度变更事件。

## 本域字段语义

### `t_credit_limit`

- `status`：`NORMAL` 正常，`FROZEN` 冻结，`EXPIRED` 过期
- `limit_type`：`REVOLVING` 循环额度，`ONE_TIME` 一次性额度

### `t_credit_adjustment`

- `adjustment_type`：`INCREASE`，`DECREASE`，`FREEZE`，`UNFREEZE`，`OCCUPY`，`OCCUPY_CONFIRM`，`RELEASE`

## 本域关联逻辑

- `t_credit_adjustment.credit_no = t_credit_limit.credit_no`