# 2026-07-10 每周 AI-for-CAE 论文简报

## 本周我做了什么

本次检索覆盖 2026-07-03 至 2026-07-10，重点补查 2026-07-08 至 2026-07-10 的新增预印本，避免遗漏周五上午前后出现的论文。作为主发现池，我读取了 `/Users/fyang/news push/data/digests/` 下 2026-07-01、2026-07-02、2026-07-04、2026-07-05、2026-07-06、2026-07-07、2026-07-08、2026-07-09 的 `*-candidates.json` 和 `*-briefing-input.md`。这些本地日志合计显示抓取 20553 条、过滤后 2945 条、显式重复 80 条；其中 2026-07-09 的抓取量最大，单日抓取 17173 条、过滤 2239 条。

本地日志中与本主题最接近的线索主要来自 Siemens Simcenter、Rescale、Synera、COMSOL、Neural Concept、Engineering.com、Hugging Face Papers 等来源，例如 agentic AI-aided engineering、GeoTransolver CFD、simulation report generation、weldline mapping、COMSOL 案例和 CAD/CAE 软件更新。但多数是产品新闻、博客、会议报道或工作流页面，不是论文，因此没有直接进入最终 10 篇论文清单，只作为产业背景使用。

在本地日志之外，我补充检索了 arXiv、Semantic Scholar/Crossref 风格的题名与 DOI/出版页线索、搜索引擎暴露的 arXiv 论文页，以及可见的 publisher/preprint 元数据。主要关键词族包括：`CAD foundation model automatic CAD generation`、`CFD surrogate neural operator`、`finite element machine learning engineering simulation`、`physics-informed neural network elastodynamics`、`turbulence closure PINN finite element`、`lattice material design multi-fidelity surrogate`、`PDE-constrained optimization neural operator`、`OpenFOAM Fluent COMSOL machine learning`、`RAG engineering industry`、`microfluidic nozzle liquid jet machine learning CFD`、`optical coating damage simulation AI`、`XFEL synchrotron instrument simulation machine learning`。

本轮外部检索得到约 14 个论文级强候选，最终去重后选出 10 篇。去重依据是题名、arXiv ID、URL、核心作者组合和摘要主题；过滤掉了 2026-06 月旧论文、非论文型产品/博客/新闻、与 CAE/工程仿真关系过弱的通用 RAG/AI 平台论文，以及只有软件版本更新但无研究贡献的条目。需要说明的限制是：多数 arXiv 页面没有稳定展示作者单位；部分 DOI 或期刊版本尚未出现；OpenFOAM、Fluent、COMSOL、液体射流、低温液氢/液氮、XFEL/同步辐射机械设计、光学镜面涂层损伤这些窄主题本周没有找到足够新的强论文匹配。

## 筛选标准

我优先考虑 2026-07-03 至 2026-07-10 内的新预印本或在线发表论文，其次看它是否直接面向 CAE、CAD、CFD、FEA、PDE 求解、工程设计优化、工业仿真加速或物理约束 surrogate。来源质量上，arXiv 预印本、正式期刊/会议页、DOI/publisher 页优先于博客和二手新闻；如果只有新闻报道而无论文页，则排除。

相关性方面，最优先的是能直接改变仿真工作流的论文，例如 neural operator surrogate、PINN、有限元/有限体积一致性、CAD 生成、PDE-constrained inverse design、turbulence closure、工业事故/核工程仿真 surrogate。工业适用性方面，我更看重是否连接真实求解器、有限元/有限体积/CFD 数据、FEniCSx、ANSYS、OpenFOAM、COMSOL 或可迁移的工程设计问题。主题多样性方面，我避免让清单只集中在 PINN 或 neural operator，而保留 CAD、CFD、结构动力学、材料/晶格设计、PDE 自动化流水线和核工程事故仿真。

## 1. 面向 PDE 约束优化的 neural operator 拓扑感知进化策略

