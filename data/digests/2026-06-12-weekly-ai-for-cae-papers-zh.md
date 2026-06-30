# Weekly AI for CAE Papers - 2026-06-12

## 本周我做了什么

- 搜索时间范围：主范围为 2026-06-05 至 2026-06-12；在定稿前额外补查了 2026-06-10 至 2026-06-12 最近 24-48 小时的新论文与预印本，避免漏掉周五早晨刚上线的条目。
- 读取的本地候选日志：`data/digests/2026-06-05-candidates.json`、`2026-06-06-candidates.json`、`2026-06-07-candidates.json`、`2026-06-08-candidates.json`、`2026-06-09-candidates.json`、`2026-06-10-candidates.json`、`2026-06-11-candidates.json`、`2026-06-12-candidates.json`，以及对应的 `briefing-input.md`；另外检查了 `paper_watch/2026-06-05-candidates.md`。
- 检查的外部来源：arXiv 预印本页、搜索结果中的 Semantic Scholar/Crossref 线索、Siemens/Rescale 等工程 AI 新闻源用于发现线索，但最终入选只保留论文或正式技术报告/综述级材料。
- 主要关键词族：
  - `CAD / CAE / engineering simulation / CFD / FEA / surrogate / reduced order / graph neural network / physics-informed`
  - `OpenFOAM / Fluent / COMSOL / Ansys / SimScale / Siemens`
  - `microfluidic / nozzle / liquid jet / fatigue / digital twin / MBSE / process systems engineering / industrial RAG`
- 本地日志可知的候选规模：仅 `2026-06-11` 与 `2026-06-12` 两天的 run log 就分别抓取了 380 和 376 条原始候选，过滤后分别剩 147 和 118 条；但其中绝大多数是新闻、博客、公司发布或泛 AI 条目，不是论文。
- 去重与过滤标准：
  - 先按标题、规范化 URL、arXiv 编号去重。
  - 只保留 2026-06-05 之后公开可核验的论文/预印本/正式技术报告级文献。
  - 优先保留同时满足“AI + 工程建模/仿真/CAE/CAD/工业设计/过程工程”交集的条目。
  - 企业博客、融资新闻、产品发布、没有论文正文或摘要支撑的条目全部剔除。
- 排除内容与原因：
  - Siemens/Rescale/Prometheus 等新闻或博客：有价值，但不是论文。
  - 许多 CAD/CFD 论文是 5 月或更早，不属于本周新增。
  - 少数搜索结果虽然带有 simulation/engineering 关键词，但实际是教育、量子模拟或泛 AI 论文，已排除。
- 局限性：
  - 本地 daily watch 更偏新闻发现，不是论文数据库，所以只能作为线索池。
  - 部分 arXiv 页不稳定暴露作者单位；作者单位仅在能可靠核验时填写，否则标记为“未在当前检索中稳定获得”。
  - 本周公开源中高相关新增论文数量不足，因此本周仅给出 6 篇可信新匹配，没有硬凑到 10 篇。

## 筛选标准

- 时效性：以 2026-06-05 至 2026-06-12 的新增论文为硬约束；只有本周新增才进入主名单。
- 相关性：优先级最高的是 AI 直接用于 CAD、CAE、CFD、FEA、工程仿真、过程工程、工业设计迭代、数字孪生或可落地工程工作流。
- 来源质量：优先 arXiv 预印本和可直接追溯的原始论文页；没有开放全文时至少应有稳定摘要页。
- 工业/工程可用性：优先那些明确讨论速度提升、跨几何泛化、物理约束、网格/求解器兼容性、可用于设计迭代或工业部署的工作。
- 主题多样性：在 CAD 生成、CFD surrogate、FEA surrogate、多尺度力学重建、过程系统工程中的 LLM 之间做平衡，避免全被单一子方向占满。

## 本周入选论文

### 1. 中文标题
用于过程系统工程的 大语言模型：机会、体系结构与工业部署挑战

