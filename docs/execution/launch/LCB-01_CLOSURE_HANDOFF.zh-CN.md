# LCB-01 关闭凭证与交接

Owner决定与targeted seed批准见[Owner记录](LCB-01_OWNER_DECISIONS.zh-CN.md)。当前计算门禁以 [verification-summary.json](../../../evidence/execution/launch-closure/lcb-01/verification-summary.json) 为准，由 `scripts/lcb01_closure.py` 检查content/receipt绑定。缺少任何必要检查或溯源时，只能为 **LCB-01 — CLOSURE BLOCKED**；全部通过后为 **LCB-01 — CLOSED**、**FULL-PROJECT LAUNCH CLOSURE — RESUME AUTHORIZED**、**FULL IMPLEMENTATION — INACTIVE**。本文不在凭证产生前宣称验证通过。

## 提交与溯源协议

1. 将全部政策、状态、candidate元数据、verifier与测试变更提交为content commit C。在clean状态对C执行全新R0捕获/重建、candidate比较、全部自测、独立crosscheck、baseline/assets及preflight。正常push C到指定研究分支，并经GitHub commit API解析。
2. 只把真实命令输出、全新独立报告和被测对象哈希写入 `owner-closure/receipts/`，形成receipt commit R；不改变被测政策、代码或corpus。Push R后，直接经GitHub解析C和R。
3. 再用一个仅含证据索引的commit，将已知C/R SHA及远端证明记录到 `verification-summary.json`，避免提交哈希自引用。R是包含实际验证凭证的commit，不是后面的索引commit；最终remote HEAD另外报告。C之后只能增加receipt/index；被测内容变化必须重新clean验证。

凭证记录 `tested_checkpoint`、`tested_content_commit`、`receipt_commit`、manifest/profile/tool哈希、全部必要结果、clean状态、受保护基线及远端可解析性，并绑定被测对象与测量文件的准确哈希。旧凭证仅作历史记录，不能关闭门禁。

Verifier在inventory/hash/精确Geometry/bounds/support/reciprocity/closure之外，新增Fast有限聚合检查，并比较66个重新生成的matrix/group。使用 `--actual <fresh-work-corpus>`；缺少实际结果返回NOT_READY，不伪装已经比较expected。新增8项测试覆盖Fast聚合/provenance和expected/exact identity；原62项全部保留，共70项。科学crosscheck继续保留独立反向积分，不能仅依赖由构造生成的互易性。

由于原12项Owner决定、完整P4–P7包及治理条件未完成，preflight仍可NOT_READY。Clean content验证发生在新closure receipt产生前，因此该次还可能报告LCB-01 provenance待完成；最终依据receipt再读门禁，确认LCB-01不再是阻塞项，但不降低总体门禁。

## 只交接，不执行下一阶段

验证关闭后，下一任务从未变化的批准base `d5bc38ebd6ba853c4cec530e4787d1ab6168203d` **加本LCB-01 closure package**，恢复 `research/full-project-launch-closure`。本任务不把package集成到该分支。后续授权任务应以可追溯历史明确纳入审阅包、校验哈希，再准备P4 VF/AOI、P5 irradiance/Perez、P6 radiosity/solver、P7 serial E2E oracle。

禁止生产Rust VF/AOI/Perez/radiosity/simulation、执行CODEX_FULL_IMPLEMENTATION_TASK.md、merge/tag/release/publish。master/develop/P3/frozen Reference/Approved Geometry/Geometry tolerance均不变。DEV-029不关闭CDR-007，targeted seed不是完整P4。本任务正常push、核验远端后结束，工作区保持clean。
