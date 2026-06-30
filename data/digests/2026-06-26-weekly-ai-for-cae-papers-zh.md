# 2026-06-26 每周 AI for CAE 论文简报

## 本周我做了什么

本次检索覆盖 2026-06-19 至 2026-06-26（欧洲/柏林时间周五上午收口），并额外补查了 2026-06-24 至 2026-06-26 的最近 24-48 小时 arXiv 新提交，避免漏掉周四晚和周五早上的论文。

我先读取了本地 daily watch 任务生成的候选日志：`data/digests/2026-06-20-candidates.json`、`2026-06-21-candidates.json`、`2026-06-22-candidates.json`、`2026-06-24-candidates.json`、`2026-06-25-candidates.json`、`2026-06-26-candidates.json`。本周本地日志合计抓取 2254 条、过滤后 552 条、显式重复 8 条。和上周类似，本地 CAE/engineering AI 候选主要是 Siemens Simcenter、Virtual Twin、Physical AI、CAD-embedded CFD 等工业新闻或产品更新，适合作为趋势线索，但大多数不是论文，因此没有直接进入论文榜单。

随后我做了新鲜论文检索，重点检查 arXiv API、arXiv paper pages、搜索引擎返回的 arXiv/Semantic Scholar/Crossref/publisher 线索。实际可稳定核验并适合本周时效的主要来源是 arXiv；本轮没有发现比 arXiv 更可靠、且发布日期落在本周窗口内的 DOI/publisher-first 论文可以替代入选条目。查询族包括：`surrogate / neural operator / PINN / physics-informed / machine learning + CFD / finite element / simulation / engineering`，`CFD / fluid / free-surface / droplet / nozzle / microfluidic + surrogate / neural / operator learning`，`CAD / generative design / topology optimization / inverse design + AI / neural / LLM / agent`，`LLM / RAG / agent + engineering / simulation / CAD / systems engineering`，`damage / fatigue / fracture / solid mechanics + neural / PINN / surrogate`，`thermal / heat / convection / HVAC + surrogate / neural / physics-informed`，以及 `OpenFOAM / Fluent / COMSOL / Ansys / FEniCSx + AI / simulation`。

arXiv 结构化检索得到 249 个唯一条目，其中 190 个落在本周窗口内；经过严格关键词与人工语义过滤后，保留 33 个论文级候选。去重按 arXiv ID、标题标准化和主题重复进行；排除了泛 LLM、推荐系统、计算机视觉生成、医疗影像、金融、软件工程、通用机器人和只含“simulation”泛词但没有 CAE/工程仿真内容的条目。作者单位方面，arXiv API 和可访问摘要页通常不稳定提供 affiliation，因此本简报只在可见时填写；本次 10 篇均未在可用元数据中稳定列出单位。局限是：Semantic Scholar/Crossref 对当天新 arXiv 条目的索引可能滞后；部分论文尚无 DOI；出版社正式版本如果稍后上线，需要下周再补。

## 筛选标准

我优先考虑五个维度：第一是时效，优先 2026-06-24 至 2026-06-25 的新提交，其次覆盖 6 月 21-23 日的强相关论文；第二是与 CAE/工程仿真的直接关系，明确涉及 PDE、CFD、有限元、热传导、断裂、损伤诊断、自由表面流、路径依赖应力场、仿真 surrogate 或工程控制；第三是来源质量，优先 arXiv 原始论文页、可下载 PDF 和清晰摘要；第四是工程可用性，优先能落到 COMSOL/FEniCSx、PFEM、VOF、EnergyPlus/OpenModelica、有限元、结构健康监测等真实工程流程的论文；第五是主题多样性，避免 10 篇都集中在同一种 neural operator 或同一种 CFD benchmark。

本周没有强行纳入光学镜面 coating damage、synchrotron/XFEL instrument mechanical design、OpenFOAM/Fluent/nozzle-specific 的新论文，因为没有找到足够新的可信论文级匹配。与这些方向相邻的入选条目包括微纳尺度热传导、自然对流、自由表面/液滴动力学、结构损伤和相场断裂。

## 1. 误差条件化神经求解器

