**历史研究文档。** 下文批准前状态及旧验证凭证由[Owner决策](LCB-01_OWNER_DECISIONS.zh-CN.md)和[当前关闭交接](LCB-01_CLOSURE_HANDOFF.zh-CN.md)替代；66-case科学结果保留为证据。当前verifier必须传入`--actual`全新重建结果，仅给candidate路径返回NOT_READY。

# LCB-01 View Factor 调查报告

日期：2026-09-22。**LCB-01 — READY FOR OWNER DECISION**。本次只有研究授权，没有生产实现、决策批准、P4 验收或全项目启动。

分支：`research/vf-lcb01-compatibility`；Base：`d5bc38ebd6ba853c4cec530e4787d1ab6168203d`；冻结 Reference：`ecbfc863657e239817603a43898ae173c7ccad9c`。P3 批准基线仍为 `c2bc8572a976279abacbcd1d4f9c460233785bdb`。Final commit 为包含本报告的提交；验证凭证另外记录实际被测 checkpoint。

## 判断与边界

Full 矩阵的缺陷属于 **Reference implementation bug**：带符号的遮挡公式依赖严格的 high/low 端点顺序，而浮点舍入后的水平子段不满足这一假设。本次扫描中 408 个明显为负的 PV→ground helper 结果，全部出现端点高度精确相等。互易回填传播负号，sky 残差随之大于正常值。修正不需要改变 Geometry。

对任务指定的七条 helper 路径整体分类为 **Mixed**：上述实现缺陷，加上 Fast 有限地面代理的定义域及数值局限。180° 时，一个 Fast 边排 helper 对朝上的背面返回地面 VF=`0.5`，取绝对值无法修正；中间排代理在其他角度也与有限地面交换量不同。这些发现分别记录，不与 Full 负值混淆，也不自动升级为已批准修正。

默认推荐采用 [DEV-028 候选](DEV-028_VIEW_FACTOR_ORIENTATION_CANDIDATE.zh-CN.md) 和 [CDR-008 候选](CDR-008_VIEW_FACTOR_VISIBILITY_HOTTEL_POLICY.zh-CN.md)：在原有有限 Geometry 上，依据实际法向和无遮挡射线定义 F，使用不依赖端点命名方向的可见域积分。Owner 批准偏差及准确候选对象后，才能把 corrected 值当作验收期望。不得直接对矩阵 clamp 或 abs。

## 首个分歧与可手算反例

`VF053` 对应 Approved Geometry `TILT_180`：3 排，宽/高 1m，gcr=0.5，轴方位180°，太阳天顶角45°，太阳/面方位270°，tilt=180°。所有 surface 记录与批准 payload 精确相同，包括索引、key、坐标和法向；见 `geometry-equality.json`。

| 字段 | 接收地面 ReferenceIndex 3 | 源 PV ReferenceIndex 28 |
|---|---|---|
| SurfaceKey | kind=ground, source=shadow, ground_element=0, cut_interval=3, row/side/segment=null, illumination=shaded | kind=pvrow, source=pvrow, row=0, side=front, segment=0, ground_element/cut_interval=null, illumination=illuminated |
| 坐标/m | [−1.4999999999999996,0] → [−0.4999999999999998,0] | [−0.5,1] → [0.5,1] |
| 长度/m | 0.9999999999999998 | 1 |
| 法向 | raw 为 null；物理地面法向 [0,1] | [1.1102230246251565e−16,−1] |

分支顺序如下：

