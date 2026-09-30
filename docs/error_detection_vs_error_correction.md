# Error Detection and Error Correction

## Error detection

An error-detection scheme adds or computes redundant information that lets a receiver test whether a received word satisfies a validity condition. A failed check signals that something may have changed; it need not identify the location or original value of the error.

- **Checksums and check digits** compress data into a smaller check value. A match can still occur after an alteration, depending on the construction and error pattern.
- **Parity** adds a bit chosen to make the number of 1s even or odd. A single bit flip changes parity, but an even number of flips can preserve it. A single parity bit does not identify which bit changed.
- **Cyclic redundancy checks (CRCs)** use polynomial arithmetic over binary symbols and append a remainder. Their guarantees depend on the generator polynomial and frame length. A CRC check by itself detects a failed check; it does not reconstruct the sent data. A system may separately use an error-correction mechanism. [RFC 3385](https://www.rfc-editor.org/rfc/rfc3385.html) is an informational analysis of CRC32C for iSCSI, and [RFC 3720](https://www.rfc-editor.org/rfc/rfc3720.html) includes CRC32C as an iSCSI digest option. [RFC 1071](https://www.rfc-editor.org/rfc/rfc1071.html) specifies the Internet one's-complement checksum, a different checksum construction.

Detection guarantees are conditional. A code with minimum Hamming distance `d_min` detects any pattern of at most `d_min - 1` symbol errors, but the decoder or verifier must know the code and its received word model.

## Error correction

An error-correcting code chooses codewords with sufficient separation that a decoder can infer the transmitted codeword when the received word is within its guaranteed distance. A code with minimum distance `d_min` can uniquely correct up to `floor((d_min - 1)/2)` symbol errors under the usual bounded-distance model. Correction requires redundancy and a decoding rule; detecting a mismatch by itself is not correction.

- **Hamming codes** add structured parity bits. The classic construction corrects one bit error; extended variants can add an overall parity bit to support single-error correction and double-error detection. Hamming's 1950 paper explicitly treats both detection and correction ([original article](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x)).
- **Reed–Solomon codes** treat blocks as symbols over a finite field and use polynomial evaluation constraints. Under standard Reed–Solomon bounded-distance decoding assumptions, let `r` be the number of parity symbols, `t` the number of unknown symbol errors, and `e` the number of known erasures. The usual correction condition is `2t + e <= r`. The foundational paper is Reed and Solomon, [“Polynomial Codes Over Certain Finite Fields”](https://doi.org/10.1137/0108018), 1960.

## Why this project is error detection

The project maps a decimal string to an integer residue modulo `m`, then marks a modeled alteration detected when its residue differs. It does not add correction redundancy that identifies the altered digit, locate an error, or reconstruct the original string. The modulus 11 result proves detection for the two defined error models; it does not provide an error-correction procedure.

## Integrity and adversaries

Accidental-error checks are not automatically secure against intentional modification. Cryptographic hashes provide a different integrity tool, and a keyed message authentication code can additionally authenticate the source when keys are managed correctly. NIST distinguishes approved hash functions and MAC mechanisms in its [Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) and [MAC guidance](https://csrc.nist.gov/Projects/message-authentication-codes). These are outside the project's algorithmic scope.
