# SGGradMatch 单人复核资料与操作指南

## 1. 复核分为两项

### A. 课程数据复核（Source audit）

目的：确认系统使用的 21 个硕士项目资料仍然准确。逐个打开大学官方网页，核对项目名称、学习模式、学制、学费、申请背景、课程内容和就业方向，然后更新课程目录中的资料及 `last_verified_at`。

### B. 适配标签复核（Suitability-label review）

目的：在不看系统推荐结果和旧标签的情况下，独立判断 30 个测试用户分别适合哪些项目。最终填写 `eval/solo_review_template.csv`。

两项复核应分开进行。先完成课程数据复核并冻结课程目录，再做适配标签复核；否则不同测试用户可能依据不同版本的课程资料。

## 2. 允许使用的资料

| 优先级 | 资料 | 用途 |
| ---: | --- | --- |
| 1 | 21 个大学官方项目网页 | 课程事实的最终依据；与本地资料冲突时，以官方网页为准 |
| 2 | `data/processed/programmes.csv` | 统一查看课程模式、学制、学费、背景、领域、课程和就业方向 |
| 3 | `data/sources/source_registry.csv` | 查找每个项目的官方网页和上次核实日期 |
| 4 | `eval/test_profiles.jsonl` | 查看 30 个测试用户的背景、职业目标、兴趣、预算、模式和最长学制 |
| 5 | `eval/suitability_rubric.md` | 对所有用户使用同一套排除规则和 5 分相关性规则 |
| 6 | `docs/data_dictionary.md` | 理解每个字段以及空值的含义 |
| 7 | `eval/solo_review_template.csv` | 填写最终适合项目 ID 和复核备注 |

### 不能作为复核依据的资料

完成全部 30 个用户的第二次标注之前，不要打开或使用：

- `eval/ground_truth.jsonl`：这是第一次标签，会造成锚定偏差。
- `eval/results/evaluation_results.json`：包含系统已经推荐的项目。
- 系统网页、命令行推荐结果或任何 Top 3 输出。
- `eval/dev_profiles.jsonl`：它用于开发调试，不属于最终 30 个测试用户。
- 自己记得的旧答案。如果记不清，应重新按评分标准判断并在备注中说明不确定性。

## 3. 21 个项目的官方资料入口

以下页面是课程事实的第一依据。学费、课程和录取规则容易变化，提交前应重新查看。

### NUS（7 个）

