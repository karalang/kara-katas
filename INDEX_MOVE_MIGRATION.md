# Index-move migration — corpus debt

`karac` now rejects moving a non-`Copy` element out of a container:
`let w = v[i]` where `v: Vec[String]` is `E0285` / `E_INDEX_MOVE_NON_COPY`.
The rule landed in the compiler as `kara@6a73afd10`
(*"feat(typecheck): reject moving a non-`Copy` element out of a container"*,
2026-08-27), closing `B-2026-08-26-21` and `B-2026-08-26-37`, and rides on
`ref` bindings over sequence elements (`kara@f545357b6`, `B-2026-08-26-36`).

**This is a deliberate tightening, not a regression.** `v[i]` is a borrow —
`Index.index` is `fn index(ref self, idx) -> ref T` — so binding one in value
position reads THROUGH a reference and needs `T: Copy`. A container is not
partially movable; there is no `Vec` with a hole in it. The rule is run-fatal,
so the interpreter cannot execute what codegen refuses.

That commit's migration "spans every Kāra corpus in the tree" — but
**`kara-katas` is a separate repo and was not migrated.**

## Extent (measured 2026-08-28, karac 0.1.0-dev.7481+g9b221e799)

`karac check` over every `.kara` in the corpus:

| | count |
|---|---:|
| `.kara` files checked | 942 |
| **failing** | **128** |
| distinct katas affected | 63 |
| of those, `bench/` inputs | **38** |

Every one of the 128 failures is `E_INDEX_MOVE_NON_COPY`. No other error class
appears — the corpus is otherwise clean against current main.

The 38 `bench/` files are the load-bearing ones: **a kata whose `bench/` input
is on this list cannot be re-benched until it is migrated**, because `bench.sh`
fails at the `karac build` step before hyperfine ever runs. That is how this was
found — kata #288 blocked mid-sweep while adding the M5 lane.

## The fix, and the one trap in it

`karac fix` offers `.clone()`. **Do not take it in a `bench/` file.** The C and
Rust mirrors borrow (`for w in &dict`, `let word = &pool[i]`; C passes
pointers), so cloning makes Kāra pay a per-iteration heap allocation that no
mirror pays and silently corrupts the cross-language comparison — a
benchmark-honesty violation, not just a style choice. Use `ref`:

```kara
let w = ref dict[i];              // was: let w = dict[i];
let word = ref pool[i % pool_n];  // was: let word = pool[i % pool_n];
```

`.clone()` is the right answer only where the binding genuinely needs an
independent owned value. Re-verify A/B (`run` == `KARAC_AUTO_PAR=0 build` ==
auto-par `build`) after each migration.

## Done

- `leetcode/201-300/288-unique-word-abbreviation/bench/uniqueabbr.kara` —
  migrated to `ref` 2026-08-28, A/B identical (`unique 573650`), bench re-run.
  Its five kata-level variants are **still on the list below.**

## Outstanding

### bench/ inputs — block a re-bench (38)

