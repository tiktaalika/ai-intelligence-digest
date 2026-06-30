# AI for CAE Paper Watch - 2026-06-05

## Search Meta

- Search run UTC: 2026-06-05T07:05:08Z
- Intended freshness window: last 24-48 hours for newly posted or newly indexed items
- Dedup baseline checked:
  - `data/digests/2026-06-03-candidates.json`
  - `data/digests/2026-06-04-candidates.json`
- Net-new additions logged here: 7
- Important note:
  - Strong primary-paper matches posted strictly on 2026-06-03 to 2026-06-05 were sparse for the requested CAE subtopics.
  - This pass therefore includes a mix of:
    - recently posted papers from late April to late May 2026 that are highly relevant, and
    - older 2026 papers that appear to have been newly indexed or resurfaced in search during the last 24-48 hours.

## Sources Checked

- arXiv
- Nature / Communications Physics / Nature Computational Science
- Copernicus / Wind Energy Science preprints
- Crossref / Crossmark DOI records
- Semantic Scholar result pages
- Secondary discovery surfaces used only for recall, then normalized back to primary paper pages where possible:
  - AlphaXiv-style mirrors
  - papers.cool

## Query Families Used

- `site:arxiv.org/abs (CFD OR OpenFOAM OR Fluent OR COMSOL OR microfluidic OR nozzle OR MBSE OR generative design OR fatigue) (AI OR "machine learning" OR "neural operator" OR surrogate)`
- `site:arxiv.org/abs 2606 CFD machine learning`
- `site:arxiv.org/abs 2606 engineering simulation AI`
- `site:nature.com neural operator finite element method 2026`
- `site:crossmark.crossref.org/dialog microfluidics machine learning 2026`
- `site:wes.copernicus.org/preprints surrogate fatigue simulation machine learning 2026`
- `site:arxiv.org/abs RAG engineering industry requirements 2026`

## Candidate Entries

### 1) Accelerating Bayesian inverse design in computational fluid dynamics using neural operators

- 中文标题: 使用神经算子加速计算流体力学中的贝叶斯逆向设计
- Authors: Bipin Tiwari; Omer San
- Affiliations: not surfaced in the search snippet
- Publication / preprint date: 2026-05-25
- Primary links:
  - arXiv abs: <https://arxiv.org/abs/2605.26059>
- Original abstract:
  - Bayesian inverse design provides a principled framework for inferring aerodynamic geometries from sparse flow observations while quantifying uncertainty. However, its practical use in computational fluid dynamics (CFD) is severely limited by the cost of repeated high-fidelity simulations required for gradient-based Markov chain Monte Carlo (MCMC) sampling. While surrogate models are commonly proposed to reduce this cost, their effect on posterior geometry and uncertainty, especially for shock-dominated flows, remains poorly understood. In this work, we demonstrate that neural operator surrogates can be embedded directly within the MCMC inference loop while preserving posterior structure. Using a fully Bayesian inverse formulation of quasi-one-dimensional nozzle flow, we demonstrate that geometry parameterization plays a decisive role in identifiability and posterior conditioning, with cubic B-splines yielding stable and physically meaningful uncertainty estimates. Building on this formulation, a Deep Operator Network trained on CFD-generated data is substituted for the CFD solver within a No-U-Turn Sampler, while keeping the likelihood model, priors, and sampling configuration unchanged. Across sparse to fully observed regimes, surrogate-based inference reproduces the posterior geometry and uncertainty trends of the CFD reference. As a result of surrogate integration, total inference time is reduced to under one second, corresponding to a speedup exceeding three orders of magnitude. In addition, a direct inverse neural operator is examined as a deterministic alternative for inverse design, enabling single-shot geometry reconstruction without posterior sampling. These results demonstrate that neural operator-accelerated Bayesian inference enables practical, uncertainty-aware inverse design workflows for aerodynamic applications.
- 中文摘要:
  - 论文把神经算子直接嵌入 CFD 贝叶斯逆设计采样环路，在一维喷嘴流问题上把高保真求解器替换为 Deep Operator Network，同时尽量保持后验结构与不确定性趋势。作者报告总推断时间降到 1 秒以内，速度提升超过三个数量级，并比较了可直接单次预测几何形状的逆向神经算子方案。对 CAE 的意义在于，它把“带不确定性约束的设计优化”从离线研究推进到了接近实时可用。
- Relevance notes:
  - Direct hit for CFD, nozzle design and optimization, surrogate modeling, uncertainty-aware design.
  - Good weekly-briefing candidate because it is methodologically strong and close to industrial inverse-design workflows.
- Exclusion / uncertainty notes:
  - Freshness is outside the strict last-48h window, but still recent and not present in prior local digests.

### 2) Hybrid Fourier Neural Operator-Lattice Boltzmann Method

