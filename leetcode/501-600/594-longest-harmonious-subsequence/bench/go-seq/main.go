// Benchmark for #594: Go mirror of the ★ arm (count in a map, then pair);
// see ../find_lhs.kara. A built-in map, which Go seeds per map.
package main

import "fmt"

func findLHS(nums []int64) int64 {
	count := map[int64]int64{}
	for _, x := range nums {
		count[x]++
	}
	var best int64
	for v, c := range count {
		if d, ok := count[v+1]; ok && c+d > best {
			best = c + d
		}
	}
	return best
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := step(seed)
	lo := step(seed)
	return hi*32768 + lo
}

func main() {
	count, rounds := 100, 20
	seed := int64(594)
	arrays := [][]int64{}
	for k := 0; k < count; k++ {
		rng := 1 + wide(&seed)%5000
		low := wide(&seed)%1999990000 - 999990000
		nums := []int64{}
		for j := 0; j < 20000; j++ {
			nums = append(nums, low+wide(&seed)%rng)
		}
		arrays = append(arrays, nums)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			got := findLHS(arrays[(round*7+g)%count])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d arrays, %d rounds: total %d, checksum %d\n", count, rounds, total, checksum)
}
