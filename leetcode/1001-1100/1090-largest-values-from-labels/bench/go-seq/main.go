// Benchmark: LeetCode #1090 Largest Values From Labels -- Go mirror of the ★
// arm: (value, label) pairs sorted by value from the largest
// (slices.SortStableFunc, stable as Kāra's `sort_by`), taken while their label
// has uses left (a map of uses per label). Same workload and sink as
// ../largest_values_from_labels.kara.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type item struct{ value, label int64 }

func largestValsFromLabels(values, labels []int64, numWanted, useLimit int64) int64 {
	items := make([]item, 0)
	for i := range values {
		items = append(items, item{values[i], labels[i]})
	}
	slices.SortStableFunc(items, func(a, b item) int { return cmp.Compare(b.value, a.value) })
	used := map[int64]int64{}
	var taken, sum int64
	for _, it := range items {
		if taken == numWanted {
			break
		}
		uses := used[it.label]
		if uses < useLimit {
			used[it.label] = uses + 1
			sum += it.value
			taken++
		}
	}
	return sum
}

var seed int64 = 1090

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	values := make([][]int64, 100)
	labels := make([][]int64, 100)
	for k := 0; k < 100; k++ {
		for i := 0; i < 20000; i++ {
			values[k] = append(values[k], nextRandom()%20001)
			labels[k] = append(labels[k], nextRandom()%1000)
		}
	}
	var total, check int64
	for round := int64(0); round < 20; round++ {
		for k := int64(0); k < 100; k++ {
			numWanted := (round*7919+k*31)%20000 + 1
			useLimit := (round*13+k)%20 + 1
			answer := largestValsFromLabels(values[k], labels[k], numWanted, useLimit)
			total += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("20 rounds over 100 problems of 2 * 10^4 items: answers sum to %d, checksum %d\n", total, check)
}