- 中文标题: 混合式傅里叶神经算子-格子玻尔兹曼方法
- Authors: Alexandra Junk; Josef M. Winter; Meike Tütken; Steffen Schmidt; Nikolaus A. Adams
- Affiliations: not surfaced in the search snippet
- Publication / preprint date: 2026-04-29
- Primary links:
  - arXiv abs: <https://arxiv.org/abs/2604.27158>
- Original abstract:
  - We propose an accelerated computational fluid dynamics framework based on a hybrid Fourier Neural Operator-Lattice Boltzmann Method (FNO-LBM) for steady and unsteady weakly compressible flows. FNO-based initialization significantly accelerates LBM in reaching steady-states of porous media flows across all macroscopic fields, achieving up to 70% speed-up in convergence of density and more than 40% of pressure-drop while preserving the final steady-state accuracy. Simulations of unsteady flows can be accelerated by hybrid coupling strategies that employ FNO rollouts embedded into LBM time advancement in a way of super-time-stepping. Global and time-resolved error metrics across 100 trajectories for generic 2D flows demonstrate that hybridization consistently improves accuracy and stabilizes long-horizon rollouts. Best efficiency is achieved for a lightweight 2.6M-parameter FNO, which diverges under pure autoregressive rollout but achieves 96-99.8% error reduction under hybrid coupling, matching the predictive capability of a much more expensive 11.2M-parameter model. The hybrid framework enhances predictive fidelity, suppresses error accumulation, and enables small and cheap surrogate models to operate effectively within the same error regime as larger surrogates. These results demonstrate that hybrid neural-operator coupling achieves robust and computationally efficient accelerated LBM while maintaining physically consistent flow evolution.
- 中文摘要:
  - 这篇工作不是单纯拿 AI 替代 CFD，而是把 FNO 与 LBM 混合耦合，用神经算子做初始化和部分时间推进，从而同时获得加速与数值稳定性。作者在多孔介质稳态流和二维非稳态流上报告了明显收敛加速，并指出小模型在混合耦合后也能进入大模型的误差区间。对 CAE/CFD 社区来说，这类“AI in the solver loop”比纯黑盒代理更接近可落地路径。
- Relevance notes:
  - Strong fit for CFD algorithm acceleration and solver-ML hybridization.
  - Useful for OpenFOAM/Fluent/industrial-solver watchers even though the implementation is LBM-based.
- Exclusion / uncertainty notes:
  - Not in the strict 48h posting window.
  - No explicit OpenFOAM / Fluent connection in the surfaced metadata.

### 3) NOEM: efficient and scalable finite element method enabled by reusable neural operators

- 中文标题: NOEM：由可复用神经算子驱动的高效可扩展有限元方法
- Authors: Weihang Ouyang; Yeonjong Shin; Si-Wei Liu; et al.; Lu Lu
- Affiliations: not fully surfaced in the search snippet
- Publication / preprint date: 2026-04-28
- Primary links:
  - Nature Computational Science: <https://www.nature.com/articles/s43588-026-00974-2>
  - DOI: <https://doi.org/10.1038/s43588-026-00974-2>
  - arXiv preprint: <https://arxiv.org/abs/2506.18427>
- Original abstract:
  - The finite element method (FEM) is a well-established numerical method for solving partial differential equations (PDEs). However, its mesh-based nature gives rise to substantial computational costs, especially for complex multiscale simulations. Emerging machine learning-based methods provide data-driven solutions to PDEs, yet they present challenges, including high training cost and low model reusability. Here we propose the neural-operator element method (NOEM) by synergistically combining FEM with operator learning to address these challenges. NOEM leverages neural operators to simulate subdomains that require fine meshes in FEM. In each subdomain, a neural operator is used to build a single element, namely, a neural-operator element (NOE). NOEs are then integrated with standard finite elements to represent the entire solution through the variational framework. Thereby, NOEM does not necessitate dense meshing and offers efficient simulations. We demonstrate the accuracy, efficiency and scalability of NOEM by performing systematic theoretical analysis and numerical experiments, such as nonlinear PDEs, multiscale problems, PDEs on complex geometries and discontinuous coefficient fields.
- 中文摘要:
  - 论文提出把神经算子当作有限元中的“元素”来使用，在需要细网格的子域内用神经算子元件替代传统细网格求解，再通过变分框架和普通有限元拼接。这样做的重点不是泛泛的 AI 加速，而是提高可复用性与多尺度复杂几何场景下的扩展性。对结构、传热、多物理场 CAE 来说，这是非常值得持续跟踪的方法论方向。
- Relevance notes:
  - Core CAE / PDE / FEM relevance.
  - Strong bridge paper between classical numerical methods and reusable operator-learning components.
