#!/bin/bash

# --- Block 1: action sentences, "Who" and "What did X verb?" questions ---

subjects=("boy" "dog" "chef" "lion" "squirrel" "bird" "cat" "rabbit" "bear" "girl" "man" "woman" "horse" "fox" "wolf")
verbs=("kicked" "baked" "chased" "bit" "caught" "ate" "carried" "dropped" "found" "grabbed" "lifted" "opened" "pulled" "pushed" "threw")
objects=("ball" "cookies" "cat" "man" "dog" "squirrel" "bird" "lion" "fish" "carrot" "pizza" "cake" "cheese" "egg" "apple" "banana" "bone" "stick" "leaf" "rock")

for subject in "${subjects[@]}"; do
  for verb in "${verbs[@]}"; do
    for object in "${objects[@]}"; do

      # Skip weird combos
      if [[ "$verb" == "baked" && "$object" != "cookies" && "$object" != "cake" && "$object" != "bread" ]]; then continue; fi
      if [[ "$verb" == "kicked" && "$object" != "ball" && "$object" != "rock" && "$object" != "stick" ]]; then continue; fi
      if [[ "$verb" == "bit" && "$object" != "man" && "$object" != "bone" && "$object" != "apple" ]]; then continue; fi
      if [[ "$verb" == "chased" && "$object" != "cat" && "$object" != "man" && "$object" != "dog" && "$object" != "bird" && "$object" != "squirrel" ]]; then continue; fi
      if [[ "$subject" == "$object" ]]; then continue; fi

      sentence="The $subject $verb the $object."

      echo -e "$sentence Q: Who $verb the $object? A: the $subject.<stop>"
      echo -e "$sentence Q: What did the $subject $verb? A: the $object.<stop>"
    done
  done
done

# --- Block 2: attribute sentences, "What was X?" and "What was the subject?" ---

attr_subjects=("cat" "dog" "car" "sky" "ball" "tree" "house" "box" "fish" "bird" "chair" "leaf" "stone" "flower" "boat" "sun" "cloud" "lake" "road" "horse" "rabbit" "lion" "wolf" "bear" "door" "wall" "roof" "floor" "lamp" "cup" "bag" "hat" "coat" "shoe" "book" "key" "bell" "ring" "rope" "flag")
adjectives=("red" "blue" "green" "yellow" "white" "black" "big" "small" "old" "new" "fast" "slow" "loud" "quiet" "bright" "dark" "cold" "warm" "heavy" "light" "tall" "short" "soft" "hard" "clean" "dirty" "wet" "dry" "sharp" "round" "flat" "thin" "thick" "long" "wide" "narrow" "deep" "broken" "lost" "empty")

for subject in "${attr_subjects[@]}"; do
  for adj in "${adjectives[@]}"; do
    sentence="The $subject was $adj."
    echo -e "$sentence Q: What was $adj? A: the $subject.<stop>"
    echo -e "$sentence Q: What was the $subject? A: $adj.<stop>"
  done
done
