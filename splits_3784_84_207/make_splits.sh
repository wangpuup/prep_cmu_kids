#!/bin/bash
  
# Define file paths
SENTENCE_FILE="sentence.tbl" #from ldc97s63/cmu_kids/tables/sentence.tbl
TOTAL_FILE="total.list"
TRAIN_FILE="train.list"
DEV_FILE="dev.list"
TEST_FILE="test.list"

python3 ./make_splits.py

# Filter prompt IDs seen in train and dev sets from test set
TEMP_TEST_FILE="test.temp"
TEMP_DEV_FILE="dev.temp"

TRAIN_PROMPTS=$(cut -c5-7 "$TRAIN_FILE" | sort | uniq)
DEV_PROMPTS=$(cut -c5-7 "$DEV_FILE" | sort | uniq)

# Filter test set
grep -v -f <(echo "$TRAIN_PROMPTS") "$TEST_FILE" | grep -v -f <(echo "$DEV_PROMPTS") > "$TEMP_TEST_FILE"
mv "$TEMP_TEST_FILE" "$TEST_FILE"

# Filter dev set
grep -v -f <(echo "$TRAIN_PROMPTS") "$DEV_FILE" > "$TEMP_DEV_FILE"
mv "$TEMP_DEV_FILE" "$DEV_FILE"

# Output results
echo "Filtered test set saved to $TEST_FILE"
echo "Filtered dev set saved to $DEV_FILE"