1. `rotation=-180`、`tilted_to_left=false`；地面 cut point 的 x 为 `-8165619676597684`。该地面段在**实体 PV 排左侧**，却在**排延长线 cut point 右侧**。两种“右侧”不是同一概念；保留批准坐标和分区。
2. `vf_pvrow_surf_to_gnd_surf_obstruction_hottel` 取 `is_left=false`；row0 不是最右边排，因此进入遮挡 helper，并选择 row1 的完整排最低点 `(1.5,0.9999999999999999)`。
3. row0 完整排端点为 `(0.5,1)` 和 `(−0.5,0.9999999999999999)`。front 子段构造/舍入后，两端 y 都成为1。按批准 tie rule：`high=(-0.5,1)`、`low=(0.5,1)`，与带符号字符串分支假设的严格下降端点方向相反。Geometry tie rule 无需改变。
4. 此处四条射线都使用直接长度：选中的邻排在它们右边，没有射线穿过邻排。首个错误符号出现在 `_vf_hottel_gnd_surf` 按 `shadow_is_left=false` 和上述 high/low 标签指定 crossed/uncrossed 时（vfmethods.py 第523–536行），不在距离计算或最终 reciprocal 回填处。

| 字符串 | 端点对 | 冻结值 |
|---|---|---:|
| l1 | high → ground right | 1.0 |
| l2 | low → ground left | 2.2360679774997894 |
| d1 | high → ground left | 1.4142135623730947 |
| d2 | low → ground right | 1.414213562373095 |

`(d1+d2-l1-l2)/(2*1) = -0.20382042637679976`。front/right 筛选保留该负数；再除以地面长度进行互易回填，得到 `F[3,28] = -0.2038204263767998`。实际两面相向、连接射线无遮挡，物理交换应为正。

以精确 binary64 坐标为输入，独立 Decimal90 得到：

```text
0.203820426376799881571260703428314244839887184860063968644491299451303351033184896553653049
```

Decimal110 在小数点后88位以外仍一致。独立可见角度/线积分为 `0.20382042637679987`。另外直接对双重余弦核做数值积分，得到非平凡收敛序列：

| 每段 Gauss 阶数 | F[3,28] |
|---:|---:|
| 2 | 0.20526498482540437 |
| 4 | 0.20381945497162346 |
| 8 | 0.2038204263816811 |
| 16 | 0.20382042637679984 |
| 32 | 0.20382042637679987 |
| 64 | 0.2038204263767998 |
| 128 | 0.20382042637680015 |

[minimal-counterexample.json](../../../evidence/execution/launch-closure/lcb-01/minimal-counterexample.json) 完整保存上述值、几何、Reference 中间量和独立输出。

## 影响域与分类

66 个样本构成有界覆盖集：包含所有指定 tilt 点，axis±90° 两种方位及镜像太阳方向，N=1/2/3/11、cut=1/2，并在近180°增加 cut=4。宽/高固定1、gcr=0.5、地面=[−100,100]。这不是对高度、尺度、排距、阴影状态、离地间隙和连续输入的穷举。触发条件是端点顺序，不是一个声称普遍适用的角度阈值。

| Case | Tilt | 方位 | N | Cut | Full 偏差项 | 越界项 |
|---|---:|---:|---:|---:|---:|---:|
| VF052 | 180 | 270 | 2 | 2 | 27 | 25 |
| VF053 | 180 | 270 | 3 | 1 | 37 | 36 |
| VF054 | 180 | 270 | 3 | 2 | 67 | 66 |
| VF055 | 180 | 270 | 11 | 1 | 493 | 492 |
| VF062 | 179.99999999999997 | 90 | 3 | 4 | 67 | 63 |
| VF063 | 179.99999999999997 | 270 | 3 | 4 | 37 | 30 |
| VF064 | 180 | 90 | 3 | 4 | 67 | 63 |
| VF065 | 180 | 270 | 3 | 4 | 127 | 126 |

8/66 case 共922个 Full 偏差：408 PV→ground、408 ground→PV、70 ground→residual-sky、36 PV→residual-sky。没有发现显著 PV→PV 偏差。其余58个样本在候选 comparator 内一致，不能由此证明所有 >90° 配置都正确。精确180°/方位90°/cut1 通过，而 cut4 失败；`180−1 ULP` 在两种方位下均为 cut1 通过、cut4 失败。仅按角度特殊处理不足以修复。