- 原始标题：Large Language Models in Process Systems Engineering: Opportunities, Architectures, and Industrial Deployment Challenges
- 作者：Bhushan Gopaluni, Vidya Kotamraju, Syon Bhushan
- 作者单位：未在当前检索中稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-10
- 中文摘要：这是一篇面向 Process Systems Engineering 的系统综述，按过程设计与工程、过程建模与仿真、时间序列预测、优化与调度、过程控制、故障检测与诊断等七类整理 LLM 应用。论文认为 LLM 在查询文档、整合非结构化知识和人机交互方面已显示出明确价值，但在实时执行、约束满足和安全保证方面仍存在显著缺口。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.11589)
- 为什么匹配你的兴趣：它直接覆盖工程建模、过程仿真、工业知识检索与部署约束，和你关心的工业 RAG、工程仿真工作流、MBSE/工程知识系统高度相关。
- 选择说明：这是本周最值得跟踪的“工程领域 LLM 总览”之一；不是最 CAE-core 的那篇，但对工业落地判断价值很高。

### 2. 中文标题
面向实验流场预测的数据驱动代理模型

- 原始标题：Data-driven surrogate models for forecasting experimentally measured fluid flows
- 作者：Peter I. Renn, Emily H. Palmer, Cong Wang, Morteza Gharib
- 作者单位：未在当前检索中稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-09
- 中文摘要：论文研究如何直接基于实验测得的圆柱尾流速度场训练代理模型，实现快于实时的流场预测。作者比较了 FCNN、U-Net、Fourier Neural Operator 与基于 DMD 的模型，发现这些方法在短时预测和低频动力学传播上有意义，但在噪声观测、不完整状态和更强三维/湍流效应下仍难以稳定保持瞬态结构和高频能量。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.10848)
- 为什么匹配你的兴趣：它正中 CFD surrogate、实验-仿真结合、流动预测和工业可用性边界这几个主题，对液体射流、样品输运和实验装置流动控制都具参考意义。
- 选择说明：优势在于它没有只报“加速比”，而是明确讨论了真实实验噪声与观测缺失下的失效模式。

### 3. 中文标题
结合循环神经网络与物理约束图神经网络的非线性力学场重建

- 原始标题：Non-linear mechanical field reconstruction coupling recurrent neural networks with physics-informed graph neural networks
- 作者：Manuel Ricardo Guevara Garban, Yves Chemisky, Etienne Pruliere, Michael Clement, Martin Abendroth, Bjorn Kiefer
- 作者单位：未在当前检索中稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-09
- 中文摘要：该工作针对非线性、历程相关载荷下异质微结构的局部应力场重建问题，提出 LSTM 与 physics-informed GNN 的耦合框架。LSTM 编码宏观应力-应变路径，GNN 负责每个时间步的空间应力场重建，并通过离散平衡罚项和逐步升温的相对加权策略解决弹塑性场景中损失尺度不匹配的问题。作者报告相对有限元有三个数量级加速，并能泛化到不同网格类型与分辨率。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.10909)
- 为什么匹配你的兴趣：这篇非常贴近 CAE 核心，覆盖非线性材料、弹塑性、多尺度仿真、网格无关 surrogate 和结构仿真加速。
- 选择说明：本周最强的“工程力学 surrogate”条目之一，优先级很高。

### 4. 中文标题
面向任意几何的有限元仿真加速网格图神经网络框架

- 原始标题：Mesh Graph Neural Network Framework for Accelerating Finite Element Simulation for Arbitrary Geometries
- 作者：Josiah D. Kunz, Kamal Choudhary
- 作者单位：未在当前检索中稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-06
- 中文摘要：论文提出一个用于 2D 结构件 von Mises 应力预测的 mesh graph network，以解决传统机器学习 surrogate 难以跨几何泛化的问题。方法不直接依赖绝对坐标，而使用节点类型、相对边特征和全局载荷特征，因此天然具备平移与旋转不变性。作者在未见几何和未见载荷上报告显著优于 Random Forest、Gradient Boosting 和 KNN 等常规基线。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.08287)
- 为什么匹配你的兴趣：这正是 FEA surrogate 在多设计迭代、任意几何泛化和工程设计空间探索中的关键痛点。
- 选择说明：如果你在关注 Siemens PhysicsAI、Ansys/Altair 类“跨几何 surrogate”方向，这篇值得优先读。

