# Design document index

Every flagship project gets an RFC before it is built, and ADRs as decisions are made. This index
links each document to the code it shaped. It grows with every wave.

## Wave 1

| Project | RFC | ADRs | Code | Results |
|---|---|---|---|---|
| lsm-kv-store | [RFC 0001](https://github.com/EquinoxWN/lsm-kv-store/blob/main/docs/rfc/0001-design.md) | [0002 ReadAt before mmap](https://github.com/EquinoxWN/lsm-kv-store/blob/main/docs/adr/0002-pread-before-mmap.md) | [lsm.go](https://github.com/EquinoxWN/lsm-kv-store/blob/main/lsm.go) | [M1](https://github.com/EquinoxWN/lsm-kv-store/blob/main/docs/results/m1.md) |
| polyglot-data-structures | [RFC 0001](https://github.com/EquinoxWN/polyglot-data-structures/blob/main/docs/rfc/0001-design.md) | [0002 vectors from reference models](https://github.com/EquinoxWN/polyglot-data-structures/blob/main/docs/adr/0002-vectors-from-reference-models.md) | [spec/](https://github.com/EquinoxWN/polyglot-data-structures/tree/main/spec) | [M1](https://github.com/EquinoxWN/polyglot-data-structures/blob/main/docs/results/m1.md) |
| tiny-transformer-scratch | [RFC 0001](https://github.com/EquinoxWN/tiny-transformer-scratch/blob/main/docs/rfc/0001-design.md) | [0002 NumPy-only, float64 gradcheck](https://github.com/EquinoxWN/tiny-transformer-scratch/blob/main/docs/adr/0002-float64-gradcheck-and-numpy-only.md) | [autograd.py](https://github.com/EquinoxWN/tiny-transformer-scratch/blob/main/src/tiny_transformer_scratch/autograd.py) | [M1](https://github.com/EquinoxWN/tiny-transformer-scratch/blob/main/docs/results/m1.md) |
| detection-as-code | [RFC 0001](https://github.com/EquinoxWN/detection-as-code/blob/main/docs/rfc/0001-design.md) | [0002 local evaluator before SIEM](https://github.com/EquinoxWN/detection-as-code/blob/main/docs/adr/0002-local-evaluator-before-siem.md) | [rules/](https://github.com/EquinoxWN/detection-as-code/tree/main/rules) | [M1](https://github.com/EquinoxWN/detection-as-code/blob/main/docs/results/m1.md) |
| secure-supply-chain | [RFC 0001](https://github.com/EquinoxWN/secure-supply-chain/blob/main/docs/rfc/0001-design.md) | [0002 pin by SHA, gate on critical](https://github.com/EquinoxWN/secure-supply-chain/blob/main/docs/adr/0002-pin-by-sha-fail-on-critical.md) | [.github/workflows](https://github.com/EquinoxWN/secure-supply-chain/tree/main/.github/workflows) | [M1](https://github.com/EquinoxWN/secure-supply-chain/blob/main/docs/results/m1.md) |
| multi-tenant-saas-core | [RFC 0001](https://github.com/EquinoxWN/multi-tenant-saas-core/blob/main/docs/rfc/0001-design.md) | [0002 transaction-local tenant context](https://github.com/EquinoxWN/multi-tenant-saas-core/blob/main/docs/adr/0002-transaction-local-tenant-context.md) | [migrations/](https://github.com/EquinoxWN/multi-tenant-saas-core/tree/main/migrations) | [M1](https://github.com/EquinoxWN/multi-tenant-saas-core/blob/main/docs/results/m1.md) |
| cdc-lakehouse | [RFC 0001](https://github.com/EquinoxWN/cdc-lakehouse/blob/main/docs/rfc/0001-design.md) | [0002 Apicurio, Confluent wire format](https://github.com/EquinoxWN/cdc-lakehouse/blob/main/docs/adr/0002-apicurio-registry-confluent-wire-format.md) | [src/](https://github.com/EquinoxWN/cdc-lakehouse/tree/main/src) | [M1](https://github.com/EquinoxWN/cdc-lakehouse/blob/main/docs/results/m1.md) |
| engineering-rfcs | [RFC 0001](docs/rfc/0001-design.md) | [0002 lint documents in CI](docs/adr/0002-lint-documents-in-ci.md) | [tools/check_docs.py](tools/check_docs.py) | [M1](docs/results/m1.md) |

Links point at each repository's `main` branch; they resolve once that repository is published.