- 中文标题：面向 PDE 约束优化的 Neural Operator 拓扑感知进化策略
- 原始标题：Neural Operator-enabled Topology-informed Evolutionary Strategy for PDE-Constrained Optimization
- 作者：Xiangming Huang, Guannan Zhang, Lu Lu, Raphaël Pestourie
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-08
- 中文摘要：论文提出 NOTES，将 DeepONet neural operator、拓扑表征学习和 CMA-ES 进化优化结合，用于高维、非凸的 PDE 约束逆向设计。方法先把设计空间压缩到具有拓扑先验的低维潜空间，再在该空间中寻找适应未见工况的高性能设计。案例包括由 Maxwell 方程约束的纳米光子束偏转器逆设计，以及结构优化问题。结果显示，NOTES 能将设计维度从 256 降至 25，在光子设计中稳定达到超过 95% 的效率，并在结构优化中找到低 compliance 设计。
- 原文链接：https://arxiv.org/abs/2607.07682
- 为什么匹配你的兴趣：它直接对应 generative design、PDE-constrained optimization、CAE surrogate 和工程逆向设计，也接近光学元件设计优化方向。
- 入选说明：本周最值得优先看的方法论文之一，因为它把 neural operator 从“快速预测场”推进到“可迁移设计优化”。

## 2. 多保真框架中用 Bayesian optimization 调节遗传算法超参数以高效设计晶格材料

- 中文标题：多保真框架中用 Bayesian optimization 调节遗传算法超参数以高效设计晶格材料
- 原始标题：Bayesian Optimization of Genetic Algorithm Hyperparameters in a Multi-Fidelity Framework for Efficient Lattice Material Design
- 作者：Sergei Zorkaltsev, Maciej Haranczyk, Christina Schenk
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-08
- 中文摘要：论文提出一个多保真晶格材料设计框架：高保真层使用 FFT homogenization 验证， 中保真层使用 3D CNN surrogate 快速评估材料属性，低保真层使用 Gaussian process surrogate 和 Bayesian optimization 指导遗传算法超参数搜索。作者比较不同 acquisition function，发现 logNEI 对遗传算法评估噪声更稳健。优化后的超参数让 25 代遗传算法达到接近 75 代完整优化的弹性模量水平，并将计算成本从 225 小时降到 171 小时。
- 原文链接：https://arxiv.org/abs/2607.07289
- 为什么匹配你的兴趣：它属于 AI-assisted generative design、材料/结构设计 surrogate、多保真工程优化，适合跟踪可制造结构和轻量化设计。
- 入选说明：不是传统 CFD/FEA solver 加速，但对工程设计空间搜索和高保真验证的结合很有参考价值。

## 3. 多逆变器电力系统小信号稳定性的 Physics-Informed Neural Network

- 中文标题：用于多逆变器电力系统小信号稳定性分析的 PINN
- 原始标题：A Physics-Informed Neural Network for Small-Signal Stability in Multi-Inverter Power Systems
- 作者：Hanxi Chen, Xiangyu Meng, Jianhong Wang, Yue Zhu
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-08
- 中文摘要：论文面向高维多逆变器电力系统，提出一个专用 PINN，用少量电磁暂态仿真生成的阶跃响应数据训练，预测全系统阻抗/导纳模型的 poles 和 residues。传统线性化阻抗模型只能在稳态工作点附近使用，而该 PINN 试图覆盖更大的运行空间，用于识别功率流变化下的振荡风险、稳定裕度和潜在根因。论文在 2-IBR 和 4-IBR 系统上验证了方法。
- 原文链接：https://arxiv.org/abs/2607.07523
- 为什么匹配你的兴趣：它是基于仿真数据的工程系统稳定性 surrogate，属于 model-based systems engineering、仿真加速和物理约束建模交叉。
- 入选说明：与机械 CAE 的距离略远，但“有限仿真数据 + 物理约束 + 系统级稳定性分析”的范式值得保留。

