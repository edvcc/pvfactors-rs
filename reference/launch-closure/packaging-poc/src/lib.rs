//! Disposable packaging evidence: array ownership only; no physics or product API.
#![forbid(unsafe_code)]

use numpy::{IntoPyArray, PyArray1, PyReadonlyArrayDyn};
use pyo3::prelude::*;

#[pyfunction]
fn owned_copy<'py>(py: Python<'py>, input: PyReadonlyArrayDyn<'py, f64>) -> Bound<'py, PyArray1<f64>> {
    // Copy while attached; no Python-backed view crosses the detach boundary.
    let owned: Vec<f64> = input.as_array().iter().copied().collect();
    let owned = py.detach(move || owned);
    owned.into_pyarray(py)
}

#[pymodule]
fn pvfactors_packaging_probe(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(owned_copy, m)?)?;
    Ok(())
}
