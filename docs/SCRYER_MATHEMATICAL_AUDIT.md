# Scryer Exact Mathematical Audit for CHRONOSIGNATURES
### Checked with the Scryer math engine

---

## 1. Overview
Harmonia's Research Charter demands:
> *"The mathematics must preserve the distinction between a theorem, a measurement, and an open coordinate."*

To ground the harmonic voicings and rhythmic subdivisions of *CHRONOSIGNATURES* in exact algebraic geometry, every chord set and cyclic pulse was checked against the **Scryer** math engine. Unlike floating-point approximations, Scryer evaluates canonical chord necklace orbits, Forte prime forms, interval vectors, and maximally even rhythmic necklaces in exact rationals and combinatorial integers.

---

## 2. Rhythmic Necklace & Maximally Even Verifications

Scryer proves that Bjorklund Euclidean pulse distribution over a discrete cyclic lattice $\mathbb{Z}_N$ produces **maximally even** distributions:

| Rhythm Label | Query | Canonical Necklace | Period | Maximally Even? | Musical Role in Album |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **4/4 Tresillo / Bossa Drift** | `rhythm 3:8` | `00100101` | 8 | **Yes** | Track 01 (*Zero Temperature Limit*) |
| **4/4 UKG Syncopated Kick** | `rhythm 3:16` | `0000010000100001` | 16 | **Yes** | Track 02 (*Circulation on the Simplex*) |
| **7/8 Asymmetric Horizon Pulse** | `rhythm 3:7` | `0010101` | 7 | **Yes** | Track 03 (*Noncommutative Horizon*) |
| **4/4 Straight Backbeat Pulse** | `rhythm 4:16` | `0001000100010001` | 4 | **Yes** | Track 05 (*Cumulant Cascade*) |
| **Golden Ratio Pulse 5:8** | `rhythm 5:8` | `01011011` | 8 | **Yes** | Track 06 (*The Gauge-Corrected Heart*) |

### Mathematical Significance
- In Track 03 (*Noncommutative Horizon*), the $7/8$ time signature subdivides into 7 eighth notes. Scryer proves that 3 pulses over 7 steps has canonical necklace `0010101`, matching the classic Balkan / progressive $3+2+2$ asymmetrical pulse. This guarantees that rhythmic asymmetry is maximally dispersed without arbitrary clustering.
- In Track 02 (*Circulation on the Simplex*), 3 pulses over 16 sixteenth notes (`rhythm 3:16`) yields the canonical UK Garage 2-step syncopation pattern ($1000001000010000$), placing the syncopated secondary kick exactly on step 6 and step 11.

---

## 3. Harmonic Path & Interval Vector Audit

Scryer evaluated the canonical forms and interval vectors $\langle i_1, i_2, i_3, i_4, i_5, i_6 \rangle$ across every harmonic transition:

### Track 01: Zero Temperature Limit (F Lydian)
- **Fmaj9#11 (Lydian Tonic)**: `chord 0 4 7 11 2 6`
  - Canonical Form: `0 1 3 5 7 8`
  - Interval Vector: `2 3 2 3 4 1`
  - Symmetry: $2$ of $24$
  - *Observation*: Dense fifth/fourth content ($i_5 = 4$) and third content ($i_2 = 3, i_4 = 3$) creates shimmering, resonant consonant overtones with minimal harshness ($i_6 = 1$).
- **G9sus4 (Acoustic Fifth)**: `chord 0 5 7 10 2`
  - Canonical Form: `0 2 4 7 9`
  - Interval Vector: `0 3 2 1 4 0` (Zero minor seconds $i_1 = 0$, zero tritones $i_6 = 0$!)
  - *Observation*: Absolute open consonance serving as the suspended bridge.

### Track 02: Circulation on the Simplex (D Dorian)
- **Dm9 (Dorian Center)**: `chord 0 3 7 10 2`
  - Canonical Form: `0 1 3 5 8`
  - Interval Vector: `1 2 2 2 3 0`
  - Symmetry: $1$ of $24$
- **Em7b5 (Half-Diminished)**: `chord 0 3 6 10`
  - Canonical Form: `0 2 5 8`
  - Interval Vector: `0 1 2 1 1 1`
  - *Observation*: The presence of the tritone ($i_6 = 1$) drives the Hodge cycle current back to the Dorian tonic center.

### Track 06: The Gauge-Corrected Heart (Db Major)
- **Dbmaj9 (Golden Tonic)**: `chord 0 4 7 11 2`
  - Canonical Form: `0 1 3 5 8`
  - Interval Vector: `1 2 2 2 3 0`
- **Gbmaj9#11 (Subdominant IV)**: `chord 0 4 7 11 2 6`
  - Canonical Form: `0 1 3 5 7 8`
  - Interval Vector: `2 3 2 3 4 1`
  - Complement: `0 1 2 5 7 9` (The pentatonic complement!)
  - *Observation*: The complement of the Lydian hexachord is the diatonic pentatonic collection, confirming that the climax preserves universal scale containment.

---

## 4. Synthesis & Architectural Takeaways
Connecting Scryer's exact algebraic proofs with Harmonia reveals that procedural music generation benefits massively when:
1. **Rhythm generation uses exact necklace algorithms** rather than randomized masks, guaranteeing maximal evenness.
2. **Harmonic paths are scored by exact interval vectors**, allowing the search engine to optimize acoustic tension and release without ad-hoc subjective weights.
