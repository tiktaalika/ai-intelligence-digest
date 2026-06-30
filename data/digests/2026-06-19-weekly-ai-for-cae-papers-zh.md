# Weekly AI for CAE Papers - 2026-06-19

## 本周我做了什么

- 搜索时间范围：主范围为 2026-06-12 至 2026-06-19；定稿前额外补查了 2026-06-17 至 2026-06-19 最近 24-48 小时上线的论文，避免漏掉周五早晨新出的 arXiv 条目。
- 读取的本地候选日志：
  - `data/digests/2026-06-12-candidates.json`
  - `data/digests/2026-06-13-candidates.json`
  - `data/digests/2026-06-14-candidates.json`
  - `data/digests/2026-06-15-candidates.json`
  - `data/digests/2026-06-16-candidates.json`
  - `data/digests/2026-06-17-candidates.json`
  - `data/digests/2026-06-18-candidates.json`
  - `data/digests/2026-06-19-candidates.json`
- 本地日志可量化规模：8 天日志合计抓取 3001 条原始候选，过滤后剩 838 条，日志内记录的显式重复 18 条。
- 额外检查的来源：arXiv 原始论文页、搜索结果中 surfaced 的 Semantic Scholar/Crossref/publisher 线索；最终入选优先保留可直接落到原始论文页或 arXiv 页的条目。
- 主要关键词族：
  - `AI for CAD / CAD generation / engineering design / feature graph / surrogate`
  - `finite element / plasticity / graph neural network / elastoplasticity / surrogate`
  - `engineering simulation / digital twin / MBSE / systems engineering / process systems engineering`
  - `CFD / fluid flow / microfluidic / nozzle / OpenFOAM / Fluent / COMSOL`
- 去重与过滤标准：
  - 先按标题、arXiv 编号、规范化 URL 去重。
  - 只保留可核验的论文、预印本、已接收会议论文或正式 paper page。
  - 优先保留“AI/ML/LLM/数据驱动方法”和“CAE/CAD/工程仿真/数字孪生/MBSE/工业系统”交集强的条目。
  - 企业博客、产品发布、融资/新闻、没有摘要支撑的网页全部剔除。
- 这周排除了什么：
  - 本地 daily logs 里的 Siemens、Ansys、AWS、NVIDIA、DeepMind 等大量新闻/博客条目，虽然能提供方向线索，但不是论文。
  - 若论文与 CAE/工程仿真的交集过弱，例如纯通用 AI、纯医学 AI、纯消费级 agent 论文，则不纳入主名单。
  - 上周已经纳入的论文，即便仍在检索结果中出现，也不重复列入本周主名单。
- 局限性：
  - 本地 daily watch 更偏发现新闻和厂商动态，不是学术数据库，因此只能作为主候选池的“线索层”，不能直接当论文清单。
  - shell 内直接访问学术 REST API 在本次运行中没有拿到有效响应，因此“fresh search”主要依赖 web 检索到的原始论文页，而不是 API 批量拉取。
  - arXiv 可稳定提供作者、日期、摘要，但作者单位经常不直接显示；只有在当前可访问页面能稳定确认时才写单位，否则标明未稳定获得。
  - 在 2026-06-12 至 2026-06-19 这一窗口里，高相关且可信的新论文数量明显不足，因此本周只给出 5 篇，没有硬凑到 10 篇。

## 筛选标准

- 时效性：优先 2026-06-12 至 2026-06-19 新出现或新提交的论文；只有在本周窗口内确实不够时，才考虑边界条目，但本周最终没有用边界旧条目来凑数。
- 相关性：优先级最高的是 AI 直接用于 CAD、CAE、FEA、工程仿真、数字孪生、MBSE、过程工程或工程设计自动化的论文。
- 来源质量：优先 arXiv 原始页和可追溯论文页；如果只有二手报道而没有 paper page，不入选。
- 工业/工程可用性：优先那些明确讨论仿真加速、可部署工作流、跨几何泛化、工程约束、可验证性或设计迭代价值的工作。
- 主题多样性：在结构仿真、几何/CAD、数字孪生和系统工程之间做平衡，不让单一子方向占满名单。

