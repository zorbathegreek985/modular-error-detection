# A Short History of Error Checks and Check Digits

This is a selective educational timeline, not a claim that each entry marks the invention of its field.

| Date | Development | Context |
|---|---|---|
| By 1950 | Parity and other simple error-detecting codes were established coding topics. | Hamming's 1950 paper discusses existing codes for isolated-error detection before developing detection and correction constructions. It is a documented reference point, not an origin claim. ([Hamming, 1950](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x)) |
| 1950 | Hamming publishes a systematic treatment of error-detecting and error-correcting codes. | The paper presents constructions for detecting and correcting errors in digital communication. ([Hamming, 1950](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x)) |
| 1954 / 1960 | Hans P. Luhn files and receives a patent for a number-verification device. | The patent application was filed in 1954 and granted in 1960. The apparatus calculates or verifies an appended check digit. ([US 2,950,048](https://patents.google.com/patent/US2950048A/en)) |
| 1960 | Reed and Solomon publish polynomial codes over finite fields. | Their work became a foundation for symbol-oriented error-correcting codes. ([Reed & Solomon, 1960](https://doi.org/10.1137/0108018)) |
| 1961 | Peterson and Brown publish a treatment of cyclic codes for error detection. | The paper describes polynomial methods and error-detection potential for cyclic codes, an important line of work underlying CRC practice. ([Peterson & Brown, 1961](https://doi.org/10.1109/JRPROC.1961.287814)) |
| 1969 | Jacobus Verhoeff publishes *Error Detecting Decimal Codes*. | The monograph develops decimal error-detecting codes and is the primary reference for the Verhoeff check-digit method. ([CWI record](https://ir.cwi.nl/pub/13045)) |
| 1983 / 2003 | ISO 7064 editions define standardized check-character systems. | ISO lists the earlier ISO 7064:1983 and ISO/IEC 7064:2003, covering specified pure and hybrid systems. ([ISO record](https://www.iso.org/standard/31531.html)) |
| 1988 | The Internet checksum is specified in RFC 1071. | RFC 1071 describes a one's-complement sum over 16-bit words; this is distinct from a CRC. ([RFC 1071](https://www.rfc-editor.org/rfc/rfc1071.html)) |
| 2000 | Damm publishes work on check-digit systems over groups and anti-symmetric mappings. | The paper characterizes conditions for such group-based check-digit systems to detect single errors and adjacent transpositions. ([Damm, 2000](https://doi.org/10.1007/s000130050524)) |
| 2002 / 2004 | CRC32C is analyzed for iSCSI and included as an iSCSI digest option. | RFC 3385 (2002) is an informational analysis of CRC32C and checksum choices; it is not an Internet Standards Track specification. RFC 3720 (2004) specifies iSCSI and includes CRC32C as a digest option. ([RFC 3385](https://www.rfc-editor.org/rfc/rfc3385.html), [RFC 3720](https://www.rfc-editor.org/rfc/rfc3720.html)) |
| Modern systems | Checksums, CRCs, cryptographic hashes, MACs, and error-correcting codes serve different integrity needs. | Standards distinguish non-keyed message digests from keyed authentication mechanisms; neither category should be conflated with a decimal check digit. ([NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final), [NIST MAC overview](https://csrc.nist.gov/Projects/message-authentication-codes)) |

## Reading the timeline

The entries mark selected publications, patents, or standards rather than a complete history. “Checksum” is used broadly in engineering, while a check digit is a small specialized value for character strings. CRCs use polynomial remainders; Internet checksums use one's-complement addition; cryptographic hashes and MACs have security properties that ordinary error checks do not provide.