- Exclusion / uncertainty notes:
  - Not newly posted in the last 48h.
  - Included because it is a high-signal 2026 paper absent from prior local logs and likely briefing-worthy.

### 4) Discontinuous Galerkin finite element operator network for solving non-smooth PDEs

- 中文标题: 用于求解非光滑偏微分方程的不连续伽辽金有限元算子网络
- Authors: Kapil Chawla; Youngjoon Hong; Jae Yong Lee; Sanghyun Lee
- Affiliations: not surfaced in the primary snippet
- Publication / preprint date: 2026-01-07
- Primary links:
  - arXiv abs: <https://arxiv.org/abs/2601.03668>
- Discovery note:
  - A secondary index surfaced a fresh crawl of the PDF 2 days before this run, which is why it is logged here despite the older arXiv posting date.
- Original abstract:
  - We introduce Discontinuous Galerkin Finite Element Operator Network (DG-FEONet), a data-free operator learning framework that combines the strengths of the discontinuous Galerkin (DG) method with neural networks to solve parametric partial differential equations (PDEs) with discontinuous coefficients and non-smooth solutions. Unlike traditional operator learning models such as DeepONet and Fourier Neural Operator, which require large paired datasets and often struggle near sharp features, our approach minimizes the residual of a DG-based weak formulation using the Symmetric Interior Penalty Galerkin (SIPG) scheme. DG-FEONet predicts element-wise solution coefficients via a neural network, enabling data-free training without the need for precomputed input-output pairs. We provide theoretical justification through convergence analysis and validate the model's performance on a series of one- and two-dimensional PDE problems, demonstrating accurate recovery of discontinuities, strong generalization across parameter space, and reliable convergence rates. Our results highlight the potential of combining local discretization schemes with machine learning to achieve robust, singularity-aware operator approximation in challenging PDE settings.
- 中文摘要:
  - 这篇工作把 DG 弱形式残差和神经网络结合起来，做出一种无需大量配对训练数据的算子学习框架，重点处理不连续系数和非光滑解。相比常见 DeepONet/FNO，作者强调它对尖锐特征和间断问题更稳健。对材料界面、接触、裂纹、复杂边界条件等 CAE 问题，这类“面向奇异性/间断”的 operator learning 很值得关注。
- Relevance notes:
  - High theoretical relevance for FEM, PDEs, non-smooth mechanics / multiphysics settings.
- Exclusion / uncertainty notes:
  - Not a new paper by posting date.
  - Newly indexed / resurfaced signal came from a secondary index, not from the primary arXiv page itself.

### 5) Physics-based machine learning toolbox for probing concentration under diffusive regime in microfluidics devices

- 中文标题: 面向微流控器件扩散主导浓度探测的物理约束机器学习工具箱
- Authors: Ryan Santoso; Yuankai Yang; Mara Lönartz; Jenna Poonoosamy
- Affiliations: not surfaced in the snippet
- Publication / preprint date: 2026-03-21
- Primary links:
  - Publisher page: <https://www.nature.com/articles/s42005-026-02590-y>
  - DOI: <https://doi.org/10.1038/s42005-026-02590-y>
- Original abstract:
  - Microfluidics experiments offer high-resolution insights into transport and chemical processes in porous media, yet direct measurement of evolving concentration profiles remains challenging. Numerical simulations can serve as virtual probes but are labor-intensive and computationally expensive. Here, we develop a physics-based machine learning toolbox that transforms such simulations into efficient and scalable virtual probes. Central to our toolbox is the non-intrusive reduced basis method, supported by the U-Net and the Convolutional Autoencoder, which learns mappings from experimental images and physical parameters to concentration profiles. By incorporating physics into its construction, the toolbox delivers accurate predictions with a limited number of training samples. Applied to two microfluidics experiments with different base patterns, the toolbox predicts spatio-temporal concentration profiles, effective diffusivities, and locations with a high probability of precipitation. This paves the way for digital twins that enable real-time analysis and tuning of experiments on the fly.
- 中文摘要:
  - 论文把 U-Net、卷积自编码器和非侵入式降阶基方法组合成一个微流控数字孪生工具箱，用于从实验图像快速推断浓度场、有效扩散率和高概率沉淀位置。它的核心价值在于把昂贵数值模拟变成“可实时调用的虚拟探针”，而不是仅做黑盒回归。对样品输运、孔隙介质、反应流和微流控实验在线调参都很贴近。
- Relevance notes:
  - Strong match for microfluidic flow, sample-delivery-adjacent transport analysis, and digital-twin style simulation assistance.
- Exclusion / uncertainty notes:
  - Publication date is March 2026, so this is a backlog catch-up item rather than a fresh posting.

### 6) Gaussian process surrogate modeling for efficient controller tuning and fatigue load prediction of the helix wake-mixing method

