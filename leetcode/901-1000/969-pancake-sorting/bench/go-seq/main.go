// Benchmark: LeetCode #969 Pancake Sorting -- the ★ arm, the largest
// pancake to the bottom one at a time, on 200 random stacks of 100
// pancakes. Mirrors pancake_sort.kara, .c, .rs and .py.
package main

import "fmt"

func flip(a []int64, k int64) {
	i, j := int64(0), k-1
	for i < j {
		a[i], a[j] = a[j], a[i]
		i++
		j--
	}
}

func pancakeSort(arr []int64) []int64 {
	a := append([]int64(nil), arr...)
	var flips []int64
	for size := int64(len(a)); size > 1; size-- {
		i := int64(0)
		for a[i] != size {
			i++
		}
		if i != size-1 {
			if i != 0 {
				flip(a, i+1)
				flips = append(flips, i+1)
			}
			flip(a, size)
			flips = append(flips, size)
		}
	}
	return flips
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomPermutation(n int64, seed *int64) []int64 {
	a := make([]int64, n)
	for v := int64(1); v <= n; v++ {
		a[v-1] = v
	}
	for i := n - 1; i > 0; i-- {
		j := nextRandom(seed) % (i + 1)
		a[i], a[j] = a[j], a[i]
	}
	return a
}

func main() {
	rounds, count := 100, 200
	seed := int64(969)
	stacks := make([][]int64, count)
	for s := range stacks {
		stacks[s] = randomPermutation(100, &seed)
	}
	flips, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for s := 0; s < count; s++ {
			for _, k := range pancakeSort(stacks[(r+s)%count]) {
				flips++
				check = (check*131 + k) % 1000000007
			}
		}
	}
	fmt.Printf("%d rounds over %d stacks of 100 pancakes: %d flips, checksum %d\n", rounds, count, flips, check)
}