- 中文标题：误差条件化神经求解器
- 原始标题：Error-Conditioned Neural Solvers
- 作者：Haina Jiang; Liam Wang; Peng-Chen Chen; Min Seop Kwak; Seungryong Kim; Brian Bell; Jeong Joon Park
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，cs.LG/cs.AI/cs.CV/math.NA
- 发布日期：2026-06-25
- 中文摘要：论文指出，常见神经 surrogate 虽然能快速从 PDE 参数映射到解，但通常把求解视为统计预测，难以自我修正约束违反和分布外误差。作者认为，在病态系统中单纯最小化 PDE residual 并不总能代表重构精度，因此提出 Error-Conditioned Neural Solvers，把 residual field 作为每轮迭代的直接输入，让网络读取自身误差的空间结构并学习修正策略。该方法在四类 PDE 上多数设置取得最高精度，在 turbulent Kolmogorov flow 上最高达到 10 倍增益，并能在参数变化、跨方程迁移等分布偏移下保持优势。
- 原文链接：https://arxiv.org/abs/2606.27354v1；PDF：https://arxiv.org/pdf/2606.27354v1
- 为什么匹配兴趣：它直接讨论 PDE surrogate、神经求解器和 residual-based hybrid 方法的可靠性，对工程仿真 surrogate 的理论选择很关键。
- 入选说明：新、理论相关度高，适合作为本周第一优先；不足是工程案例还偏 benchmark，尚未绑定具体 CAE 软件。

## 2. 基于多保真卷积自编码器迁移学习的导波损伤诊断

- 中文标题：基于多保真卷积自编码器迁移学习的导波损伤诊断框架
- 原始标题：A Multi-Fidelity Convolutional Autoencoder-Transfer Learning Framework for Guided-Wave-Based Damage Diagnosis Using Large Simulated and Limited Experimental Datasets
- 作者：Santosh Kapuria; Abhishek
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，cs.LG
- 发布日期：2026-06-25
- 中文摘要：论文面向带压电传感器的板状结构导波结构健康监测，解决真实标注实验数据少、高保真仿真数据昂贵的问题。方法用轻量物理仿真生成大规模合成数据，结合卷积自编码器深度特征学习、前馈神经网络和少量实验测量进行迁移学习，实现损伤定位和尺寸估计。作者使用一维时域谱元模型生成预训练数据，随后迁移到实验域；结果显示，CAE-based transfer learning 的定位精度优于 CNN 对照，定位 R² 超过 0.93、尺寸估计 R² 超过 0.99，并能泛化到预训练和微调中未出现的损伤情形。
- 原文链接：https://arxiv.org/abs/2606.27304v1；PDF：https://arxiv.org/pdf/2606.27304v1
- 为什么匹配兴趣：直接覆盖 damage、结构健康监测、有限实验数据和仿真数据结合，是工程结构损伤诊断的 AI-for-CAE 应用。
- 入选说明：应用明确、工程价值高；不是 CFD/热方向，但补足本周损伤与疲劳相关覆盖。

## 3. 用混合 IFENN 求解器建模相场断裂起裂与扩展

- 中文标题：用于可泛化相场断裂起裂与扩展建模的混合 IFENN 求解器
- 原始标题：A hybrid IFENN solver for generalizable modeling of phase-field fracture initiation and propagation
- 作者：Panos Pantidis; Fouad Amin; Diab Abueidda; Mostafa E. Mobasher
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，cs.CE
- 发布日期：2026-06-25
- 中文摘要：论文展示 Integrated Finite Element Neural Network（IFENN）如何模拟相场断裂从起裂到扩展的全过程。IFENN 将标准 FEM 求解器用于力学平衡，并用预训练神经网络近似耦合场：起裂阶段使用带 Kolmogorov-Arnold trunk/branch 的 DeepONet，扩展阶段使用 CNN。网络只在一个 benchmark 几何上训练一次，采用基于最大应变能和相场变量的 physics-informed 策略，并只使用少量增量和断裂过程区内少量 Gauss 点，从而降低离线训练成本。作者还用人工边界条件处理远离裂尖区域的 extrapolation，展示了对训练几何和未见几何的精度与灵活性。
- 原文链接：https://arxiv.org/abs/2606.27177v1；PDF：https://arxiv.org/pdf/2606.27177v1
- 为什么匹配兴趣：直接属于有限元、断裂、损伤和混合 AI-CAE 求解器。
- 入选说明：本周结构力学方向最强条目之一；优先级高于更泛的材料 ML。

