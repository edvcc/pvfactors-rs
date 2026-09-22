"""Installed wheel ownership/strides/import evidence, not a production binding."""
import argparse
import importlib.metadata as md
import json
import platform
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pvfactors_packaging_probe as probe

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
cases = 0
for x in [np.arange(20.0), np.arange(30.0).reshape(5, 6)[:, ::-2], np.array([]),
          np.asfortranarray(np.arange(12.0).reshape(3, 4))]:
    wanted = np.asarray(x).ravel(order='C').copy()
    y = probe.owned_copy(x)
    np.testing.assert_array_equal(y, wanted)
    assert not np.shares_memory(x, y)
    x[...] = -9
    np.testing.assert_array_equal(y, wanted)
    del x
    y[...] = 7
    cases += 1
with ThreadPoolExecutor(max_workers=4) as pool:
    outputs = list(pool.map(lambda _: probe.owned_copy(np.arange(100.0)), range(12)))
for y in outputs:
    np.testing.assert_array_equal(y, np.arange(100.0))
cases += len(outputs)
try:
    probe.owned_copy(np.array(['invalid'], dtype=object))
    raise AssertionError('object dtype unexpectedly accepted')
except TypeError:
    cases += 1
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps({'status': 'PASS', 'tests_run': cases,
    'python': sys.version, 'platform': platform.platform(), 'machine': platform.machine(),
    'numpy': np.__version__, 'package': md.version('pvfactors-packaging-probe'),
    'boundary': 'Isolated installed-wheel smoke only; no product physics or minimum OS proof'}, indent=2)+'\n')
print(f'PASS: {cases} packaging ownership/import cases')
