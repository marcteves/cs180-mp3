# Builds a list of emails that form the training set.
# Then concatenates them all into one big file
# this also builds the test set list
find text/ -type f | shuf -n 45251 > training_list
find text/ -type f > test_set_list
diff --new-line-format="" --unchanged-line-format="" <(sort test_set_list) <(sort training_list) > test_set_list

echo "hello" > training_concat_text
cat training_list | xargs cat >> training_concat_text
