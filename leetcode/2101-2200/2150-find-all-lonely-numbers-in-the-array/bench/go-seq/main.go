// LeetCode #2150: Find All Lonely Numbers in the Array -- the benchmark's
// Go mirror of lonely.kara.
package main

import "fmt"

func findLonely(nums []int64) []int64 {
	count := map[int64]int64{}
	for _, x := range nums {
		count[x]++
	}
	out := []int64{}
	for x, c := range count {
		_, below := count[x-1]
		_, above := count[x+1]
		if c == 1 && !below && !above {
			out = append(out, x)
		}
	}
	return out
}

var seed int64 = 2150

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	const n = 100000
	lists := make([][]int64, 4)
	for l := range lists {
		lists[l] = make([]int64, n)
		for i := range lists[l] {
			lists[l][i] = wide() % 1000001
		}
	}
	var total, check int64
	for round := int64(0); round < 25; round++ {
		for l := 0; l < 4; l++ {
			at := wide() % n
			lists[l][at] = wide() % 1000001
			out := findLonely(lists[l])
			var sum int64
			for _, x := range out {
				sum += x
			}
			total += int64(len(out))
			check = (check*31 + sum%1000000007 + int64(len(out)) + round) % 1000000007
		}
	}
	fmt.Printf("100 searches: %d lonely in all, checksum %d\n", total, check)
}
