---
name: data-card
description: Use when adding or first using a dataset (ISLR, ASL Fingerspelling, a public letter set, ASL Citizen). Creates docs/data_cards/<source>.md with only measured or documented facts before any training use.
---

# Data card

CLAUDE.md requires a data card in `docs/data_cards/` for every source before it is used. File name: `docs/data_cards/<source>.md`.

## Rules
- Every number comes from a script you ran (paste the command and the commit) or from the dataset's own documentation (cite the page). If it is not measured yet, write `not measured yet`. Never estimate.
- You usually cannot open Kaggle pages or accept rules for the user. Ask the user for the license and competition rules text, or for confirmation that they accepted the rules. Do not guess a license.
- Never commit dataset files, samples or thumbnails (rule 7). The card holds statistics and links only.
- Participant data is out of scope here (rule 8); own recordings get their counts by pseudonymous ID only.

## Template

```markdown
# Data card: <source>

- Card date / commit:
- Link:
- License and usage rules (quote or link):
- Download steps (reproducible, including the Kaggle rules acceptance):
- Size on disk (raw / after conversion to clip format):

## Content
- Classes and counts per class:
- Number of signers (or "no signer IDs"):
- Split key used (`participant_id`, person, none) and how the grouped split is built:
- Handedness mix (left / right / unknown):
- Share of frames with no detected hand:
- Frame size known? (width x height, or unknown and the assumption tested)
- Extractor that produced the landmarks (name, version, model file) and whether it matches our pinned Tasks extractor:

## Quality
- Near-duplicates found (method, count):
- Signer diversity notes (skin tone, lighting, backgrounds, age if documented):
- Label noise or known errors:
- Anything that makes a random split leaky:

## Sampling (letter image sets)
- Sample size per class, sample seed, path to the list of chosen files:

## Decision
- Used for: (training / validation / not used)
- Reason and alternatives rejected (also add a dated entry to `docs/decisions.md`):
```

## Steps
1. Check for an existing card; update it rather than creating a second.
2. Fill the documented facts first; run the measuring script (put it in `src/asl/`, not in a notebook) for the rest.
3. Save the card, add the `docs/decisions.md` entry, commit as `docs(data): add data card for <source>` on a `docs/data-card-<source>` branch, open a PR.
