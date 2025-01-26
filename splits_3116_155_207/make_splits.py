import pandas as pd
import re
from collections import defaultdict

# Load sentence.tbl into a DataFrame
sentence_file = "sentence.tbl"
sentence_data = []
with open(sentence_file, "r") as f:
    for line in f:
        parts = line.strip().split("\t")
        sentence_data.append((parts[0], int(parts[1]), parts[2]))
sentence_df = pd.DataFrame(sentence_data, columns=["PromptID", "Frequency", "Sentence"])

# Load total.list into a list
total_file = "total.list"
utterances = []
with open(total_file, "r") as f:
    for line in f:
        utterances.append(line.strip())

# Parse utterance IDs into a dictionary mapping prompt IDs to speaker IDs
utterance_map = defaultdict(list)
for utterance in utterances:
    speaker_id = utterance[:4]
    prompt_id = utterance[4:7]
    utterance_map[prompt_id].append(speaker_id)

# Ensure no overlapping speaker IDs across sets
used_speaker_ids = set()

# 1. Identify test set prompt IDs
prompt_test_ids = set(sentence_df[sentence_df["Frequency"] <= 2]["PromptID"])

# 2. Identify speaker IDs for test set
speaker_test_ids = set()
for prompt_id in prompt_test_ids:
    speaker_test_ids.update(utterance_map[prompt_id])
speaker_test_ids -= used_speaker_ids
used_speaker_ids.update(speaker_test_ids)

# 3. Filter utterances for test set
utterances_test = [u for u in utterances if u[:4] in speaker_test_ids]

# Remove test set utterances from further processing
remaining_utterances = [u for u in utterances if u not in utterances_test]

# 4. Identify dev set prompt IDs
remaining_prompt_ids = {u[4:7] for u in remaining_utterances}
remaining_prompt_freq = sentence_df[sentence_df["PromptID"].isin(remaining_prompt_ids)]
prompt_dev_ids = set(remaining_prompt_freq[(remaining_prompt_freq["Frequency"] >= 3) & (remaining_prompt_freq["Frequency"] <= 9)]["PromptID"])

# 5. Identify speaker IDs for dev set
speaker_dev_ids = set()
for prompt_id in prompt_dev_ids:
    speaker_dev_ids.update(utterance_map[prompt_id])
speaker_dev_ids -= used_speaker_ids
used_speaker_ids.update(speaker_dev_ids)

# Filter utterances for dev set
utterances_dev = [u for u in remaining_utterances if u[:4] in speaker_dev_ids]

# Remaining utterances are for the train set
utterances_train = [u for u in remaining_utterances if u[:4] not in used_speaker_ids]

# Save to files
def save_list(filename, data):
    with open(filename, "w") as f:
        for item in data:
            f.write(f"{item}\n")

save_list("train.list", utterances_train)
save_list("dev.list", utterances_dev)
save_list("test.list", utterances_test)

print(f"Train set: {len(utterances_train)} utterances")
print(f"Dev set: {len(utterances_dev)} utterances")
print(f"Test set: {len(utterances_test)} utterances")