## 本周入选论文

### 1. 中文标题
面向塑性材料模型时间积分的机器学习加速框架

- 原始标题：Machine Learning-Accelerated Time Integration of Plasticity Models
- 作者：Nasrin Talebi, Magnus Ekh, Knut Andreas Meyer
- 作者单位：未在当前可访问页面稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-12
- 中文摘要：论文针对有限元中非线性材料本构积分成本高的问题，提出一种基于神经网络的显式时间积分框架，用神经网络直接预测状态变量更新，从而在保持较大时间步长的同时降低计算代价。该方法以不变量为输入，并把必要的演化方向通过训练数据与解析结构结合起来，同时显式满足塑性一致性条件。作者在 von Mises 屈服准则和非线性运动硬化原型模型上评估了方法，并将其嵌入有限元边值问题中，结果显示在精度、数值稳定性和计算效率上都具有较好表现。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.14548)
- 为什么匹配你的兴趣：这篇非常贴近 CAE 核心，直接处理 FE 材料积分这一真正耗时的工业瓶颈，对损伤、疲劳、成形和非线性结构分析都有现实意义。
- 选择说明：本周最值得优先读的条目之一，因为它不是泛泛而谈 surrogate，而是切进 FE 工作流里最硬的局部积分环节。

### 2. 中文标题
用于参数曲面测地样曲线计算的神经网络框架

- 原始标题：A Neural Network Framework for Geodesic-Like Curve Computation on Parametric Surfaces
- 作者：Sheng-Gwo Chen, Chen-Chang Peng
- 作者单位：未在当前可访问页面稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-17
- 中文摘要：该工作围绕参数曲面上的最短路径近似问题，提出一个基于深度学习与 Physics-Informed Neural Networks 的 geodesic-like curve 计算框架。作者强调，这一框架不仅能处理单一参数曲面，还能处理更复杂的多曲面系统、具有至少 C0 连续性的拼接曲面，以及旋转曲面。核心价值不在“生成式 AI”，而在于把几何约束与 PINN 结合为一个更高效的曲面路径求解框架。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.18759)
- 为什么匹配你的兴趣：它更偏 CAD/CAM/几何计算，但与工程曲面建模、路径规划、复杂表面设计与参数化几何处理直接相关。
- 选择说明：这篇不是本周最强的 CAE 实用论文，但它属于“几何计算 + 神经网络 + 工程曲面”这个你关心而且本周确实有新增的方向。

### 3. 中文标题
利用 LiDAR 点云与 OpenStreetMap 自动构建高速公路场景数字孪生

- 原始标题：Automated Digital Twin Construction for Highway Scenarios Using LiDAR Point Clouds and OpenStreetMap
- 作者：Yongqi Zhao, Dong Bi, Paul Kovacevic, Tomislav Mihalj, Martin Schabauer, Johannes Betz, Arno Eichberger
- 作者单位：未在当前可访问页面稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-15
- 中文摘要：论文提出一条自动化工作流，将移动测绘 LiDAR 的车道级几何精度与 OpenStreetMap 的道路拓扑结合，生成地理配准的 ASAM OpenDRIVE 高速公路场景地图。方法通过 LiDAR 重建主线道路，通过 OSM 推断匝道几何和拓扑，从而在无需完整传感器覆盖的情况下补全高速公路互通区域。实验报告平均横向 RMSE 为 0.740 米，输出结果可直接用于 IPG CarMaker 和 Esmini 等主流仿真平台。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.16570)
- 为什么匹配你的兴趣：它不属于典型 LLM 论文，但高度贴合“工程仿真前处理自动化”和“数字孪生场景构建”这条实用链路。
- 选择说明：因为它偏 simulation infrastructure 而不是 CAE 求解器本身，所以优先级略低于塑性积分那篇，但工程落地价值很高。

### 4. 中文标题
结合数字孪生仿真的治疗响应优化临床决策支持 AI 系统

