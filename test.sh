# Builds a list of emails that form the training set.
# Then concatenates them all into one big file
find text/ -type f | shuf -n 45251 > training_list
echo "hello" > training_concat_text
cat training_list | xargs cat >> training_concat_text
