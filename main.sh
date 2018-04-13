source config.sh
# just in case git removes file permissions
chmod +x *.py
# strip the text parts from the emails
find "$DATA_PATH" -type f | xargs ./strip_mail.py
# Build a list of emails that form the training set.
# Then concatenate them all into one big file.
find "$TEXT_PATH" -type f | shuf -n "$NUM_TRAIN" > "$TRAINING_LIST"
# sort training list according to version sort
cat "$TRAINING_LIST" | sort -V > "$TRAINING_LIST".$$
mv "$TRAINING_LIST".$$ "$TRAINING_LIST"
# build the test set list
find "$TEXT_PATH" -type f > "$TEST_LIST"
# take every line in file list that isn't in training list
diff --new-line-format="%L" --unchanged-line-format="" <(sort "$TRAINING_LIST") <(sort "$TEST_LIST") > "$TEST_LIST".$$
mv "$TEST_LIST".$$ "$TEST_LIST"
# sort test list according to version sort
cat "$TEST_LIST" | sort -V > "$TEST_LIST".$$
mv "$TEST_LIST".$$ "$TEST_LIST"

# obtain ham spam vectors for each list file
./ham_spam_read.py "$REFERENCE" "$TRAIN_HS" "$TRAIN_LIST"
./ham_spam_read.py "$REFERENCE" "$TEST_HS" "$TEST_LIST"

echo "hello" > "$TRAINING_TEXT"
cat "$TRAINING_LIST" | xargs cat >> "$TRAINING_TEXT"
# now run build_dict.py on the training text
./build_dict.py "$TRAINING_TEXT" "$DICT_FILE" "$WORD_COUNT"

# save feature vectors in compressed format
./build_vectors.py "$DICT_FILE" "$TRAINING_CSV" "$TRAIN_LIST"
./build_vectors.py "$DICT_FILE" "$TEST_CSV" "$TEST_LIST"
