# Wordlist

This folder held the custom Italian wordlists and candidate-password lists used for
the brute-force phase of this project (see `docs/` findings for methodology).

Content has been removed from this public tree: the lists were built (in part) from
real personal names and data related to the device owner, and are not appropriate to
publish. Kept locally only, outside the repo.

## What was here

- A base Italian word dictionary, sourced from
  [napolux/paroleitaliane](https://github.com/napolux/paroleitaliane) (no license file
  found upstream at time of use; author notes some lists are of unknown/recovered
  provenance — see their README).
- `genera_wordlist.py` — a script generating name/date/pattern-derived candidate
  passwords (mangling rules: capitalization, suffixes, leet substitutions, etc.) from a
  base name and known personal details.
- Generated candidate lists split by length/type (numeric PINs, 5-6 char, 7 char, etc.)
  used to drive the brute-force runs.
- A progress screenshot of a live brute-force run (non-sensitive, terminal output only).

## Reproducing

The generation approach is documented in the project's findings/brute-force report
under `docs/`. To rebuild a similar wordlist for your own research, clone
`paroleitaliane` as a base dictionary and write comparable mangling rules — do not
reuse another person's private wordlist.
