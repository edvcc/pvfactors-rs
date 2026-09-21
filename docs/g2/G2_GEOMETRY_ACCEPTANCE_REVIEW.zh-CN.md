# G2 Geometry Acceptance Review

- 评审日期：2026-09-22
- 结论：**PASS**
- Gate 声明：**Technical Gate PASS；Owner Approval PASS；Canonical Runtime R0 PASS；Golden Approval PASS。**
- Approved Golden：`geometry-golden-v0.1`
- Source candidate：`geometry-golden-v0.1-candidate`
- Approved manifest SHA-256：`efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Tolerance：`geometry-tolerance-v0.1`

## 结论

CDR-003 已纳入 Owner Review Revision 1，CDR-006 已纳入 DEV-013 明确决策；predicate 数值与
tolerance 未改。Repository Owner 已于 2026-09-22 批准 CDR-003、CDR-006、
`geometry-tolerance-v0.1` 与准确 Geometry Golden manifest。
Candidate pipeline 已采集 row geometry、
projection、raw/clipped shadow、PV/ground partition、稳定 logical key、`ReferenceIndex` 与
active map；raw、normalized、corrected artifact 已分离；schema、不变量、差异追溯、compare
和同环境 reproducibility 均通过。在已测试范围内未发现未知 Geometry semantic blocker。

G2 为 `PASS`：technical verification、Owner approval、Canonical Runtime R0、CDR、tolerance
与 Golden approval 条件均已关闭。approved corpus 是具名 candidate 的字节级一致 promotion。
`develop` 仍是 integration baseline；本任务不直接修改或 merge 该分支。

## Verified

- 输入 ZIP SHA-256 与内部 121 项 hash：PASS；
- 冻结 upstream source 78 个 Git blob hash：PASS；
- Upstream Reference suite：102 passed / 11 warnings / 0 failed；
- G2 concrete catalog：55 cases，所需 derived family 已展开为具体输入，包括 `TILT_120`、
  `TILT_180`、`GCR_GT_1`、`SUN_BELOW_HORIZON`、两个闭区间外 invalid-tilt probe、9 个
  predicate ±ULP probe 与 1 个双时刻 nonzero-index DEV-013 probe；
- Generated corpus：165 artifacts，加 manifest 与 validation summary；
- Canonical Runtime R0：Linux x86_64 / glibc 2.39 / CPython 3.12.14；29 个固定
  package、GEOS 3.13.1 与确定性环境变量全部匹配，PASS；
- Case 与 artifact JSON Schema：PASS；
- 独立不变量：65 个 report，覆盖 row-side conservation、shade bounds、ground 无正长度 overlap/无 gap 的完整覆盖、
  active endpoint finite、active threshold、identity/order/map 精确、corrected finite extent、
  structured invalid error、primitive expectation 与 full mirror：PASS；
- 两次独立完整生成：字节级一致，PASS；
- 与 macOS arm64 / CPython 3.12.12 的 cross-runtime payload comparison：PASS；
  24,391 个 topology/key/side/index/active-state 检查精确一致，无 exact-payload 或超 tolerance
  差异；最大绝对差：angle 0、length `5.551115123125783e-16 m`、orientation
  `5.551115123125783e-17`、position `8.881784197001252e-16 m`；
- Raw/corrected provenance：PASS；47 条 deviation record 均具有完整 field-level provenance，
  分别归属 DEV-004/CDR-003、DEV-013/CDR-006、DEV-016/CDR-006 或 DEV-027/CDR-003；
- Branch safety：工作位于从 `origin/develop` `ddee1f43...` 创建的
  `research/g2-owner-review-closure`；authoritative `origin/master` 保持
  `bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba`；
- Rust Geometry Core、solver、Python binding、execution planner、SIMD、GPU 均未实现，符合禁区。

## Approved

- CDR-003：**APPROVED**；
- CDR-006：**APPROVED**；
- `geometry-tolerance-v0.1`：仅对 Geometry **APPROVED**；
- `geometry-golden-v0.1`：按上述准确 manifest hash **APPROVED**；
- P3 Entry Contract：**ACTIVE**。

## 治理边界

`reference/approved/geometry-golden-v0.1` 是 immutable approved baseline。后续 candidate
不得覆盖；manifest 变化必须获得新的明确 Owner approval。PR #2 仍按正常流程 review，本任务
未 merge。P3 implementation 未开始。

## Not verified

- Windows 与 R0 以外的 Linux kernel/libc 变体：未执行；
- Rust native differential：P3 implementation 尚未开始，属于范围外；
- Browser、IDE、packaging、Python binding、View Factor、Perez、Radiosity、aggregate
  irradiance、parallelism、performance：范围外；
- P3 implementation 结果：不存在；本 closure 只激活 Entry Contract。

## Gate 转换

Phase 0–1 输入证据已接受。P2 / G2 技术工作、Runtime verification 与治理批准均已完成。
G2 为 `PASS`；P3 Entry Contract 为 `ACTIVE`，P3 implementation 仍为 `NOT STARTED`。现有
`develop` 是 integration baseline；本任务不 merge。
