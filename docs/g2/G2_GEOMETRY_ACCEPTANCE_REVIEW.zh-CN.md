# G2 Geometry Acceptance Review

- 评审日期：2026-09-22
- 结论：**CONDITIONALLY PASS**
- Gate 声明：**Technical package complete with recorded baseline conditions; Awaiting Repository Owner Approval.**
- Candidate：`geometry-golden-v0.1-candidate`
- Manifest SHA-256：`efd2adf3037740b9788792c9f5be6122fb2e842d72f2ddbe2bb5552abc27141b`
- Tolerance：`geometry-tolerance-v0.1`

## 结论

CDR-003 已纳入 Owner Review Revision 1，CDR-006 已纳入 DEV-013 明确决策；predicate 数值与
tolerance 未改，二者仍是 approval candidate。
Candidate pipeline 已采集 row geometry、
projection、raw/clipped shadow、PV/ground partition、稳定 logical key、`ReferenceIndex` 与
active map；raw、normalized、corrected artifact 已分离；schema、不变量、差异追溯、compare
和同环境 reproducibility 均通过。在已测试范围内未发现未知 Geometry semantic blocker。

G2 不能标为 `PASS`：Repository Owner 尚未批准 CDR-003、CDR-006 与 Golden candidate。
`develop` 是本次 closure 工作的 integration baseline，但本任务不直接修改或 merge 该分支。
Canonical Runtime blocker 已关闭：当前 candidate 在 R0 下生成，并通过与独立再生成的 3.12.12
运行结果的对照。

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

## Recommended

- CDR-003：**Recommended for Approval**；
- CDR-006：**Recommended for Approval**；
- `geometry-tolerance-v0.1`：仅对 Geometry **Recommended for Approval**；
- `geometry-golden-v0.1-candidate`：**Recommended for Approval**；仍是 candidate，
  未自动批准。

## Awaiting Owner Approval

1. 批准或拒绝 CDR-003；
2. 批准或拒绝 CDR-006；
3. 批准或拒绝准确的 R0 生成 candidate manifest hash；
4. 审查新建的 `develop` PR；三个治理决定明确前不得 merge。

`reference/approved` 保持 `NOT APPROVED`。没有 promote candidate，也没有 merge。

## Not verified

- Windows 与 R0 以外的 Linux kernel/libc 变体：未执行；
- Rust native differential：P3 被阻止，属于范围外；
- Browser、IDE、packaging、Python binding、View Factor、Perez、Radiosity、aggregate
  irradiance、parallelism、performance：范围外；
- Owner 身份/签字及批准证据：不存在。

## Gate 转换

Phase 0–1 输入证据以记录条件方式接受。P2 / G2 技术工作已形成完整审查包，Runtime blocker
已关闭，但 P3 仍被阻止。只有 Owner 批准三个治理对象后，G2
才可升级为 `PASS`。现有 `develop` 是 integration baseline；本任务不 merge。
