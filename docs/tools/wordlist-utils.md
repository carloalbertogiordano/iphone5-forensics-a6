# Wordlist Utilities (paroleitaliane)

## Purpose
Collection of Italian wordlists and associated scripts for generating dictionaries, brute-force attacks, and linguistic analysis. Includes utilities to create unique word lists, ZIP archives, and maintain the collection.

## Key Features
- Multiple wordlist files catering to different use cases: common words, compound words, profanity, proper nouns, surnames, verb conjugations.
- Specialized `bruteforce.txt` wordlist containing:
  - All possible six-digit birthdate combinations (DDMMYY format).
  - Italian dictionary words.
  - All six-digit numeric combinations (000000-999999).
  - Profanity and common English terms used in Italy.
  - Frequently observed passwords (e.g., `qwertyuio`).
- Scripts to regenerate derived files (`parole_uniche.txt`) and recreate ZIP archives.
- All files use UTF-8 encoding, LF line endings, no duplicates, sorted with Italian collation (`it_IT.UTF-8`).

## Core Files
- **Wordlist categories**:
  - `400_parole_composte.txt`: Hyphenated compound words.
  - `lista_badwords.txt`: Profanity and vulgar terms.
  - `1000_parole_italiane_comuni.txt`: Most common Italian words.
  - `9000_nomi_propri.txt`: Personal names.
  - `lista_38000_cognomi.txt`: Italian surnames.
  - `60000_parole_italiane.txt`: Common Italian words.
  - `95000_parole_italiane_con_nomi_propri.txt`: Words plus proper nouns and locations.
  - `110000_parole_italiane_con_nomi_propri.txt`: Extended word list with proper nouns and foreign terms.
  - `lista_cognomi.txt`: Italian and foreign surnames.
  - `280000_parole_italiane.txt`: Inflected forms of Italian words.
  - `coniugazione_verbi.txt`: Verb conjugations (CC BY-SA 3.0 licensed).
  - `660000_parole_italiane.txt`: Largest list of pure Italian words.
  - `parole_uniche.txt`: Deduplicated union of all lists (generated).
  - `bruteforce.txt`: Specialized brute-force wordlist (separate directory).
- **Scripts**:
  - `scripts/genera_parole_uniche.sh`: Regenerates `parole_uniche.txt`.
  - `scripts/crea_zip.sh`: Recreates `paroleitaliane.zip` and `bruteforce.zip`.

## Usage
- Use any `.txt` file directly as a dictionary for password cracking, linguistic analysis, or game development.
- For brute-force attacks on iOS passcodes, utilize `bruteforce.txt` which includes common patterns like birthdates and numeric sequences.
- To update the collection after adding/modifying word files, run the regeneration scripts:
  ```bash
  ./scripts/genera_parole_uniche.sh
  ./scripts/crea_zip.sh
  ```
  Note: The unique word script requires the `it_IT.UTF-8` locale.

## Building
No compilation required; the repository consists of plain text files and shell scripts.

## Dependencies
- Standard Unix shell (bash).
- Core utilities (`sort`, `uniq`, `zip`).
- Italian locale (`it_IT.UTF-8`) for proper sorting in regeneration scripts.

## References
- Original README: `wordlist/paroleitaliane/README.md`
- Verb data source: https://github.com/ian-hamlin/verb-data (CC BY-SA 3.0)
- Archives: `paroleitaliane.zip`, `bruteforce.zip` in the repository root.