# Invariant Computing Lab — Public Repository Tree Readiness Audit

**Checked:** 8 November 2026 · **Scope:** all 56 public Invariant Computing Lab GitHub repositories, recursively scanned on their then-current default branches using the GitHub repository-tree API. Private organization and personal repositories are excluded.

## Structural inventory (not an execution result)

- **56/56** repositories were readable; no incomplete/truncated tree response was reported.
- **0/56** had a visible `.github/workflows/` file in the default branch. This does **not** mean no testing has ever occurred; CI might run elsewhere.
- **3/56** had a licence-like file path with basename `LICENSE`, `LICENCE` or `COPYING`. Absence of such a file does **not** prove no rights notice exists; review repository-level rights and third-party components separately. **Never invent an open-source licence.**
- **45/56** had a test-like file path (heuristic: a `test/`, `tests/` directory or `test_*.py`). Presence does **not** establish successful execution, meaningful assertions or coverage.
- **56/56** had a dependency-manifest-like path (`pyproject.toml`, `requirements*.txt`, `package.json`, etc.). No environment, dependency or security test was executed.

## Per-repository file-tree evidence

| Repository | File paths | Test-like path | Licence-like path | GitHub Actions workflow | Dependency manifest |
|---|---:|---|---|---|---|
| [2dqm-lattice-index](https://github.com/Invariant-Computing-Lab/2dqm-lattice-index) | 43 | Seen | Not located | Not located | Seen |
| [g19-afc-finite-recoverability-bounded](https://github.com/Invariant-Computing-Lab/g19-afc-finite-recoverability-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g20-afc-side-information-limits-bounded](https://github.com/Invariant-Computing-Lab/g20-afc-side-information-limits-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g21-afc-checkpoint-replay-bounded](https://github.com/Invariant-Computing-Lab/g21-afc-checkpoint-replay-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g22-afc-exact-fallback-bounded](https://github.com/Invariant-Computing-Lab/g22-afc-exact-fallback-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g23-afc-fault-injection-bounded](https://github.com/Invariant-Computing-Lab/g23-afc-fault-injection-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g24-afc-distributed-recovery-bounded](https://github.com/Invariant-Computing-Lab/g24-afc-distributed-recovery-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g25-afc-artifact-nondestruction-bounded](https://github.com/Invariant-Computing-Lab/g25-afc-artifact-nondestruction-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g26-afc-reference-oracles-bounded](https://github.com/Invariant-Computing-Lab/g26-afc-reference-oracles-bounded) | 14 | Seen | Not located | Not located | Seen |
| [bcq-marked-invariants](https://github.com/Invariant-Computing-Lab/bcq-marked-invariants) | 36 | Seen | Not located | Not located | Seen |
| [forge-l-core](https://github.com/Invariant-Computing-Lab/forge-l-core) | 13 | Not located | Not located | Not located | Seen |
| [forge-ym-finite](https://github.com/Invariant-Computing-Lab/forge-ym-finite) | 49 | Seen | Seen | Not located | Seen |
| [g36-gop-auxiliary-lifts-bounded](https://github.com/Invariant-Computing-Lab/g36-gop-auxiliary-lifts-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g72-invariant-source-catalog-bounded](https://github.com/Invariant-Computing-Lab/g72-invariant-source-catalog-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g73-invariant-archive-indexer-bounded](https://github.com/Invariant-Computing-Lab/g73-invariant-archive-indexer-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g74-invariant-provenance-deduper-bounded](https://github.com/Invariant-Computing-Lab/g74-invariant-provenance-deduper-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g75-invariant-reproducibility-cli-bounded](https://github.com/Invariant-Computing-Lab/g75-invariant-reproducibility-cli-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g76-invariant-ci-acceptance-bounded](https://github.com/Invariant-Computing-Lab/g76-invariant-ci-acceptance-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g77-invariant-rights-privacy-audit-bounded](https://github.com/Invariant-Computing-Lab/g77-invariant-rights-privacy-audit-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g78-invariant-dataset-split-audit-bounded](https://github.com/Invariant-Computing-Lab/g78-invariant-dataset-split-audit-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g79-invariant-hf-card-generator-bounded](https://github.com/Invariant-Computing-Lab/g79-invariant-hf-card-generator-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g80-invariant-release-registry-bounded](https://github.com/Invariant-Computing-Lab/g80-invariant-release-registry-bounded) | 17 | Seen | Not located | Not located | Seen |
| [gop-finite-benchmarks](https://github.com/Invariant-Computing-Lab/gop-finite-benchmarks) | 14 | Not located | Not located | Not located | Seen |
| [gop-finite-foundation](https://github.com/Invariant-Computing-Lab/gop-finite-foundation) | 660 | Seen | Not located | Not located | Seen |
| [hlf-invariant-geometry](https://github.com/Invariant-Computing-Lab/hlf-invariant-geometry) | 34 | Not located | Not located | Not located | Seen |
| [ice-dyadic-invariants](https://github.com/Invariant-Computing-Lab/ice-dyadic-invariants) | 36 | Not located | Not located | Not located | Seen |
| [idf-quotient-geometry](https://github.com/Invariant-Computing-Lab/idf-quotient-geometry) | 38 | Not located | Not located | Not located | Seen |
| [oft-warped-spectrum](https://github.com/Invariant-Computing-Lab/oft-warped-spectrum) | 34 | Not located | Not located | Not located | Seen |
| [ogd-spherical-spectrum](https://github.com/Invariant-Computing-Lab/ogd-spherical-spectrum) | 38 | Not located | Not located | Not located | Seen |
| [pmst-invariant-quotient](https://github.com/Invariant-Computing-Lab/pmst-invariant-quotient) | 43 | Not located | Not located | Not located | Seen |
| [vgm-limited-core](https://github.com/Invariant-Computing-Lab/vgm-limited-core) | 32 | Not located | Not located | Not located | Seen |
| [yildirim-lattice-invariants](https://github.com/Invariant-Computing-Lab/yildirim-lattice-invariants) | 43 | Not located | Seen | Not located | Seen |
| [huret-label-free-audit](https://github.com/Invariant-Computing-Lab/huret-label-free-audit) | 46 | Not located | Not located | Not located | Seen |
| [icl-core](https://github.com/Invariant-Computing-Lab/icl-core) | 206 | Seen | Not located | Not located | Seen |
| [icl-native-r5](https://github.com/Invariant-Computing-Lab/icl-native-r5) | 1437 | Seen | Not located | Not located | Seen |
| [g10-rari-distributed-inference-bench-bounded](https://github.com/Invariant-Computing-Lab/g10-rari-distributed-inference-bench-bounded) | 14 | Seen | Not located | Not located | Seen |
| [invariant-omega-portable](https://github.com/Invariant-Computing-Lab/invariant-omega-portable) | 46 | Seen | Not located | Not located | Seen |
| [rari-neurobrain-v7-release](https://github.com/Invariant-Computing-Lab/rari-neurobrain-v7-release) | 25 | Seen | Seen | Not located | Seen |
| [rari-omega-engine](https://github.com/Invariant-Computing-Lab/rari-omega-engine) | 32 | Seen | Not located | Not located | Seen |
| [rari-omega-reference](https://github.com/Invariant-Computing-Lab/rari-omega-reference) | 30 | Seen | Not located | Not located | Seen |
| [g27-sacra-authority-graph-bounded](https://github.com/Invariant-Computing-Lab/g27-sacra-authority-graph-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g28-sacra-role-delegation-bounded](https://github.com/Invariant-Computing-Lab/g28-sacra-role-delegation-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g29-sacra-provenance-engine-bounded](https://github.com/Invariant-Computing-Lab/g29-sacra-provenance-engine-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g30-sacra-conflict-resolution-bounded](https://github.com/Invariant-Computing-Lab/g30-sacra-conflict-resolution-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g31-sacra-human-approval-gate-bounded](https://github.com/Invariant-Computing-Lab/g31-sacra-human-approval-gate-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g32-sacra-multiagent-policy-tests-bounded](https://github.com/Invariant-Computing-Lab/g32-sacra-multiagent-policy-tests-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g33-sacra-narrative-continuity-bounded](https://github.com/Invariant-Computing-Lab/g33-sacra-narrative-continuity-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g34-sacra-editorial-integrity-bounded](https://github.com/Invariant-Computing-Lab/g34-sacra-editorial-integrity-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g43-ievf-evidence-schema-bounded](https://github.com/Invariant-Computing-Lab/g43-ievf-evidence-schema-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g44-ievf-evidence-registry-bounded](https://github.com/Invariant-Computing-Lab/g44-ievf-evidence-registry-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g45-ievf-claim-gate-bounded](https://github.com/Invariant-Computing-Lab/g45-ievf-claim-gate-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g46-ievf-itf-benchmark-bounded](https://github.com/Invariant-Computing-Lab/g46-ievf-itf-benchmark-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g47-ievf-ori-benchmark-bounded](https://github.com/Invariant-Computing-Lab/g47-ievf-ori-benchmark-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g48-ievf-rrn-aiba-suite-bounded](https://github.com/Invariant-Computing-Lab/g48-ievf-rrn-aiba-suite-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g49-ievf-sapi-magh-suite-bounded](https://github.com/Invariant-Computing-Lab/g49-ievf-sapi-magh-suite-bounded) | 14 | Seen | Not located | Not located | Seen |
| [g50-ievf-cross-domain-transfer-bounded](https://github.com/Invariant-Computing-Lab/g50-ievf-cross-domain-transfer-bounded) | 14 | Seen | Not located | Not located | Seen |

## Release-quality completion sequence

1. **Provenance and rights first.** Review `README.md`, upstream licence/source manifests, third-party datasets, weights and personal-data restrictions. A public repository is not automatically open licensed.
2. **Execution second.** Pin interpreter and dependencies, capture deterministic fixture/test commands, assess false positives and known limitations, and record dated run evidence. A filename is not a test result.
3. **CI only after dry-run.** Add GitHub Actions workflow only when the current test command is proved locally and the organization explicitly accepts run-cost/security implications. No workflows were created or triggered by this audit.
4. **Version labels.** Freeze source hash, original vs reconstructed/replacement provenance, release candidate semantics and artefact type (reproducibility package vs independent research result).
5. **Public claim review.** State what finite/synthetic tests support and explicitly what they do not establish: new physics, biological mechanism, clinical efficacy, granted patent or industrial readiness.

## Boundary of this audit

This is a **file-tree / navigation audit only**, not a security audit, peer review, clean-room reproducibility test, licence determination, deployment or hardware validation. Some tests may be embedded in other scripts and are therefore not detected by the simple naming heuristic. A zero in a column must not be read as proof that a capability is absent.

Related: [Research programme catalogue](PUBLIC_RESEARCH_CATALOG.md) · [Hugging Face public card audit](PUBLIC_HF_REPOSITORY_INDEX.md) · [Zenodo DOI and community crosswalk](DOI_COMMUNITY_CROSSWALK.md).
