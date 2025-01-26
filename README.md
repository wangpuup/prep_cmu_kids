# Prepare CMU Kids Splits
  
The official splits of the [CMU Kids dataset](https://catalog.ldc.upenn.edu/LDC97S63) are located at [espnet/egs2/cmu_kids/asr1/conf/file_list](https://github.com/espnet/espnet/tree/master/egs2/cmu_kids/asr1/conf/file_list).

Split files show utterance IDs of train, dev, and test splits. Each utterance ID is named in 8 characters (e.g., `fejm2ah2`). The first four characters indicate the speaker ID (e.g., `fejm`), and the following three characters indicate the prompt ID (e.g., `2ah`).

The official splits ensure non-overlapping speakers across train, test, and dev splits, while allowing overlapping prompts.

The recipe [filter_overlapping_prompt.sh](https://github.com/wangpuup/prep_cmu_kids/blob/main/filter_overlapping_prompt.sh) is for detecting and filtering out overlapping prompts that have been seen in the train and dev splits from the test splits.

---

## New Splits Overview

### 1. `splits_3797_671_712`

- Retains all utterances (5180 utterances, 9.1 hours) with non-overlapping speakers between test and train/dev splits.
- Allows a small portion of overlapping prompts between test and train/dev splits.
- Allows speaker and prompt overlaps between train and dev splits.

The recipe for generating train/dev/test splits is available at [splits_3797_671_712/make_splits.py](https://github.com/wangpuup/prep_cmu_kids/blob/main/splits_3797_671_712/make_splits.py).

|           | train | dev | test |
|-----------|-------|-----|------|
| # utterances | 3797  | 671 | 712  |
| # hours      | 6.69  | 1.21| 1.20  |

---

### 2. `splits_3784_84_207`

- Retains the same amount of training utterances as the official splits.
- Ensures non-overlapping speakers and prompts across train, test, and dev splits.

The recipe for generating train/dev/test splits is available at [splits_3784_84_207/make_splits.sh](https://github.com/wangpuup/prep_cmu_kids/blob/main/splits_3784_84_207/make_splits.sh).

|           | train | dev | test |
|-----------|-------|-----|------|
| # utterances | 3784  | 84  | 207  |
| # hours      | 6.73  | 0.21| 0.35 |

---

### 3. `splits_3116_155_207`

- Built upon the `splits_3784_84_207`.

The recipe for generating train/dev/test splits is available at [splits_3116_155_207/make_splits.sh](https://github.com/wangpuup/prep_cmu_kids/blob/main/splits_3116_155_207/make_splits.sh).

|           | train | dev | test |
|-----------|-------|-----|------|
| # utterances | 3116  | 155 | 207  |
| # hours      | 5.50   | 0.32| 0.35 |

