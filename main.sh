TRAINING_TEXT=training_concat_text
TRAINING_LIST=training_list
TEST_LIST=test_set_list
DICT_FILE=dictionary
WORD_COUNT=35000
NUM_TRAIN=45251
DATA_PATH=trec07p/data/
TEXT_PATH=text/
# strip the text parts from the emails
find "$DATA_PATH" -type f | xargs ./strip_mail.py
# Build a list of emails that form the training set.
# Then concatenate them all into one big file.
# this also builds the test set list
find "$TEXT_PATH" -type f | shuf -n "$NUM_TRAIN" > "$TRAINING_LIST"
find "$TEXT_PATH" -type f > "$TEST_LIST"
diff --new-line-format="" --unchanged-line-format="" <(sort test_set_list) <(sort "$TRAINING_LIST") > "$TEST_LIST"

echo "hello" > "$TRAINING_TEXT"
cat "$TRAINING_LIST" | xargs cat >> "$TRAINING_TEXT"
# now run build_dict.py on the training text
./build_dict.py "$TRAINING_TEXT" "$DICT_FILE" "$WORD_COUNT"
