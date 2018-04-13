source config.sh
# just in case git removes file permissions
chmod +x *.py
# strip the text parts from the emails
find "$DATA_PATH" -type f | xargs ./strip_mail.py
# Build a list of emails that form the training set.
# Then concatenate them all into one big file.
find "$TEXT_PATH" -type f | shuf -n "$NUM_TRAIN" > "$TRAIN_LIST"
# sort training list according to version sort
cat "$TRAIN_LIST" | sort -V > "$TRAIN_LIST".$$
mv "$TRAIN_LIST".$$ "$TRAIN_LIST"
# build the test set list
find "$TEXT_PATH" -type f > "$TEST_LIST"
# take every line in file list that isn't in training list
diff --new-line-format="%L" --unchanged-line-format="" <(sort "$TRAIN_LIST") <(sort "$TEST_LIST") > "$TEST_LIST".$$
mv "$TEST_LIST".$$ "$TEST_LIST"
# sort test list according to version sort
cat "$TEST_LIST" | sort -V > "$TEST_LIST".$$
mv "$TEST_LIST".$$ "$TEST_LIST"

# obtain ham spam vectors for each list file
./ham_spam_read.py "$REFERENCE" "$TRAIN_HS" "$TRAIN_LIST"
./ham_spam_read.py "$REFERENCE" "$TEST_HS" "$TEST_LIST"

echo "hello" > "$TRAIN_TEXT"
cat "$TRAIN_LIST" | xargs cat >> "$TRAIN_TEXT"
# now run build_dict.py on the training text
./build_dict.py "$TRAIN_TEXT" "$DICT_FILE" "$WORD_COUNT"

# save feature vectors in compressed format
./build_vectors.py "$DICT_FILE" "$TRAIN_CSV" "$TRAIN_LIST"
./build_vectors.py "$DICT_FILE" "$TEST_CSV" "$TEST_LIST"

# Now classify
./classify.py "$TRAIN_CSV".npz "$TRAIN_HS" "$TEST_CSV".npz "$TEST_HS" out