## 4. 带 surrogate likelihood guidance 的潜空间扩散后验采样

- 中文标题：用于 PDE 逆问题的带代理似然引导潜空间扩散后验采样
- 原始标题：Latent Diffusion Posterior Sampling with Surrogate Likelihood Guidance for PDE Inverse Problems
- 作者：Yuanzhe Wang; Alexandre M. Tartakovsky
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，cs.CE/cs.LG
- 发布日期：2026-06-25
- 中文摘要：论文提出 L-DPS，一个面向 PDE 约束高维逆问题的近似贝叶斯框架。方法结合 VAE、无条件潜空间扩散模型、diffusion posterior sampling 和可微神经 surrogate：VAE 将空间参数场映射到低维潜空间，扩散模型学习隐式先验，似然梯度通过 decoder-surrogate 组合计算，从而避免反复调用完整 PDE 数值求解器。作者在 Darcy flow 逆问题中，从稀疏含噪压力观测反演空间渗透率场；结果显示 L-DPS 在稀疏和噪声场景下比 conditional latent diffusion、inverse FNO 等 amortized inverse baseline 更稳健，同时降低推理成本。
- 原文链接：https://arxiv.org/abs/2606.26592v1；PDF：https://arxiv.org/pdf/2606.26592v1
- 为什么匹配兴趣：覆盖 PDE 逆问题、surrogate forward model、贝叶斯不确定性和工程参数识别。
- 入选说明：对设计反演、材料/流体参数识别有方法论价值；工程案例目前是 Darcy flow benchmark。

## 5. 基于声子 Boltzmann 方程的 MC-PINN 反演多尺度热传导

- 中文标题：通过声子 Boltzmann 传输方程求解反演多尺度热传导问题的 Monte Carlo PINN
- 原始标题：Monte Carlo physics-informed neural networks for inverse multiscale heat conduction problems via the phonon Boltzmann transport equation
- 作者：Qingyi Lin; Chuang Zhang; Xuhui Meng; Zhaoli Guo
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，physics.comp-ph/math.AP
- 发布日期：2026-06-24
- 中文摘要：论文关注微纳尺度热传导中从有限测量反演热场和热物性的问题。在这类问题中，经典 Fourier law 失效，需要声子 Boltzmann transport equation 描述非扩散传输。作者将 MC-PINN 从正问题扩展到反问题，处理两类任务：未知边界条件下从稀疏内部温度测量重构完整热场，以及同时反演 relaxation time 与热场。Monte Carlo mesh-free 采样让模型在 diffusive、transitional 和 ballistic regime 中统一处理，不需要预先知道 relaxation time。论文在准 1D、准 2D、3D benchmark 和真实 3D FinFET 结构上验证，显示在稀疏数据下优于纯数据驱动网络。
- 原文链接：https://arxiv.org/abs/2606.25793v1；PDF：https://arxiv.org/pdf/2606.25793v1
- 为什么匹配兴趣：与 heat-load simulation、热场反演、微纳热输运和高热载荷组件建模高度相关。
- 入选说明：对光学元件热载荷仿真有间接方法价值；不是专门 synchrotron/XFEL optics，但方向接近。

## 6. 用神经 surrogate 改进自然对流仿真

- 中文标题：用于自然对流问题仿真的神经代理方法
- 原始标题：A Neural Surrogate Approach for Simulating Natural Convection Problems
- 作者：Nurshat Menglik; Alex Shao; David Hyde
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，physics.comp-ph/physics.flu-dyn
- 发布日期：2026-06-24
- 中文摘要：论文用 Fourier neural operator 改进 Boussinesq flow model 对自然对流问题的预测。训练数据由低成本但较低精度的 Boussinesq 仿真和更昂贵、更高精度的 compressible flow 仿真配对构成。两类仿真均基于隐式 monolithic mixed FEM，并使用开源 FEniCSx 实现；结果用 COMSOL 和标准文献算例验证。以 compressible flow 作为高保真参考后，单次模型评估即可显著改善 Boussinesq 结果，所有 flow variables 的 SSIM 接近 1，MSE 降低 1 到近 3 个数量级；代码和数据开源。
- 原文链接：https://arxiv.org/abs/2606.25259v1；PDF：https://arxiv.org/pdf/2606.25259v1
- 为什么匹配兴趣：明确出现 COMSOL、FEniCSx、FEM、热-流耦合和 neural operator，是本周最贴近 CAE 工具链的论文。
- 入选说明：应用和工具链匹配度很高；发布日期略早于 6 月 25 日条目，但综合优先级很高。