`anomaly-taxonomy.json` 对每一异常有向项记录双方 key、side、row、ground element、helper path、cut-point side、raw/candidate 值。`obstruction_helper` 只是 Reference 路径标签，不证明存在物理遮挡；另以相向pair凸包内部是否与挡板相交，判断正测度遮挡：816个异常physical pair均为UNOBSTRUCTED，106个residual项不适用；物理地面左/右/重叠与cut-point side分开记录。物理遮挡另由射线相交判断。`independent-crosschecks.json` 包含30组遮挡使裸字符串大小减小的实例。覆盖阴影/受光地面、边排/中间排和两侧。候选完整矩阵包含所有 active pair、inactive 零槽及边界行。

## 七个指定函数的审查结论

| 函数 | 发现 |
|---|---|
| vf_pvrow_surf_to_gnd_surf_obstruction_hottel | 依据 cut-point side/边排分支，保留负中间量并传播互易性；VF053 的首个分歧不在 side mask。 |
| _vf_hottel_gnd_surf | 舍入后的 high/low tie 破坏带符号端点配对；408个负 helper 均满足此触发条件。 |
| _hottel_string_length | 单条直接/绕行距离均非负。VF053 所选最低遮挡点并不实际遮挡，没有引入绕行；复用角度判断前仍须证明其 ordered-row 假设。 |
| _vf_surface_to_surface | 给出非负大小，不提供面向/可见性 oracle。相向且无遮挡的测试对一致；翻转法向或加入挡板后，同一裸大小就不正确。 |
| vf_pvrow_to_pvrow | 使用相邻排及 side mask；本扫描含 >90° 未发现显著偏差。候选仍要求按实际法向工作，不交换身份。 |
| calculate_vf_to_gnd | 独立的 Fast 问题：VF053 row0 单侧 min 使“左地面段”从−100指向约−8.17e15，既越出有限域又反向。数值消减得到朝上背面的0.5。中间排最低端点代理也不等于有限地面。 |
| calculate_vf_to_pvrow | 本扫描未发现显著 back→PV 聚合偏差；背面/相邻排选择及 shaded endpoint 构造仍需后续 Fast 覆盖，本次没有认证全部 Fast 源项。 |

Fast 地面组在53个 case、139个字段上与独立有限地面结果不同。许多偏差在0°/45°/120°已出现，属于有限域代理差异，不能算作 Full 负号 bug。180°边排错误和近180°正值消减残差，说明 abs 无法修复全部路径。[fast-helper-comparison.json](../../../evidence/execution/launch-closure/lcb-01/fast-helper-comparison.json) 独立保存这些结果。推荐 Fast 几何组由有限 F 聚合，但必须由 Owner 明确批准兼容性变化；这不会把 Fast 变成 Full radiosity。

## 独立证据与局限

