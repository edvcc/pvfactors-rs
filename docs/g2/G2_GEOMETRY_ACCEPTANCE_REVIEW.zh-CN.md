# G2 Geometry Acceptance Review

- 评审日期：2026-09-21
- 结论：**CONDITIONALLY PASS**
- Gate 声明：**Technical package complete with recorded baseline conditions; Awaiting Repository Owner Approval.**
- Candidate：`geometry-golden-v0.1-candidate`
- Manifest SHA-256：`5afcc7e2cbc761ef883a422dd596e972cda603313a27f8425278dd067be57e3f`
- Tolerance：`geometry-tolerance-v0.1`

## 结论

CDR-003 与 CDR-006 已形成完整 approval candidate。Candidate pipeline 已采集 row geometry、
projection、raw/clipped shadow、PV/ground partition、稳定 logical key、`ReferenceIndex` 与
active map；raw、normalized、corrected artifact 已分离；schema、不变量、差异追溯、compare
和同环境 reproducibility 均通过。在已测试范围内未发现未知 Geometry semantic blocker。

G2 不能标为 `PASS`：Repository Owner 尚未批准 CDR-003、CDR-006 与 Golden candidate。
GitHub 记录显示 PR #1 在本次 runtime closure 推送前已被外部 merge，因此远端现在存在
`develop`；本任务未修改该分支，也不据此推定 Owner 对 P3 integration baseline 的意图。
Canonical Runtime blocker 已关闭：当前 candidate 在 R0 下生成，并通过与保留的 3.12.12
运行结果的对照。

## Verified

- 输入 ZIP SHA-256 与内部 121 项 hash：PASS；
- 冻结 upstream source 78 个 Git blob hash：PASS；
- Upstream Reference suite：102 passed / 11 warnings / 0 failed；
- G2 concrete catalog：39 cases，所需 derived family 已展开为具体输入；
- Generated corpus：117 artifacts，加 manifest 与 validation summary；
- Canonical Runtime R0：Linux x86_64 / glibc 2.39 / CPython 3.12.14；29 个固定
  package、GEOS 3.13.1 与确定性环境变量全部匹配，PASS；
- Case 与 artifact JSON Schema：PASS；
- 独立不变量：row-side conservation、shade bounds、ground 无正长度 overlap/无 gap 的完整覆盖、
  active endpoint finite、active threshold、identity/order/map 精确、corrected finite extent、
  structured invalid error、primitive expectation 与 full mirror：PASS；
- 两次独立完整生成：字节级一致，PASS；
- 与 macOS arm64 / CPython 3.12.12 的 cross-runtime payload comparison：PASS；
  19,511 个 topology/key/side/index/active-state 检查精确一致，数值无超 tolerance 差异；
- Raw/corrected provenance：PASS；只有具名 DEV-004/CDR-003 与 DEV-016/CDR-006 字段差异；
- Branch safety：工作位于 `research/g2-geometry-acceptance`；local 与 remote-tracking master
  保持 `bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba`；
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
4. 指定/创建 integration `develop` baseline，并决定 PR 路径。

`reference/approved` 保持 `NOT APPROVED`。没有 promote candidate，也没有 merge。

## Not verified

- Windows 与 R0 以外的 Linux kernel/libc 变体：未执行；
- Rust native differential：P3 被阻止，属于范围外；
- Browser、IDE、packaging、Python binding、View Factor、Perez、Radiosity、aggregate
  irradiance、parallelism、performance：范围外；
- Owner 身份/签字及批准证据：不存在。

## Gate 转换

Phase 0–1 输入证据以记录条件方式接受。P2 / G2 技术工作已形成完整审查包，Runtime blocker
已关闭，但 P3 仍被阻止。只有 Owner 批准三个治理对象并指定 integration baseline 后，G2
才可升级为 `PASS`。
