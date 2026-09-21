# Schema contract

case.schema.json validates the specified catalog, including deliberately invalid physics inputs. Semantic validation (broadcast, positive geometry, axis consistency) belongs to the classifier, not a schema that would discard the invalid cases being tested.

trace.schema.json describes the future immutable capture manifest. Array names and required stages are specified in docs/06. A schema-valid file alone is not sufficient: capture validators must check required field names for Full/Fast, matching rank/axes, units, source/surface ordering, payload hashes, finite masks, and no mutation of F during G construction. Missing mandatory Full fields must fail approval even though additional diagnostic arrays are allowed.

Current nominal-trace.npz is research evidence in the original upstream axis convention, not an instance of the approved normalized trace schema. It records its available keys only; do not silently treat it as a full corpus.
