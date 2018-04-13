source config.sh
./classify.py "$TRAIN_CSV".npz "$TRAIN_HS" "$TEST_CSV".npz "$TEST_HS" 
./classify.py "$TRAIN_CSV""$SUFFIX_NOSTOP".npz "$TRAIN_HS" "$TEST_CSV""$SUFFIX_NOSTOP".npz "$TEST_HS" 
./classify.py "$TRAIN_CSV""$SUFFIX_STEM".npz "$TRAIN_HS" "$TEST_CSV""$SUFFIX_STEM".npz "$TEST_HS" 
