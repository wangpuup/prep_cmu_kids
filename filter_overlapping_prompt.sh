#!/bin/bash

# Define file paths
test_file="test.list"
train_file="train.list"
dev_file="dev.list"

# Temporary files to store filtered content
temp_train="train_filtered.list"
temp_dev="dev_filtered.list"
temp_test="test_filtered.list"

cp "$train_file" "$temp_train"
cp "$dev_file" "$temp_dev"
cp "$test_file" "$temp_test"

# Extract prompt IDs from train.list
train_prompt_ids=$(cut -c 5-7 "$train_file" | sort | uniq)

#Extract prompt IDs from dev.list
dev_prompt_ids==$(cut -c 5-7 "$dev_file" | sort | uniq)

# Filter test.list
for id in $train_prompt_ids; do
    grep -v ".\{3\}$id" "$temp_test" > "${temp_test}_new" && mv "${temp_test}_new" "$temp_test"
    echo "filtered out prompt $id from test.list"
done

for id in $dev_prompt_ids; do
    grep -v ".\{3\}$id" "$temp_test" > "${temp_test}_new" && mv "${temp_test}_new" "$temp_test"
    echo "filtered out prompt $id from test.list"
done

# Replace the original files with the filtered files
mv "$temp_train" "$train_file"
mv "$temp_dev" "$dev_file"
mv "$temp_test" "$test_file"

echo "Filtered test.list successfully."
