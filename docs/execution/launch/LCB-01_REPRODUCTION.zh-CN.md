# LCB-01 复现与验证

仅供研究。候选验证不关闭 Owner 决策，也不验收 P4。解释结果前先读调查报告、DEV-028、CDR-008。没有新增 Rust/runtime 依赖；研究使用 stdlib 和 R0 既有 NumPy/SciPy。保留原 attribution/license；capture 调用冻结 Reference，`independent.py` 从余弦测度和线段几何独立推导，不逐行翻译 Reference VF helper。

## 本地快速验证

```sh
python scripts/verify_vf_candidate.py reference/candidate/vf-lcb01-v0.1
python -m unittest discover -s scripts/tests -v
python scripts/verify_project.py assets
python scripts/verify_project.py preflight
```

前三项应在文档要求环境中通过（Python≥3.11；project/G2 检查使用既有 jsonschema）。Owner 关闭决策、补齐剩余全项目启动要求前，clean checkout 上 preflight 应保持 NOT_READY/exit2，不能修改状态字符串制造 PASS。

## 全新独立数值重建

使用既有 `pvfactors-rs-g2-r0:cp31214` 镜像，Linux/amd64、离线；environment ID 必须为 `031158a1d1be8cdb9093`。从仓库根目录运行。每轮使用新工作目录，不覆盖已经验收的候选文件；以下采用 ignored work 路径：

```sh
mkdir -p reference/work/lcb01-review/candidate reference/work/lcb01-review/evidence
docker run --rm --pull=never --platform linux/amd64 --network=none --read-only --tmpfs /tmp \
  -v "$PWD:/workspace:ro" -v "$PWD/reference/work/lcb01-review:/review" -w /workspace \
  pvfactors-rs-g2-r0:cp31214 python3.12 reference/launch-closure/lcb01/capture.py --output /review/candidate
docker run --rm --pull=never --platform linux/amd64 --network=none --read-only --tmpfs /tmp \
  -v "$PWD:/workspace:ro" -v "$PWD/reference/work/lcb01-review:/review" -w /workspace \
  pvfactors-rs-g2-r0:cp31214 python3.12 reference/launch-closure/lcb01/analyze.py \
  --candidate /review/candidate --evidence /review/evidence
docker run --rm --pull=never --platform linux/amd64 --network=none --read-only --tmpfs /tmp \
  -v "$PWD:/workspace:ro" -v "$PWD/reference/work/lcb01-review:/review" -w /workspace \
  pvfactors-rs-g2-r0:cp31214 python3.12 reference/launch-closure/lcb01/crosscheck.py \
  --candidate /review/candidate --evidence /review/evidence
```

逐个比较 raw/normalized/corrected JSON 对象及66-case inventory 与已提交候选；JSON key 顺序无关，但字段值/类型必须保持。Raw 应逐字节一致。检查 domain-scan、independent-oracle-verification、minimal-counterexample 和 Fast 正值反例。扫描固定66case、最多11排/cut4、R0单线程设置，每个事件单元求积有 `limit=200` 限制；无研究理由不扩大笛卡尔积。提交的候选/证据约13MB，生成工作副本被忽略，保留验证凭证后可清理。

`package.py` 是本具名未批准候选的准备期打包器，不是启动命令。它在独立捕获后绑定 raw/normalized/corrected 哈希、代码哈希及 proposed comparator；不得用来静默刷新 Owner 已接受的manifest。`--only-new`/`--resume` 仅便于增量研究，会沿用此前数值；完整干净重建才是可复现性检查。归档的增量 warning 元数据与完整捕获不同，raw 值一致，完整凭证作为 canonical。

结果解释：Reference bounds FAIL 是本次调查的缺陷；corrected candidate invariants PASS 和 mutation tests PASS，不表示 Reference 兼容、完整P4覆盖、容差已批准、生产测试已运行或获得实现启动权限。独立求积误差估计不是严格区间界。正式停点仍为 **LCB-01 — READY FOR OWNER DECISION**。