## 4. 双材料体系弹性动力波传播的 PINN 框架

- 中文标题：用于双材料体系弹性动力波传播的 Physics-Informed Neural Network 框架
- 原始标题：A Physics-Informed Neural Network Framework for Elastodynamic Wave Propagation in Bimaterial Systems
- 作者：Sonal Ankush Chibire, Jenn-Terng Gau, Bo Zhang
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-07
- 中文摘要：论文将轴对称线弹性方程、初始条件、边界条件和材料界面条件嵌入 PINN loss，用于建模钢-铝双材料体系中的瞬态弹性动力波传播。研究以 Split Hopkinson Pressure Bar 类型结构为代表，并使用 ANSYS Workbench Explicit Dynamics 的高保真有限元结果进行验证和辅助训练。模型能够预测界面反射/透射、轴向与径向位移、面平均响应以及主要应力应变演化，并能泛化到未见时间点和修改后的材料属性。
- 原文链接：https://arxiv.org/abs/2607.06479
- 为什么匹配你的兴趣：直接连接 ANSYS、显式动力学、冲击/高应变率固体力学、有限元 surrogate 和损伤/疲劳前置问题。
- 入选说明：这是本周结构力学方向最贴近 CAE 工程仿真的论文之一。

## 5. 一维对流-扩散方程的质量守恒 PINN

- 中文标题：面向一维对流-扩散方程的质量守恒 PINN
- 原始标题：Mass-Conserving Physics-Informed Neural Networks For The One-Dimensional Advection-Diffusion Equation
- 作者：Eszra Forenita Sigalingging, Liu Kin Men, Setianto Setianto, Ferry Faizal
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-07
- 中文摘要：论文研究 PINN 在周期性一维对流-扩散方程中是否能长期保持全局质量守恒。作者比较 Vanilla PINN、带软质量守恒惩罚项的 Mass-Penalty PINN 和 Crank-Nicolson 格式，在不同 Peclet 数和短/长时间仿真区间上测试。结果显示，在长时间仿真中，质量守恒惩罚可以显著降低相对 L2 误差和质量漂移误差，改善幅度分别可达约 9-67 倍和 15-215 倍。
- 原文链接：https://arxiv.org/abs/2607.06091
- 为什么匹配你的兴趣：对流-扩散是 CFD、热传递、微流控、污染/粒子输运和样品输送建模的基础方程；守恒性是工程部署中 PINN 的关键短板。
- 入选说明：问题是一维 benchmark，工业复杂度有限，但它抓住了 PINN 用于守恒律仿真时最重要的可靠性问题。

## 6. 自动 CAD 生成的 foundation models

- 中文标题：用于自动 CAD 生成的 Foundation Models
- 原始标题：Foundation Models for Automatic CAD Generation
- 作者：J de Curtò, Victoria Guillén, I. de Zarzà
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-06
- 中文摘要：论文研究 LLM/VLM 从自然语言规格自动生成参数化 3D CAD 机械零件的能力。作者提出 LLMForge text-to-CAD 框架，结合 JSON schema 校验、解析式特征评分、mesh synthesis 和多轮迭代 refinement，并比较 IterTracer 和 IterVision 两种反馈机制。benchmark 包含 97 个工程设计问题，覆盖带孔板、复杂盒体、法兰圆柱和 L 型支架等几何族。实验评估七个 foundation model，并分析 watertight mesh、几何一致性和旋转对称结构的失败模式。
- 原文链接：https://arxiv.org/abs/2607.05573
- 为什么匹配你的兴趣：直接命中 AI for CAD、机械零件生成、CAD-to-CAE 前处理自动化和工程设计 workflow。
- 入选说明：对工业 CAD 生成很相关，但仍偏 benchmark 和自动建模，尚未直接验证下游 FEA/CFD 可用性。

## 7. PDEFlow：面向 Neural Operator 学习和无求解器推理的自动化 PDE agent 流水线