- `leetcode/1-100/100-same-tree/bench/same_tree.kara`
- `leetcode/1-100/17-letter-combinations-of-a-phone-number/bench/letter_combinations.kara`
- `leetcode/1-100/23-merge-k-sorted-lists/bench/divide_and_conquer.kara`
- `leetcode/1-100/39-combination-sum/bench/combination_sum.kara`
- `leetcode/1-100/40-combination-sum-ii/bench/combination_sum_ii.kara`
- `leetcode/1-100/46-permutations/bench/permutations.kara`
- `leetcode/1-100/47-permutations-ii/bench/permutations_ii.kara`
- `leetcode/1-100/48-rotate-image/bench/rotate_image.kara`
- `leetcode/1-100/49-group-anagrams/bench/group_anagrams.kara`
- `leetcode/1-100/73-set-matrix-zeroes/bench/set_matrix_zeroes.kara`
- `leetcode/1-100/76-minimum-window-substring/bench/minimum_window_substring.kara`
- `leetcode/1-100/95-unique-binary-search-trees-ii/bench/generate_trees.kara`
- `leetcode/1-100/95-unique-binary-search-trees-ii/bench/generate_trees_share.kara`
- `leetcode/1-100/97-interleaving-string/bench/interleave.kara`
- `leetcode/1-100/97-interleaving-string/bench/interleave_unchecked.kara`
- `leetcode/101-200/101-symmetric-tree/bench/is_symmetric.kara`
- `leetcode/101-200/102-binary-tree-level-order-traversal/bench/level_order.kara`
- `leetcode/101-200/103-binary-tree-zigzag-level-order-traversal/bench/zigzag.kara`
- `leetcode/101-200/104-maximum-depth-of-binary-tree/bench/max_depth.kara`
- `leetcode/101-200/107-binary-tree-level-order-traversal-ii/bench/level_order_bottom.kara`
- `leetcode/101-200/109-convert-sorted-list-to-binary-search-tree/bench/sorted_list_to_bst.kara`
- `leetcode/101-200/110-balanced-binary-tree/bench/is_balanced.kara`
- `leetcode/101-200/111-minimum-depth-of-binary-tree/bench/min_depth.kara`
- `leetcode/101-200/112-path-sum/bench/path_sum.kara`
- `leetcode/101-200/113-path-sum-ii/bench/path_sum_ii.kara`
- `leetcode/101-200/118-pascals-triangle/bench/generate.kara`
- `leetcode/101-200/124-binary-tree-maximum-path-sum/bench/max_path_sum.kara`
- `leetcode/101-200/126-word-ladder-ii/bench/word_ladder_ii.kara`
- `leetcode/101-200/127-word-ladder/bench/word_ladder.kara`
- `leetcode/101-200/129-sum-root-to-leaf-numbers/bench/sum_numbers.kara`
- `leetcode/101-200/131-palindrome-partitioning/bench/palindrome_partitioning.kara`
- `leetcode/101-200/132-palindrome-partitioning-ii/bench/min_cut.kara`
- `leetcode/201-300/218-the-skyline-problem/bench/skyline.kara`
- `leetcode/201-300/241-different-ways-to-add-parentheses/bench/different_ways.kara`
- `leetcode/201-300/244-shortest-word-distance-ii/bench/shortest_distance_ii.kara`
- `leetcode/201-300/248-strobogrammatic-number-iii/bench/strobogrammatic_count.kara`
- `leetcode/201-300/290-word-pattern/bench/word_pattern.kara`
- `leetcode/301-400/332-reconstruct-itinerary/bench/reconstruct_itinerary.kara`

### kata-level files (90)