独立 oracle 不导入 pvfactors VF helper。它从三维漫射余弦积分推导无限排二维核，显式检测射线与不透明排段的相交；内层角度积分加外层 SciPy 求积，与四端点 Hottel 不同构。[COMSOL 辐射推导](https://www.comsol.com/blogs/introduction-to-computing-radiative-heat-exchange) 支持基础余弦积分和无遮挡前提；本次自行推导二维约化、可见单元语义及实现。[NASA View Factor 报告](https://ntrs.nasa.gov/api/citations/19950020924/downloads/19950020924.pdf) 提供方法背景。两者都不被当成项目批准或未经验证的数值 fixture。

解析遮挡样例：y=0 与 y=2 各有长度2的平行段，x=1 有连接两平面的不透明挡板，只有左左、右右半段交换。Decimal100 对两块可见矩形分别做 Hottel 并按长度加权，得到 `sqrt(5)-2 = 0.236067977499789696409…`；可见角度积分在1e−5/1e−8/1e−12三档请求精度下均为 `0.2360679774997897`。无遮挡裸大小为 `sqrt(2)-1 = 0.414213562373095…`。接收面朝反方向或中间完全遮挡时，物理值为零，裸大小仍为正。该 synthetic oracle 验证与批准 Geometry case 明确分开。

全部66个完整矩阵分别请求1e−7、1e−11误差运行，结果在 binary64 上相同（按可见性事件分段后积分平滑），最大估计求积误差低于9.92e−15。这是数值估计，不是严格区间界；上表的直接双重积分另提供逐阶收敛证据。138组代表 pair 还分别做反向积分、完整物理域镜像、端点反转，长度互易最大误差2.91e−15，端点顺序最大误差7.78e−16。镜像连有限地面一起反射，没有错误宣称固定地面范围内的两种方位数组天然完全镜像。

候选矩阵的 reciprocity 由交换量生成，sky closure 由残差生成，因此它们 PASS 本身不是独立正确性证据。数值边界、support、解析样例、反向积分及 mutation tests 提供额外保障。107个裸 Hottel 大小一致的例子是比较后筛选的描述性证据，不能算作107个独立验收测试。

Global abs 结论：**作为通用修复为 NO**。`abs(matrix)` 保留接近2的 sky 并破坏闭合；Fast 的正0.5仍错；无方向 Hottel 不能决定可见面。更窄的“obstruction-helper 取 abs、保留 side mask、重算残差”在66个样本上确实修复了 Full 偏差，但对整个批准域仍为 **NOT PROVEN**。两者不能混为一谈。

## 候选、验证与下一个批准点

- `reference/candidate/vf-lcb01-v0.1/manifest.json`：66 case、198 raw/normalized/corrected artifacts。raw F 采用无损稀疏表示，只省略精确零。Infinity 只以显式字符串存在于 raw cut-point 诊断字段。矩阵轴仍为 receiver/source ReferenceIndex，最后一项为 sky。
- `comparator-policy.json`：PROPOSED/UNAPPROVED。bounds epsilon=1e−10、expected absolute=2e−9、closure/长度互易=1e−10。预算依据请求求积精度，不从 Reference 的大误差反向放宽，也未被批准为所有平台的保证。Geometry tolerance 冻结不变。
- `candidate-index.json` 锁定准确 manifest hash。超过研究 comparator 的每个修正字段均保存 raw/corrected 和 DEV/CDR/oracle provenance；全部矩阵字段另有独立生成器说明。Fast 几何组提案单独记录。
- R0 `031158a1d1be8cdb9093` 中66个 raw case 二次捕获逐字节一致。增量捕获元数据的 warning 清单较窄，完整重跑元数据作为 canonical，旧凭证保留；没有把 warning 包装为生产 PASS。
- `python scripts/verify_vf_candidate.py reference/candidate/vf-lcb01-v0.1` 检查候选哈希、inventory、Geometry 精确保留和不变量。PASS 仅用于研究，输出明确标记 P4 NOT_READY。`python -m unittest discover -s scripts/tests -v` 包含指定四类 mutation，以及非有限值、support、全零矩阵等检查。
- 当前验证凭证及证据哈希位于 `evidence/execution/launch-closure/lcb-01/`。统一 `verify_project.py assets` 继续检查原491个冻结文件/G2。Launch preflight 因 Owner 批准及其余启动包未完成，仍为 NOT_READY。

请集中审阅 DEV、CDR、comparator 和准确 manifest。Owner 可以批准统一可见性政策及候选范围、要求修改，或仅把 raw Reference 兼容保留为独立诊断模式，不能将其冒充 corrected physical F。默认推荐统一修正政策，包含 Fast 有限几何聚合；不推荐收窄输入域、交换身份或放宽容差。本调查批准不等于全部 P4–P7 fixture 批准，更不构成实现授权。

按任务要求在此停止。Owner 关闭前 LCB-01 对 launch 仍然开放，完整项目 closure 保持 BLOCKED。未改 master/develop/P3 分支、frozen source、Approved Geometry、P3 Design、Geometry tolerance 或生产 Rust 源码。本调查没有执行远端 push、PR、merge、tag 或 release。
