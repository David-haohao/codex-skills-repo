---
name: vn-sql-user-domain
description: 越南信贷用户域相关内容。仅提供用户域表结构、字段语义与域内关联，不承载跨域路由与跨场景 join 规范。
---

# 用户域（V2 子 Skill）

跨域关联统一见主 Skill：`..\\..\\SKILL.md` 的“跨场景关联目录”。

## 本域表结构

### `t_borrower`

- 主键：`id`
- 业务键：`borrower_no`
- 常用字段：`name`、`mobile`、`email`、`status`、`channel_code`、`created_at`、`updated_at`、`deleted`、`kyc_status`

### `t_borrower_account`

- 主键：`id`
- 业务键：`borrower_no`
- 常用字段：`account_type`、`account_number`、`bind_phone`、`status`、`is_default`、`created_at`、`updated_at`、`deleted`

### `t_borrower_profile`

- 主键：`id`
- 业务键：`borrower_no`
- 常用字段：`gender`、`birthday`、`marital_status`、`education`、`occupation`、`company_name`、`min_monthly_income`、`max_monthly_income`、`credit_cards_count`、`has_house`、`has_car`、`credit_score`、`risk_level`、`tags`、`address`、`id_card_front`、`id_card_back`、`liveness_pic`、`liveness_score`、`ocr_status`、`liveness_status`、`children_count`、`division_code`、`detail_address`、`industry`、`position`、`payday`、`salary_method`、`min_job_months`、`max_job_months`、`max_residence_years`、`min_residence_years`、`created_at`、`updated_at`、`deleted`

### `t_borrower_relationship`

- 主键：`id`
- 业务键：`borrower_no`
- 常用字段：`relationship_type`、`contract_name`、`contract_phone`、`deleted`、`created_at`、`updated_at`

### `t_detection_record`

- 主键：`id`
- 业务键：`borrower_no`
- 常用字段：`detection_type`、`status`、`result`、`risk_flag`、`created_at`、`updated_at`、`deleted`

### `t_trace_record`

- 主键：`id`
- 业务键：`borrower_no`
- 常用字段：`event_type`、`event_name`、`path`、`cost_time`、`ext_params`、`created_at`、`device_id`、`ip_addr`

## 本域各表含义

- `t_borrower`：用户主档，记录用户唯一标识与账户生命周期状态。
- `t_borrower_account`：用户收付账户信息，包含钱包/银行卡及默认账户标识。
- `t_borrower_profile`：用户画像与基础资质信息，覆盖人口属性、工作、居住与认证结果。
- `t_borrower_relationship`：用户联系人信息，用于联系人维度分析与核验链路。
- `t_detection_record`：OCR/活体等认证检测流水，记录检测类型、状态与结果。
- `t_trace_record`：App/流程行为埋点日志，用于行为路径与事件分析。

## 本域字段语义

### `t_borrower`

- `status`：`NORMAL` 正常，`FROZEN` 冻结，`BLACKLIST` 黑名单
- `kyc_status`：`0` 完成注册（验证码登录）`1` 基础信息 `2` 工作信息 `3` 联系人 `4` 身份证 `5` 活体 `6` 绑卡(完件). 完件进度依次递增

### `t_borrower_account`

- `account_type`：`wallet` 钱包，`bankcard` 银行卡
- `is_default`：`1` 默认账户，`0` 非默认

### `t_borrower_profile`

- `has_house`：`1` 有房，`0` 无房
- `has_car`：`1` 有车，`0` 无车
- `ocr_status`：`1` 成功，`-1` 失败
- `liveness_status`：`1` 成功，`-1` 失败

### `t_detection_record`

- `detection_type`：`ocr`，`liveness`
- `status`：`init`，`success`，`fail`
- `result`：`1` pass，`0` nopass

## 本域关联逻辑

- `t_borrower.borrower_no = t_borrower_account.borrower_no`
- `t_borrower.borrower_no = t_borrower_profile.borrower_no`
- `t_borrower.borrower_no = t_borrower_relationship.borrower_no`
- `t_borrower.borrower_no = t_detection_record.borrower_no`
- `t_borrower.borrower_no = t_trace_record.borrower_no`