- `backend/todo-api/main.kara`
- `leetcode/1-100/100-same-tree/same_tree.kara`
- `leetcode/1-100/100-same-tree/same_tree_serial.kara`
- `leetcode/1-100/17-letter-combinations-of-a-phone-number/letter_combinations.kara`
- `leetcode/1-100/23-merge-k-sorted-lists/divide_and_conquer.kara`
- `leetcode/1-100/47-permutations-ii/permutations_ii_swap.kara`
- `leetcode/1-100/48-rotate-image/rotate_image.kara`
- `leetcode/1-100/48-rotate-image/rotate_image_flip.kara`
- `leetcode/1-100/48-rotate-image/rotate_image_fresh.kara`
- `leetcode/1-100/48-rotate-image/rotate_image_transpose.kara`
- `leetcode/1-100/49-group-anagrams/count_signature.kara`
- `leetcode/1-100/49-group-anagrams/map_of_lists.kara`
- `leetcode/1-100/49-group-anagrams/sorted_key.kara`
- `leetcode/1-100/51-n-queens/bitmask.kara`
- `leetcode/1-100/51-n-queens/conflict_scan.kara`
- `leetcode/1-100/51-n-queens/marker_arrays.kara`
- `leetcode/1-100/54-spiral-matrix/spiral_boundary.kara`
- `leetcode/1-100/54-spiral-matrix/spiral_steps.kara`
- `leetcode/1-100/54-spiral-matrix/spiral_visited.kara`
- `leetcode/1-100/68-text-justification/text_justification.kara`
- `leetcode/1-100/68-text-justification/text_justification_twophase.kara`
- `leetcode/1-100/73-set-matrix-zeroes/set_matrix_zeroes.kara`
- `leetcode/1-100/73-set-matrix-zeroes/set_matrix_zeroes_markers.kara`
- `leetcode/1-100/77-combinations/combinations.kara`
- `leetcode/1-100/77-combinations/combinations_bitmask.kara`
- `leetcode/1-100/77-combinations/combinations_pruned.kara`
- `leetcode/1-100/78-subsets/subsets.kara`
- `leetcode/1-100/78-subsets/subsets_iterative.kara`
- `leetcode/1-100/90-subsets-ii/subsets_ii.kara`
- `leetcode/1-100/90-subsets-ii/subsets_ii_iterative.kara`
- `leetcode/1-100/95-unique-binary-search-trees-ii/generate_trees.kara`
- `leetcode/1-100/95-unique-binary-search-trees-ii/generate_trees_dp.kara`
- `leetcode/1-100/97-interleaving-string/interleave.kara`
- `leetcode/1-100/97-interleaving-string/interleave_rolling.kara`
- `leetcode/101-200/102-binary-tree-level-order-traversal/level_order.kara`
- `leetcode/101-200/102-binary-tree-level-order-traversal/level_order_bfs.kara`
- `leetcode/101-200/102-binary-tree-level-order-traversal/level_order_bylevel.kara`
- `leetcode/101-200/103-binary-tree-zigzag-level-order-traversal/zigzag.kara`
- `leetcode/101-200/103-binary-tree-zigzag-level-order-traversal/zigzag_bfs.kara`
- `leetcode/101-200/107-binary-tree-level-order-traversal-ii/level_order_bottom.kara`
- `leetcode/101-200/107-binary-tree-level-order-traversal-ii/level_order_bottom_bfs.kara`
- `leetcode/101-200/118-pascals-triangle/generate.kara`
- `leetcode/101-200/118-pascals-triangle/generate_binomial.kara`
- `leetcode/101-200/126-word-ladder-ii/word_ladder_ii.kara`
- `leetcode/101-200/127-word-ladder/word_ladder.kara`
- `leetcode/101-200/131-palindrome-partitioning/palindrome_partitioning.kara`
- `leetcode/101-200/132-palindrome-partitioning-ii/min_cut.kara`
- `leetcode/101-200/140-word-break-ii/word_break_ii.kara`
- `leetcode/101-200/171-excel-sheet-column-number/column_number.kara`
- `leetcode/101-200/171-excel-sheet-column-number/column_number_recursive.kara`
- `leetcode/101-200/179-largest-number/largest_number.kara`
- `leetcode/201-300/207-course-schedule/course_schedule.kara`
- `leetcode/201-300/210-course-schedule-ii/course_schedule_ii.kara`
- `leetcode/201-300/212-word-search-ii/word_search_ii.kara`
- `leetcode/201-300/216-combination-sum-iii/combination_sum_iii.kara`
- `leetcode/201-300/218-the-skyline-problem/skyline.kara`
- `leetcode/201-300/244-shortest-word-distance-ii/shortest_distance_pool.kara`
- `leetcode/201-300/245-shortest-word-distance-iii/differential.kara`
- `leetcode/201-300/247-strobogrammatic-number-ii/strobogrammatic_ii.kara`
- `leetcode/201-300/248-strobogrammatic-number-iii/differential.kara`
- `leetcode/201-300/248-strobogrammatic-number-iii/strobogrammatic_count.kara`
- `leetcode/201-300/248-strobogrammatic-number-iii/strobogrammatic_iii.kara`
- `leetcode/201-300/249-group-shifted-strings/differential.kara`
- `leetcode/201-300/249-group-shifted-strings/group_shifted.kara`
- `leetcode/201-300/249-group-shifted-strings/group_shifted_diffkey.kara`
- `leetcode/201-300/261-graph-valid-tree/differential.kara`
- `leetcode/201-300/261-graph-valid-tree/graph_valid_tree.kara`
- `leetcode/201-300/261-graph-valid-tree/graph_valid_tree_bfs.kara`
- `leetcode/201-300/261-graph-valid-tree/graph_valid_tree_peel.kara`
- `leetcode/201-300/265-paint-house-ii/differential.kara`
- `leetcode/201-300/269-alien-dictionary/differential.kara`
- `leetcode/201-300/271-encode-and-decode-strings/encode_decode.kara`
- `leetcode/201-300/271-encode-and-decode-strings/encode_decode_fixed.kara`
- `leetcode/201-300/278-alien-dictionary/differential.kara`
- `leetcode/201-300/280-wiggle-sort/wiggle_sort.kara`
- `leetcode/201-300/280-wiggle-sort/wiggle_sort_brute.kara`
- `leetcode/201-300/280-wiggle-sort/wiggle_sort_sorted.kara`
- `leetcode/201-300/282-expression-add-operators/add_operators.kara`
- `leetcode/201-300/282-expression-add-operators/add_operators_enumerate.kara`
- `leetcode/201-300/282-expression-add-operators/differential.kara`
- `leetcode/201-300/288-unique-word-abbreviation/differential.kara`
- `leetcode/201-300/288-unique-word-abbreviation/unique_word_abbr.kara`
- `leetcode/201-300/288-unique-word-abbreviation/unique_word_abbr_brute.kara`
- `leetcode/201-300/288-unique-word-abbreviation/unique_word_abbr_buckets.kara`
- `leetcode/201-300/288-unique-word-abbreviation/unique_word_abbr_counts.kara`
- `leetcode/201-300/290-word-pattern/word_pattern.kara`
- `leetcode/301-400/332-reconstruct-itinerary/reconstruct_itinerary.kara`
- `oracle/recursive-owned-string-param-uaf/ablations/a1-local-binding-STILL-FAILS.kara`
- `oracle/recursive-owned-string-param-uaf/ablations/a2-no-map-PASSES.kara`
- `oracle/recursive-owned-string-param-uaf/repro.kara`
