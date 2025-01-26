import pandas as pd
import random
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

# Shuffle remaining utterances
random.shuffle(remaining_utterances)

# Split remaining utterances into train and dev sets (85% train, 15% dev)
train_split_index = int(0.85 * len(remaining_utterances))
utterances_train, utterances_dev = remaining_utterances[:train_split_index], remaining_utterances[train_split_index:]

# Ensure no overlapping speaker IDs between train and dev sets
train_speaker_ids = set(u[:4] for u in utterances_train)
filtered_dev = [u for u in utterances_dev if u[:4] not in train_speaker_ids]

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

