# 单人复核标签变更记录

复核日期：2026-10-02

## 复核方法

本轮先依据 21 个大学官方课程页面修正并冻结 `programmes.csv`，再隐藏旧标签、旧评估结果和系统推荐，严格按 `suitability_rubric.md` 对 `test01` 至 `test30` 独立复核。30 份新答案全部完成并通过结构检查后，才打开旧 `ground_truth.jsonl` 进行比较。

固定规则是：先应用学习模式、已知学费及已知学制等硬约束，再对职业目标、兴趣和学术背景评分；总分至少 3 分且无硬约束冲突才纳入。`NUS_MSBA` 的官方学费按身份分层，而测试资料没有申请人身份，因此不把该项当作已知超预算。

## 总体变更

- 30/30 个测试用户的标签集合发生变化。
- 新增 153 个“适合”标签，主要原因是旧标签多为短名单，而评分标准要求列出所有达到门槛的项目。
- 删除 25 个旧标签，主要由官网学费更新后触发预算硬约束；少数项目因相关性得分不足 3 分而删除。
- 本轮没有根据评估结果回调权重或修改标签。

## 逐用户变更

表中“补全”均表示项目通过硬约束且固定适配分达到 3 分；另有说明的删除项目给出具体原因。

| 用户 | 新增项目 | 删除项目 | 修改原因 |
|---|---|---|---|
| test01 | NTU_ENTERPRISE_AI、NTU_FINTECH、NTU_MSIS、NUS_AII、NUS_MSBA、SMU_MDSE、SMU_MITB、SMU_MSCOMPUTING | 无 | 补全所有达到门槛的 AI、数据、金融科技及信息系统项目。 |
| test02 | NTU_ENTERPRISE_AI、NTU_MSDS、NTU_MSIS、NUS_AII、NUS_DSML、NUS_SIDT、SMU_MDSE、SMU_MITB、SMU_MSCOMPUTING | 无 | 补全所有达到门槛的 AI、数据科学及技术管理项目。 |
| test03 | NTU_ENTERPRISE_AI、NTU_MSIS、NUS_AII、NUS_MSBA、SMU_MAF、SMU_MITB、SMU_MQF、SMU_MSCOMPUTING、SMU_MSE、SMU_MSFE | NTU_MSDS | 补全商业分析、金融和数据项目；NTU_MSDS 官方学费 S$65,748.80，超过 S$65,000 预算。 |
| test04 | NUS_DSML、NUS_SIDT、SMU_MDSE、SMU_MSE、SMU_MSFE | NTU_MSBA | 补全数据、经济及产品方向项目；NTU_MSBA 官方学费 S$75,210，超过 S$65,000 预算。 |
| test05 | NTU_MSIS、NUS_MSBA、SMU_MDSE | 无 | 补全达到门槛的商业分析、数据经济及信息系统项目。 |
| test06 | NUS_AII | 无 | NUS_AII 在 AI 产品落地、职业目标及背景三项上达到门槛。 |
| test07 | NTU_ENTERPRISE_AI、NTU_MSIS | NTU_FINTECH、NUS_DFINTECH | 补全企业 AI 与信息系统；两项金融科技课程的官网学费均超过 S$65,000 预算。 |
| test08 | NTU_ANALYTICS、NUS_DSML、NUS_MSBA、SMU_MDSE、SMU_MITB、SMU_MSE | NTU_FINTECH | 补全分析、数据、金融及经济项目；NTU_FINTECH 官方学费 S$68,378.75，超过 S$65,000 预算。 |
| test09 | NUS_MSBA | SMU_MQF | 补全符合门槛的商业分析项目；SMU_MQF 官方学费 S$63,220，超过 S$60,000 预算。 |
| test10 | NUS_MSBA | SMU_MSFE | 补全符合门槛的商业分析项目；SMU_MSFE 官方学费 S$57,700，超过 S$55,000 预算。 |
| test11 | NUS_AII、NUS_MSBA、SMU_MSCOMPUTING | NTU_ENTERPRISE_AI | 补全 AI、商业分析与计算项目；NTU_ENTERPRISE_AI 官方学费 S$60,085，超过 S$60,000 预算。 |
| test12 | NTU_ENTERPRISE_AI、NUS_AII、NUS_SIDT | NUS_MCOMP_GT | 补全 AI 和数字转型项目；NUS_MCOMP_GT 官方学费 S$76,409，超过 S$60,000 预算。 |
| test13 | NTU_FINTECH、NTU_MSDS、NUS_DSML、NUS_MSBA、NUS_SIDT、SMU_MDSE、SMU_MITB | NUS_MCOMP_GT | 补全数据、金融科技及技术管理项目；NUS_MCOMP_GT 官方学费 S$76,409，超过 S$70,000 预算。 |
| test14 | NTU_ANALYTICS、NTU_ENTERPRISE_AI、NTU_MSIS、NUS_AII、NUS_DSML、SMU_MITB、SMU_MSE、SMU_MSFE | SMU_MQF | 补全分析、AI、金融及经济项目；SMU_MQF 与目标和兴趣的固定相关性得分不足 3 分。 |
| test15 | NTU_ENTERPRISE_AI、NTU_MSIS、NUS_AII、NUS_SIDT、SMU_MDSE、SMU_MSE | NTU_MSBA | 补全 AI、信息系统、数据经济项目；NTU_MSBA 官方学费 S$75,210，超过 S$65,000 预算。 |
| test16 | NTU_MSIS、NUS_DSML、NUS_MSBA、SMU_MDSE、SMU_MSCOMPUTING | 无 | 补全商业分析、数据科学、信息系统与计算项目。 |
| test17 | SMU_MITB、SMU_MSE | NTU_ENTERPRISE_AI | 补全商业技术和经济方向；NTU_ENTERPRISE_AI 官方学费 S$60,085，超过 S$60,000 预算。 |
| test18 | NTU_ANALYTICS、NTU_ENTERPRISE_AI、NUS_AII、NUS_DSML、NUS_MSBA、SMU_MAF、SMU_MITB、SMU_MQF、SMU_MSCOMPUTING、SMU_MSE | NTU_FINTECH、NUS_DFINTECH | 补全金融、分析、AI 和数据项目；两项金融科技课程的官网学费均超过 S$65,000 预算。 |
| test19 | NTU_ANALYTICS、NTU_ENTERPRISE_AI、NTU_FINTECH、NTU_MSDS、NTU_MSIS、NUS_AII、NUS_MSBA、NUS_SIDT、SMU_MDSE、SMU_MITB、SMU_MSCOMPUTING | 无 | 补全所有达到门槛的 AI、数据、分析、金融科技和计算项目。 |
| test20 | NTU_ANALYTICS、NTU_ENTERPRISE_AI、NUS_AII、NUS_MSBA、SMU_MDSE、SMU_MSE | NUS_MCOMP_GT | 补全商业分析、AI、分析与经济项目；NUS_MCOMP_GT 官方学费 S$76,409，超过 S$70,000 预算。 |
| test21 | NUS_DSML、NUS_MSBA、SMU_MDSE、SMU_MITB、SMU_MSE | 无 | 补全商业分析、数据、金融与经济项目。 |
| test22 | NTU_ANALYTICS、NTU_ENTERPRISE_AI、NTU_FINTECH、NTU_MSIS、NUS_DSML、NUS_MSBA、NUS_SIDT、SMU_MDSE、SMU_MITB | NUS_MCOMP_GT | 补全数据、分析、金融科技和技术管理项目；NUS_MCOMP_GT 官方学费 S$76,409，超过 S$70,000 预算。 |
| test23 | 无 | SMU_MSFE | SMU_MSFE 官方学费 S$57,700，超过 S$55,000 预算。 |
| test24 | NTU_MSIS、NUS_MSBA、SMU_MDSE | NTU_ENTERPRISE_AI | 补全商业分析、信息系统与数据经济项目；NTU_ENTERPRISE_AI 官方学费 S$60,085，超过 S$60,000 预算。 |
| test25 | NTU_ENTERPRISE_AI、NUS_SIDT、SMU_MAF、SMU_MDSE、SMU_MITB、SMU_MQF、SMU_MSE、SMU_MSFE | NTU_MSBA | 补全商业、金融、经济与企业 AI 项目；NTU_MSBA 官方学费 S$75,210，超过 S$65,000 预算。 |
| test26 | NTU_MSIS、NUS_SIDT | NUS_MCOMP_GT | 补全数字转型与信息系统项目；NUS_MCOMP_GT 官方学费 S$76,409，超过 S$65,000 预算。 |
| test27 | NTU_ANALYTICS、NTU_ENTERPRISE_AI、NTU_MSIS、NUS_AII、NUS_DSML、NUS_MSBA、SMU_MDSE、SMU_MITB、SMU_MSCOMPUTING、SMU_MSE、SMU_MSFE | NTU_FINTECH、NUS_DFINTECH | 补全金融、分析、AI 和数据项目；两项金融科技课程的官网学费均超过 S$65,000 预算。 |
| test28 | NTU_MSIS、NUS_SIDT、SMU_MDSE | NTU_ENTERPRISE_AI | 补全数字转型、信息系统与数据经济项目；NTU_ENTERPRISE_AI 官方学费 S$60,085，超过 S$60,000 预算。 |
| test29 | NUS_DSML、NUS_MSBA、SMU_MITB | NTU_ANALYTICS | 补全数据科学、商业分析与商业技术项目；NTU_ANALYTICS 官方学费 S$64,841.92，超过 S$60,000 预算。 |
| test30 | NTU_MSIS、NUS_MSBA | 无 | 补全符合门槛的商业分析与信息系统项目。 |

## 解释限制

这些标签仍由项目作者进行第二次复核，属于作者标注的自评基准，不是独立专家或外部用户的真实偏好数据。课程学费和页面内容可能继续变化；后续使用时应重新核验官网。
