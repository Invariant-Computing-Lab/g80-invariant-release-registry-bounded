# G80 — invariant-release-registry

**Status: PRIVATE CANDIDATE / NEWLY IMPLEMENTED BOUNDED UTILITY.** This is NOT the original unrecovered upstream G80 repository, and is NOT a scientific validation or a public release authorization.

## Functionality

This standalone, standard-library Python utility implements the finite **`release_registry`** check. It includes deterministic synthetic input, fail-closed behavior where appropriate, and self-contained unit tests.

```shell
python run.py --input sample.json
python -m unittest discover -v
```

The fixture result is **PASS**. HOLD is the correct safe result for unresolved approval, license, or claim review gates.

## V7 target linkage

- Target code: `G80`
- Planned title: `invariant-release-registry`
- Source plan: `Invariant_Yayin_Plani_V7_Teslim(6).html`
- Original scientific/rights limitation: Bağlandı≠doğrulandı; claim gate'in yanlış olumlu/olumsuz kontrolü ve dış kullanım benchmark'ı gerekir.
- Implementation date: 2026-10-20, independently authored bounded starting implementation, **not** an independent experiment or original recovered functionality.

## Boundaries

No protected clinical data, third-party weights, network calls, training, physical claims, or public posting. The proof, source lineage, rights and integration gates remain open.

## Installation and release engineering (0.1.1)

```sh
python -m pip install .
invariant-g80 --input sample.json
python -m unittest discover -v
```

Exit codes: 0 = this bounded check passed; 1 = invalid input or check failure; 2 = HOLD / unverified evidence. HOLD is not success. Wheels use the unique `invariant_v7_g80` module to avoid cross-package import collisions. Empty evidence, string booleans, invalid digests and unsafe Windows/POSIX paths are rejected. Human-signature authenticity cannot be proven by a JSON flag.

This engineering revision does not recover the original upstream implementation and does not resolve ownership, licensing or independent scientific validation.
## Verified packaging revision — 2026-10-20

18 bounded contract tests, wheel build, clean offline co-install and CLI checks. Not the complete original research product.

Runtime state: `PASS`. Rights and release approval are separate. See `RELEASE_VERIFICATION.json`. No paper or conference submission is included as a new software result.