- 原始标题：Treatment Response Optimized Clinical Decision Support AI System via Digital Twin Simulation
- 作者：Xinyu Qin, Anil K. Sood, Ruiheng Yu, Sara Corvigno, Elaine Stur, Lu Wang
- 作者单位：未在当前可访问页面稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本；已被 IEEE EMBC 2026 接收
- 发布日期：2026-06-16
- 中文摘要：论文提出一个在线自适应框架，把治疗效应估计、患者数字孪生和强化学习组合起来，用于序列治疗决策。系统先在历史病历上训练，并在运行中持续学习；同时通过规则模块阻止禁忌治疗，并把内部模型分歧较大的病例升级给专家复核。作者在合成临床模拟器和真实卵巢癌数据集上验证了方法，结果显示它在疗效、稳定性和低延迟方面优于对照基线。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.17405)
- 为什么匹配你的兴趣：这篇不是 CAE 狭义核心，但它代表了“数字孪生 + 仿真 + AI 决策”的方法学方向，对工业数字孪生中的闭环优化和安全约束设计有参考意义。
- 选择说明：列入是因为它在“仿真驱动 AI 决策”方法上有可迁移性，但如果你只关心机械/流体 CAE，它不是第一优先级。

### 5. 中文标题
用于水路物流预测决策的数字孪生仿真

- 原始标题：Digital Twin-Based Simulation for Predictive Decision-Making in Waterway Logistics
- 作者：Matthijs Jansen op de Haar, Daniel Frutos Rodriguez
- 作者单位：未在当前可访问页面稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本；提交至 IEEE Digital Twin 2026
- 发布日期：2026-06-11
- 中文摘要：论文研究在不确定水位条件下，数字孪生能否改善内河货运路径决策。作者先通过专家访谈归纳三类常见应急场景，再把这些场景嵌入分时仿真环境，对比基于数字孪生的预测式决策与传统反应式方法。结果显示，在 70% 到 100% 的预测精度范围内，预测式建模能显著降低运营成本和运输方式切换，燃油相关成本平均下降 28.3%。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.13492)
- 为什么匹配你的兴趣：它更偏工业系统仿真和数字孪生运营决策，但属于“仿真如何直接进入业务闭环”的真实工程案例。
- 选择说明：这是本周最低优先级的入选项之一，原因是它不直接对应 CAD/CAE 求解器，但在数字孪生应用层很典型。

## 为什么本周没有凑满 10 篇

- 在 2026-06-12 至 2026-06-19 这个窗口内，真正同时满足“新增”“论文级别”“AI/数据驱动方法明确”“与 CAE/工程仿真交集强”的条目数量不足。
- 本地候选池虽然大，但主要是厂商新闻、博客、产品发布和泛 AI 动态，不是 paper-grade 条目。
- 我有意没有把 6 月初已经出现但本周仍能搜到的旧论文、或者仅与工程沾边的通用 AI 论文塞进主名单。

## Watchlist

- `site:arxiv.org/abs finite element plasticity machine learning 2026`
- `site:arxiv.org/abs CAD feature graph engineering design surrogate 2026`
- `site:arxiv.org/abs digital twin simulation engineering decision-making 2026`
- `site:arxiv.org/abs parametric surfaces PINN engineering geometry 2026`
- `site:arxiv.org/abs microfluidic flow machine learning surrogate 2026`
- `site:arxiv.org/abs nozzle optimization machine learning CFD 2026`
- `site:arxiv.org/abs OpenFOAM Fluent COMSOL machine learning 2026`
- `site:arxiv.org/abs process systems engineering large language models 2026`

## 下周我会怎么调整

- 更少依赖 daily news-like candidate logs，把 arXiv 定向搜索放到更前面。
- 对 `cs.CE`、`cs.RO`、`cs.AI`、`physics.flu-dyn`、`cond-mat.mtrl-sci` 中与工程仿真相关的最近提交做更细粒度扫描。
- 增强对“FE 材料模型、疲劳、损伤、流体 surrogate、数字孪生前处理自动化、MBSE + AI、工业 RAG”六条子线的单独检索，而不是用一套大词包扫全域。
- 若下周本地日志仍以新闻为主，建议后续把 daily watch 增加一层 arXiv/OpenAlex 定向源，否则周报每周都需要人工剥离大量非论文噪声。