## 7. 物理约束 Fourier-Wavelet Transformer 用于多尺度 CFD surrogate

- 中文标题：用于多尺度 CFD 代理建模的物理约束 Fourier-Wavelet Transformer
- 原始标题：A Physics-Informed Fourier-Wavelet Transformer for Multiscale Computational Fluid Dynamics Surrogate Modeling
- 作者：Somyajit Chakraborty; Ming Pan; Xizhong Chen
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，physics.flu-dyn/cs.LG
- 发布日期：2026-06-23
- 中文摘要：论文针对现有 CFD surrogate 更容易恢复全局流动模式、但难以捕捉局部多尺度结构的问题，提出物理约束 Fourier-wavelet transformer。方法结合 Fourier-wavelet 谱编码、基于 PDE residual diagnostics 的 physics-biased self-attention，以及 Masked Physics Prediction 和 Equation Consistency Prediction 自监督预训练。实验覆盖 cylinder wake 和 fluid-structure interaction 两个真实 benchmark，并与 spectral、transformer、operator-learning、PINN 类 baseline 对比。结果在 cylinder wake 上取得最佳综合精度，在 FSI benchmark 上的 normalized MSE 低于最强 baseline，并更好恢复 near-body、wake-core 和 far-wake 局部结构。
- 原文链接：https://arxiv.org/abs/2606.24696v1；PDF：https://arxiv.org/pdf/2606.24696v1
- 为什么匹配兴趣：直接是 CFD surrogate、PDE-informed attention、wake/FSI，对流体仿真和液体射流类问题有方法参考价值。
- 入选说明：强相关；但 benchmark 仍偏通用流动，尚未到 OpenFOAM/Fluent 工业案例。

## 8. 用 Vision Transformer 预测黏弹性液滴撞击动力学

- 中文标题：基于 Vision Transformer 的黏弹性液滴撞击动力学预测
- 原始标题：Prediction of Viscoelastic Droplet Impact Dynamics Using a Vision Transformer-Based Approach
- 作者：Diego A. de Aguiar; Cassio M. Oishi
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，physics.flu-dyn/cs.LG
- 发布日期：2026-06-22
- 中文摘要：论文研究固体表面上黏弹性液滴撞击的时间演化预测，这类问题与 spray cooling、inkjet printing、pharmaceutical processing 等应用有关。作者使用 VOF 方法得到的 volume fraction fields，训练 Video Vision Transformer（ViViT）预测液滴动力学。对于黏弹性流体，除 Reynolds 和 Weber 数外，还需要 solvent viscosity ratio 与 Weissenberg number，导致仿真成本上升。该方法只用仿真最初 10%-20% 的演化预测后续过程，较完整数值仿真降低约 80%-90% 成本，并能捕捉 spreading 和 bouncing regime，保持几何特征和结构相似性。
- 原文链接：https://arxiv.org/abs/2606.23940v1；PDF：https://arxiv.org/pdf/2606.23940v1
- 为什么匹配兴趣：虽然不是 liquid sheet jet 或 nozzle optimization，但它是液体/黏弹性流动、VOF、参数化流体仿真加速的近邻主题。
- 入选说明：用于补足 liquid jets/sample delivery/microfluidic flow 相关覆盖；优先级低于直接 CFD surrogate 论文。

## 9. 用注意力机制构建可扩展网格神经 surrogate 模拟自由表面流