- 中文标题：PDEFlow：用于 Neural Operator 学习和无求解器推理的自主 agentic PDE 流水线
- 原始标题：PDEFlow: Autonomous Agentic PDE Pipelines for Neural Operator Learning and Solver-Free Inference
- 作者：Akshat Jani, Prathamesh Gadekar, Sakhinana Sagar Srinivas, Venkataramana Runkana
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-06
- 中文摘要：论文提出 PDEFlow，将自然语言或用户级 ODE/PDE 描述转化为 solver-backed neural-operator pipeline。系统包括问题规格解析、参数采样、基于 FEniCSx 有限元后端的数据生成、operator 训练、checkpoint 管理和无求解器推理。当前实现使用 multi-branch Bayesian DeepONet，并在多个 ODE/PDE benchmark 上展示可以生成有效规格、自动产生仿真数据、训练 neural operator，并在保存的 checkpoint 上做快速预测。
- 原文链接：https://arxiv.org/abs/2607.05134
- 为什么匹配你的兴趣：它把 LLM/agent、FEniCSx、PDE 仿真数据生成和 neural operator 连接起来，接近“CAE 自动化流水线”而不是单个模型。
- 入选说明：工程潜力很高；需要后续观察它在真实复杂几何、网格质量和工业边界条件下的鲁棒性。

## 8. CoFINN：面向守恒律物理问题的 Conservation Flux Informed Neural Networks

- 中文标题：CoFINN：用于守恒律物理问题的 Conservation Flux Informed Neural Networks
- 原始标题：CoFINN: Conservation Flux Informed Neural Networks for Physics Problems Governed by Conservation Laws
- 作者：Adnan Harun Doğan, Mert Deniz, Hande Alemdar, Özgür Uğraş Baran
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-05
- 中文摘要：论文提出 CoFINN，用有限体积视角把守恒律物理直接嵌入 CNN surrogate 的训练。与只优化像素误差的普通 CNN 不同，CoFINN 将输出场解释为结构化计算网格上的有限体积单元，并通过数值通量计算施加守恒一致性。论文在跨声速翼型流场预测中评估方法，工况为 Mach 0.7、Re = 6e6，并覆盖激波和高攻角情况。结果显示 CoFINN 能降低气动力预测误差，极端攻角下阻力误差最多降低 34%，平均约降低 15%。
- 原文链接：https://arxiv.org/abs/2607.06587
- 为什么匹配你的兴趣：这是非常直接的 CFD surrogate 论文，尤其关心有限体积一致性、跨声速翼型、气动力预测和有限数据情形。
- 入选说明：本周 CFD 方向优先级很高；它比纯黑箱 CNN 更接近工程 CFD 的数值结构。

## 9. 通过 PINN solver-agnostic 训练实现跨钝体形状泛化的湍流闭合

- 中文标题：通过 PINN solver-agnostic 训练实现跨钝体形状泛化的湍流闭合
- 原始标题：Generalizable turbulence closures across bluff-body shapes by PINN-based solver-agnostic training
- 作者：Zhen Zhang, Theo Käufer, Louise Ronglan, Michael S. Triantafyllou, George Em Karniadakis
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-05
- 中文摘要：论文提出一种不把 CFD solver 放入优化循环的湍流闭合训练方法。作者在 PINN 中施加 RANS residual，使逆问题变成 mesh-free、可微且 solver-agnostic，从而快速筛选不同闭合形式。论文开发了四类闭合模型，包括 Reynolds stress tensor basis、带输运湍动能的非局部模型、学习长度尺度模型，以及直接建模 Reynolds force 的模型。它们在六个 2D 钝体尾流、Re = 10^4 上训练，并冻结后部署到有限元求解器中，在 leave-one-shape-out 测试中改善速度场和阻力预测。
- 原文链接：https://arxiv.org/abs/2607.04491
- 为什么匹配你的兴趣：直接面向 CFD turbulence closure、有限元部署、solver-agnostic 学习和工程流动泛化。
- 入选说明：比一般 PINN benchmark 更接近真实 CFD 建模痛点，尤其适合跟踪 OpenFOAM/Fluent/自研 solver 闭合模型路线。