### 5. 中文标题
用于流动代理建模的 Drifting Models

- 原始标题：Drifting Models for Surrogate Flow Modeling
- 作者：Chris R. Jung, Markus Doerr, Natalie Juengling, Jennifer Niessner, Adam T. Mueller, Nicolaj C. Stache
- 作者单位：未在当前检索中稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-05
- 中文摘要：论文将新近的 generative drifting 框架引入流体 surrogate 建模，目标是在保持高质量流场生成的同时避免 diffusion 类模型推理过慢的问题。作者采用条件化架构，在 VAE 潜空间中执行 drifting，并利用边界条件相关的掩码对齐生成样本。结果显示该模型在精度与流动一致性上接近迭代式 diffusion，但推理速度可快两个数量级。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.07481)
- 为什么匹配你的兴趣：这直接对应“CFD 代理模型是否能进入实时设计空间探索”的问题，对室内流动、喷射/通风以及更广泛的快速流场评估都相关。
- 选择说明：它不是 OpenFOAM/Fluent 绑定型论文，但在 surrogate inference speed 这件事上很关键。

### 6. 中文标题
GuideCAD：基于前缀嵌入的轻量级多模态 3D CAD 生成框架

- 原始标题：GuideCAD: A Lightweight Multimodal Framework for 3D CAD Model Generation via Prefix Embedding
- 作者：Minseong Kim, Jinyeong Park, Sungho Park, Jibum Kim
- 作者单位：未在当前检索中稳定获得
- 来源/期刊/会议/预印本服务器：arXiv 预印本
- 发布日期：2026-06-05
- 中文摘要：这篇工作提出一个面向 3D CAD 生成的轻量级多模态框架，通过映射网络把图像嵌入转换为 prefix embeddings，让预训练大语言模型更高效地融合视觉与文本信息，再由 transformer decoder 预测 CAD construction sequence。作者声称在保持生成质量的同时，所需可训练参数约减少四倍、训练效率约提升两倍。
- 原文链接：[arXiv](https://arxiv.org/abs/2606.07024)
- 为什么匹配你的兴趣：它属于你明确关心的 AI for CAD / generative design 主线，而且强调工程可编辑的 construction sequence，而不是只生成网格或图片。
- 选择说明：优先级略低于 FEA/CFD surrogate 条目，因为它更偏 CAD 生成，但本周在 CAD 方向里是较新的强相关项。

## 为什么本周没有凑满 10 篇

- 在 2026-06-05 至 2026-06-12 这个窗口内，公开可核验且与 AI-for-CAE/engineering simulation 高度重合的新论文数量不足。
- 检索中有一些“边界上相关”的条目，例如更早几周的 CAD+FEA agent 论文、5 月底的 solid mechanics surrogate、以及企业博客中的工程 AI 案例，但它们不满足“本周新增”或“论文优先”的约束。
- 因此本周主名单只给出 6 篇，优先保证可信度和可追溯性。

## 下周我会怎么调整

- 加强对 arXiv 最近 7 天 `cs.LG`、`cs.CE`、`cs.AI`、`physics.flu-dyn`、`cond-mat`、`stat.ML` 中工程仿真相关关键词的定向扫描，而不是仅依赖通用搜索。
- 把以下查询保留为 watchlist，并在下周直接复用：
  - `site:arxiv.org/abs CAD generative engineering design`
  - `site:arxiv.org/abs CFD surrogate flow modeling`
  - `site:arxiv.org/abs finite element graph neural network arbitrary geometries`
  - `site:arxiv.org/abs physics-informed graph neural network elastoplasticity`
  - `site:arxiv.org/abs process systems engineering large language models`
  - `site:arxiv.org/abs microfluidic flow machine learning surrogate`
  - `site:arxiv.org/abs nozzle optimization machine learning CFD`
  - `site:arxiv.org/abs optical coating damage simulation machine learning`
