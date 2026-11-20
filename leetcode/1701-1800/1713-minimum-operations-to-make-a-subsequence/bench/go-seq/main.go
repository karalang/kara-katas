// LeetCode #1713: Minimum Operations to Make a Subsequence -- the Go
// mirror of the bench (operations.kara): a map of the target's places and
// the smallest tail of each rising run, found with `sort.Search`, on 20
// random problems of 100000 values, each answered 5 times.
package main

import (
	"fmt"
	"sort"
)

func minOperations(target, arr []int32) int32 {
	place := map[int32]int64{}
	for i, v := range target {
		place[v] = int64(i)
	}
	tails := []int64{}
	for _, a := range arr {
		p, ok := place[a]
		if !ok {
			continue
		}
		i := sort.Search(len(tails), func(k int) bool { return tails[k] >= p })
		if i == len(tails) {
			tails = append(tails, p)
		} else {
			tails[i] = p
		}
	}
	return int32(len(target) - len(tails))
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	a := nextRandom(seed)
	return a*32768 + nextRandom(seed)
}

func main() {
	count := 20
	var rounds int64 = 5
	var n int64 = 100000
	var seed int64 = 1713
	targets := make([][]int32, count)
	arrs := make([][]int32, count)
	for p := 0; p < count; p++ {
		target := make([]int32, n)
		for i := int64(0); i < n; i++ {
			target[i] = int32(i)
		}
		for i := n - 1; i >= 1; i-- {
			j := wide(&seed) % (i + 1)
			target[i], target[j] = target[j], target[i]
		}
		for i := int64(0); i < n; i++ {
			target[i] = target[i]*10000 + int32(nextRandom(&seed)%10000)
		}
		arr := make([]int32, 0, n)
		for i := int64(0); i < n; i++ {
			if nextRandom(&seed)%2 == 0 {
				arr = append(arr, target[wide(&seed)%n])
			} else {
				arr = append(arr, int32(wide(&seed)%1000000000))
			}
		}
		targets[p] = target
		arrs[p] = arr
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for p := 0; p < count; p++ {
			answer := int64(minOperations(targets[p], arrs[p]))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d values, %d rounds: answers sum to %d, checksum %d\n", count, n, rounds, sum, check)
}