## 10. 基于 ASTEC 的核反应堆严重事故深度学习 surrogate

- 中文标题：基于 ASTEC 的核反应堆严重事故深度学习 surrogate 模型
- 原始标题：A Deep Learning-based surrogate model for Severe Accidents in nuclear reactors using ASTEC
- 作者：Alessandro Longhi, Danny Lathouwers, Zoltán Perkó
- 作者单位：arXiv 页面未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv
- 发布日期：2026-07-05
- 中文摘要：论文面向核反应堆严重事故仿真，构建 ASTEC 的深度学习 surrogate。原始 ASTEC 仿真一次可能需要数天，不适合实时训练或应急操作支持。作者将 AutoEncoder 降维与 Neural ODE 时间推进结合，训练数据来自站 blackout 和 loss-of-coolant accident 等事故场景下的 operator action 采样。模型同时预测 ASTEC vessel domain 中约 80 个热工水力、堆芯退化和裂变产物释放相关变量，并可稳定 autoregressive rollout 到 5 万步；AutoEncoder 实现超过 300 倍降维，可在 CPU/GPU 上一分钟内预测约 40 小时事故演化。
- 原文链接：https://arxiv.org/abs/2607.04450
- 为什么匹配你的兴趣：这是典型工业/安全关键仿真 surrogate，涉及多物理场、长时间 rollout、实时模拟器和工程决策支持。
- 入选说明：不是你列出的光学/XFEL/流体喷嘴窄方向，但“复杂工业仿真代码 + DL surrogate”的架构价值很高。

## 本周排除但值得留意的条目

- Approximate Dynamic Optimization via Deep Neural Operators：https://arxiv.org/abs/2607.03861。该文发表于 2026-07-04，面向化工过程动态优化和温度程序，相关性不错；本周因最终清单优先保留 2026-07-05 之后更贴近 CAE/CFD/FEA 的条目而未列入前 10。
- Evaluating RAG Metrics in Applied Contexts：https://arxiv.org/abs/2607.07302。它对工业 RAG 评估有用，但不是工程仿真/CAE 论文，本周作为方法背景观察，不进入主清单。
- Accelerating Industrial Finite Element Simulations of Electric Machines based on Runtime Analysis：https://arxiv.org/abs/2607.07514。工业 FEA 相关性强，但 AI/ML 成分不明确，故未进入 AI-for-CAE 主清单。
- Siemens、Rescale、Synera、COMSOL、Neural Concept 的多条本地日志线索反映了工业 AI/CAE 产品趋势，但没有论文级元数据或正式研究贡献，本周不作为论文收录。

## 下周我会怎么调整

下周应继续保留 arXiv-first 检索，同时加强 Crossref、Semantic Scholar、publisher online-first 页面和会议 proceedings 的查重。窄主题方面，本周没有强匹配的光学镜面 coating damage、heat-load simulation of optical components、XFEL/同步辐射仪器机械设计、液体 sheet jet、低温液氢/液氮、nozzle optimization、OpenFOAM/Fluent/COMSOL 实名工具链论文，下周需要更窄的 query 和更长的回看窗口。

建议下周追加这些 watchlist queries：`synchrotron mirror coating damage machine learning simulation`、`XFEL instrument mechanical design simulation AI`、`optical component heat load neural surrogate`、`liquid sheet jet nozzle optimization machine learning CFD`、`cryogenic liquid hydrogen CFD surrogate neural operator`、`OpenFOAM physics-informed graph neural network turbulent flow`、`Fluent COMSOL neural surrogate heat transfer`、`microfluidic sample delivery neural operator`、`RAG CAE simulation report generation evaluation`。