- 中文标题: 用于螺旋尾流混合方法高效控制调参与疲劳载荷预测的高斯过程代理建模
- Authors: Daan van der Hoek; Tim Dammann; Jan-Willem van Wingerden
- Affiliations: not surfaced in the snippet
- Publication / preprint date: 2026-04-14
- Primary links:
  - Copernicus preprint page: <https://wes.copernicus.org/preprints/wes-2026-62/>
  - DOI: <https://doi.org/10.5194/wes-2026-62>
- Original abstract excerpt:
  - Wind farms experience reduced power production and elevated structural loading due to wake interactions. Wake-mixing control techniques, which dynamically excite upstream turbine wakes to accelerate recovery, have demonstrated promising improvements in downstream power production but at the expense of increased fatigue loading. Identifying the optimal control settings and quantifying the resulting load implications remain challenging because these methods require high-fidelity simulations that capture both the dynamic actuation and the resulting turbulence. This study presents two complementary advances to improve the design of wake-mixing strategies using a limited number of large-eddy simulations (LES) and Gaussian process (GP) regression.
- 中文摘要:
  - 论文利用有限数量 LES 数据和 GP 代理模型，一方面搜索尾流混合控制参数，另一方面预测相应疲劳载荷，目标是在发电收益和结构寿命之间做更快的设计权衡。虽然应用场景是风电，但方法论对“高保真仿真 + 代理模型 + 疲劳/载荷评估”这一 CAE 组合非常典型。对 damage and fatigue 方向属于直接相关候选。
- Relevance notes:
  - Strong fit for fatigue, surrogate modeling, high-fidelity simulation reduction.
- Exclusion / uncertainty notes:
  - Domain is wind energy rather than the user’s core CAD/CFD stack.
  - Still worth tracking because it is one of the cleaner 2026 examples of surrogate-assisted fatigue prediction.

### 7) An Industrial-Scale Retrieval-Augmented Generation Framework for Requirements Engineering: Empirical Evaluation with Automotive Manufacturing Data

- 中文标题: 面向需求工程的工业级检索增强生成框架：基于汽车制造数据的实证评估
- Authors: Muhammad Khalid; Yilmaz Uygun
- Affiliations: not surfaced in the snippet
- Publication / preprint date: 2026-03-20
- Primary links:
  - arXiv abs: <https://arxiv.org/abs/2603.20534>
- Original abstract excerpt:
  - Requirements engineering in Industry 4.0 faces critical challenges with heterogeneous, unstructured documentation spanning technical specifications, supplier lists, and compliance standards. While retrieval-augmented generation (RAG) shows promise for knowledge-intensive tasks, no prior work has evaluated RAG on authentic industrial RE workflows using comprehensive production-grade performance metrics. This paper presents a comprehensive empirical evaluation of RAG for industrial requirements engineering automation using authentic automotive manufacturing documentation.
- 中文摘要:
  - 这篇论文严格来说不属于仿真算法，但和工程工具链、需求工程、可追溯性、汽车工业文档工作流高度相关。作者用真实汽车制造文档评估工业级 RAG 在需求抽取与追踪中的效果，并报告了较强的准确率、可追溯性和时间节省。若周报想加入“RAG 在工业工程中的真实落地信号”，它是一个可保留但优先级略低的候选。
- Relevance notes:
  - Useful for the user’s “RAG in industry” / engineering process intelligence watchlist.
- Exclusion / uncertainty notes:
  - Lower-confidence fit versus the core CAE/simulation theme.
  - Keep only if the weekly briefing wants one process/toolchain item alongside physics/simulation papers.

## Excluded / Weak-Match Areas This Run

- No convincing fresh primary-paper hits were found in this pass for:
  - heat-load simulation of optical components
  - coating damage of optical mirrors
  - synchrotron instrument mechanical design and simulation
  - XFEL instrument design and simulation
  - liquid hydrogen / liquid nitrogen nozzle optimization specifically tied to AI + CAE
  - explicit OpenFOAM / Fluent / COMSOL new papers posted in the last 48 hours
- Several results were product / blog / company announcements rather than papers and were not logged here.

## Suggested Weekly-Briefing Shortlist Seed

- Highest priority:
  - `Accelerating Bayesian inverse design in computational fluid dynamics using neural operators`
  - `Hybrid Fourier Neural Operator-Lattice Boltzmann Method`
  - `NOEM: efficient and scalable finite element method enabled by reusable neural operators`
- Secondary:
  - `Physics-based machine learning toolbox for probing concentration under diffusive regime in microfluidics devices`
  - `Gaussian process surrogate modeling for efficient controller tuning and fatigue load prediction of the helix wake-mixing method`
  - `Automotive Engineering-Centric Agentic AI Workflow Framework`