| 项目 ID | 项目 | 官方页面 |
| --- | --- | --- |
| `NUS_MCOMP_AI` | Master of Computing in Artificial Intelligence | [NUS School of Computing](https://www.comp.nus.edu.sg/programmes/pg/mcomp-ai/) |
| `NUS_MCOMP_GT` | Master of Computing General Track | [NUS School of Computing](https://www.comp.nus.edu.sg/programmes/pg/mcomp-gen/) |
| `NUS_MSBA` | Master of Science in Business Analytics | [NUS Business School](https://bschool.nus.edu.sg/analytics-operations/masters-degrees/msba/) |
| `NUS_DSML` | Master of Science in Data Science and Machine Learning | [NUS Mathematics](https://www.math.nus.edu.sg/ms-dsml-v1/) |
| `NUS_DFINTECH` | Master of Science in Digital Financial Technology | [NUS Master's Programmes](https://masters.nus.edu.sg/programmes/master-of-science-in-digital-financial-technology) |
| `NUS_AII` | Master of Science in Artificial Intelligence and Innovation | [NUS SCALE](https://scale.nus.edu.sg/programmes/graduate/msc-%28artificial-intelligence-innovation%29) |
| `NUS_SIDT` | Master of Science in Smart Industries and Digital Transformation | [NUS SCALE](https://scale.nus.edu.sg/programmes/graduate/msc-%28smart-industries-and-digital-transformation%29) |

### NTU（7 个）

| 项目 ID | 项目 | 官方页面 |
| --- | --- | --- |
| `NTU_MSAI` | Master of Science in Artificial Intelligence | [NTU College of Engineering](https://www.ntu.edu.sg/engineering/coe-programmes/graduate/coe-programme-detail/master-of-science-in-artificial-intelligence) |
| `NTU_MSDS` | Master of Science in Data Science | [NTU SPMS](https://www.ntu.edu.sg/spms/admissions/grad/detail/master-of-science-in-data-science-%28msds%29) |
| `NTU_ANALYTICS` | Master of Science in Analytics | [NTU SPMS](https://www.ntu.edu.sg/spms/about-us/mathematics/grad/msc-in-analytics) |
| `NTU_FINTECH` | Master of Science in Financial Technology | [NTU SPMS](https://www.ntu.edu.sg/spms/about-us/mathematics/grad/msc-in-financial-technology) |
| `NTU_ENTERPRISE_AI` | Master of Science in Enterprise Artificial Intelligence | [NTU SPMS](https://www.ntu.edu.sg/spms/admissions/grad/detail/master-of-science-in-enterprise-artificial-intelligence) |
| `NTU_MSIS` | Master of Science in Information Systems | [NTU SPMS](https://www.ntu.edu.sg/spms/admissions/grad/detail/master-in-science-in-information-systems) |
| `NTU_MSBA` | Master of Science in Business Analytics | [NTU Business School](https://www.ntu.edu.sg/business/education/graduate-programme/master-of-science-in-business-analytics) |

### SMU（7 个）

| 项目 ID | 项目 | 官方页面 |
| --- | --- | --- |
| `SMU_MITB` | Master of IT in Business | [SMU Master's Programmes](https://masters.smu.edu.sg/programme/master-of-it-in-business) |
| `SMU_MSCOMPUTING` | Master of Science in Computing | [SMU School of Computing and Information Systems](https://computing.smu.edu.sg/mscomputing) |
| `SMU_MAF` | Master of Science in Applied Finance | [SMU Master's Programmes](https://masters.smu.edu.sg/programme/msc-in-applied-finance) |
| `SMU_MDSE` | Master of Data Science in Economics | [SMU Master's Programmes](https://masters.smu.edu.sg/programme/master-of-data-science-economics) |
| `SMU_MSFE` | Master of Science in Financial Economics | [SMU Master's Programmes](https://masters.smu.edu.sg/programme/master-in-financial-economics) |
| `SMU_MQF` | Master of Science in Quantitative Finance | [SMU Master's Programmes](https://masters.smu.edu.sg/programme/msc-in-quantitative-finance) |
| `SMU_MSE` | Master of Science in Economics | [SMU Master's Programmes](https://masters.smu.edu.sg/programme/master-in-economics) |

## 4. 每个项目需要核对什么

逐项填写或确认以下内容。网页没有清楚说明时保留空值，不猜测。

1. `programme_name`：项目正式名称。
2. `study_modes`：全日制、非全日制或两者都有。
3. `duration_ft_months` / `duration_pt_months`：对应模式的正常或公布学制。
4. `tuition_sgd`：项目总学费；不要把每学期费用或申请费误当总学费。
5. `academic_backgrounds`：官网明确接受、偏好或要求的学术背景。
6. `experience_note`：工作经验、先修课程、桥梁课程等重要限制。
7. `domains` / `curriculum`：只能概括官网支持的核心领域和课程。
8. `career_outcomes`：依据项目培养方向作宽泛归纳，不写就业保证。
9. `source_url`：必须是大学官方页面。
10. `last_verified_at`：完成核对当天的日期。

## 5. 每个测试用户需要看什么

从 `eval/test_profiles.jsonl` 读取七项输入：

- `academic_background`：学术背景；用于背景匹配的 1 分。
- `career_goal`：职业目标；用于职业相关性的 0–2 分。
- `interests`：三个兴趣；用于领域/课程相关性的 0–2 分。
- `budget_sgd`：最高预算；只排除已知学费超过预算的项目。
- `preferred_mode`：学习模式；项目不提供该模式时排除。
- `max_duration_months`：最长可接受学制；已知学制超出时排除。
- `years_experience`：在官网明确规定或偏好工作经验时用于判断并写备注。

30 个测试用户涵盖 AI/机器学习、数据科学、商业分析、数字化转型、金融科技、量化金融、经济学、信息系统、数据工程及网络安全等方向。必须按 `test01` 至 `test30` 顺序全部完成，不能只复核系统表现不好的案例。

## 6. 固定判断方法

### 第一步：硬约束

只在课程目录有明确事实时排除：

- 不提供用户要求的学习模式；
- 已知总学费超过用户预算；
- 已知对应模式学制超过用户上限。

学费或学制为空不等于符合条件，也不等于不符合条件。保留该项目，并在 `author_review_notes` 中记录“费用未知”或“学制未知”。

### 第二步：相关性计分（最高 5 分）

| 项目 | 0 分 | 1 分 | 2 分 |
| --- | --- | --- | --- |
| 职业目标 | 无实质支持 | 邻近但不是核心方向 | 直接对应课程领域或就业方向 |
| 兴趣 | 无匹配 | 1 个兴趣匹配 | 至少 2 个兴趣匹配 |
| 学术背景 | 官网支持不清楚 | 官网列出该背景，或明确接受广泛背景 | 不适用 |

总分至少 3 分、并且没有已知硬约束冲突，才标为 suitable。不要因为“可能录取”而加分，也不要判断实际录取概率。

### 第三步：填写

在 `eval/solo_review_template.csv` 中：

- 第二列填写所有 suitable 的项目 ID，用 `|` 分隔；不限制为 3 个。
- 第三列记录边界判断、未知学费/学制、官网表述不清或背景要求问题。
- 先完成全部 30 行，再与旧标签比较。

## 7. 建议执行顺序

1. 复制一份空白 `solo_review_template.csv` 作为工作副本。
2. 按官方页面核对 21 个项目，并冻结 `programmes.csv`。
3. 暂时关闭旧标签、评估结果和推荐系统。
4. 打开评分标准、冻结后的课程目录、测试用户文件和空白复核表。
5. 从 `test01` 开始，对 21 个项目逐一做硬约束检查和相关性评分。
6. 完成 `test01` 至 `test30` 后保存并标记日期。
7. 才打开 `ground_truth.jsonl`，逐行比较两次标签。
8. 对每个变化记录原因：事实修正、评分规则原先使用不一致、漏填或抄写错误。
9. 冻结新标签，运行一次最终评估；不要根据最终测试结果继续调权重。

## 8. 复核完成的证据

最终仓库至少应保留：

- 更新后的 `programmes.csv` 和 `source_registry.csv`；
- 填写完整的 `solo_review_template.csv`；
- 一份标签变更记录；
- 重新生成的 `evaluation_results.json`；
- 报告中对“作者自行标注与复核”的透明说明。