- 中文标题：用于自由表面流可扩展网格神经代理的注意力机制
- 原始标题：Attention mechanism for scalable mesh-based neural surrogates of free-surface fluids
- 作者：Federico Lanteri; Massimiliano Cremonesi
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，cs.CE/cs.LG
- 发布日期：2026-06-22
- 中文摘要：论文面向基于 Particle Finite Element Method（PFEM）的自由表面流高保真仿真。PFEM 需要持续更新计算域并反复求解控制方程，非牛顿流体中的材料非线性进一步增加成本。作者提出基于 self-attention 的神经 surrogate，保留 PFEM 网格离散结构，用注意力机制建模节点交互和空间依赖，同时支持重网格、节点重分布、长期 rollout 稳定性，并可通过标准有限元算子重构应力等派生力学量。论文比较标准 self-attention 和线性 attention，在 2D/3D 自由表面 benchmark、演化几何、不同材料参数和非牛顿流体上显示出较好精度与可扩展性。
- 原文链接：https://arxiv.org/abs/2606.23251v1；PDF：https://arxiv.org/pdf/2606.23251v1
- 为什么匹配兴趣：自由表面流、非牛顿流体、PFEM、网格 surrogate 与液体样品输送/喷流问题有明显方法交集。
- 入选说明：不是最新一天，但主题和用户流体方向高度匹配，因此保留。

## 10. 面向集成电动车热管理的物理约束预测控制 benchmark

- 中文标题：面向集成电动车热管理的物理约束预测控制：开放、真实数据锚定 benchmark
- 原始标题：Physics-Informed Predictive Control for Integrated Electric-Vehicle Thermal Management: An Open, Real-Data-Anchored Benchmark
- 作者：Yifan Wang
- 作者单位：arXiv 可用元数据未稳定列出
- 来源/期刊/会议/预印本服务器：arXiv，eess.SY
- 发布日期：2026-06-21
- 中文摘要：论文提出 OpenEV-ThermoSciML，一个开放可复现的 BEV 热管理 benchmark，耦合电池电-热-老化模型、两节点乘员舱模型、热泵/HVAC 模型和 CO2/通风模型，并使用真实驾驶循环和真实天气数据。作者在 benchmark 上构建 physics-informed SciML surrogate，即名义物理先验加学习残差和守恒惩罚，在分布外 rollout 中优于黑箱和 Koopman surrogate。进一步的 shielded SciML MPC 在六个场景下相对规则控制器获得统计显著改进，例如真实热天 US06 行程中能耗降低 15%、舒适性 RMSE 降低 47%、峰值 CO2 降低 25%、电池热梯度降低 78%，并能迁移到独立导出的 OpenModelica 8-node co-simulation plant。
- 原文链接：https://arxiv.org/abs/2606.22529v1；PDF：https://arxiv.org/pdf/2606.22529v1
- 为什么匹配兴趣：覆盖热管理、多物理系统、surrogate、MPC、co-simulation 和工程控制，是 industrial AI for simulation 的实用案例。
- 入选说明：发布时间比其他条目略早，但 benchmark 和工程闭环价值高；不是 CAE 软件论文，因此排在第 10。

## 下周我会怎么调整

- 增加直接 arXiv API 查询中的 `physics.ins-det`、`physics.acc-ph`、`physics.optics`、`cond-mat.mtrl-sci` 过滤，专门追踪 synchrotron/XFEL instrument、optical components、mirror coating damage、thermal deformation 和 beamline mechanics。
- 将 `liquid sheet jet`、`sample delivery`、`nozzle optimization`、`cryogenic jet`、`liquid hydrogen`、`liquid nitrogen` 与 `OpenFOAM`、`Fluent`、`COMSOL` 组合成更窄 watchlist，因为本周泛 CFD 检索没有抓到足够直接的新论文。
- 对本地 daily watch 增加“paper-grade”识别，降低 Siemens/厂商新闻对周报候选池的占比；这些新闻仍保留为工业趋势，但不应挤占论文检索预算。
- 对当天新 arXiv 条目，在下周补查 Semantic Scholar、Crossref 和 DOI 状态；本周多数新论文尚无 DOI 或 publisher page。
- 继续保留以下 watchlist 查询：`OpenFOAM machine learning surrogate CFD arXiv`、`Fluent POD-NN surrogate digital twin`、`COMSOL neural operator heat transfer`、`XFEL instrument simulation machine learning`、`synchrotron mirror coating damage simulation AI`、`liquid sheet jet nozzle optimization machine learning CFD`、`microfluidic sample delivery neural surrogate`、`phase-field fracture neural operator finite element`。
