// LeetCode #1296 bench: the ★ arm over 20 arrays of 16666 runs of 6
// consecutive numbers, shuffled, built once; then 10 passes, each swapping two
// numbers of every array and choosing k from the checksum so far. Go has no
// sorted map; the counts' keys are sorted once per call, as the ★ arm's walk
// visits them.
package main

import (
	"fmt"
	"sort"
)

func isPossibleDivide(nums []int64, k int64) bool {
	if int64(len(nums))%k != 0 {
		return false
	}
	count := make(map[int64]int64)
	for _, x := range nums {
		count[x]++
	}
	keys := make([]int64, 0, len(count))
	for x := range count {
		keys = append(keys, x)
	}
	sort.Slice(keys, func(i, j int) bool { return keys[i] < keys[j] })
	for _, x := range keys {
		sets := count[x]
		if sets == 0 {
			continue
		}
		for y := x; y < x+k; y++ {
			have := count[y]
			if have < sets {
				return false
			}
			count[y] = have - sets
		}
	}
	return true
}

func main() {
	seed := int64(1296)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	wideRandom := func() int64 {
		a := nextRandom()
		return a*32768 + nextRandom()
	}
	arrays := make([][]int64, 20)
	for a := range arrays {
		spread := int64(1000000000)
		if a%2 == 0 {
			spread = 10000
		}
		nums := make([]int64, 0, 99996)
		for r := 0; r < 16666; r++ {
			start := 1 + wideRandom()%spread
			for d := int64(0); d < 6; d++ {
				nums = append(nums, start+d)
			}
		}
		n := int64(len(nums))
		for i := int64(0); i < n; i++ {
			j := i + wideRandom()%(n-i)
			nums[i], nums[j] = nums[j], nums[i]
		}
		arrays[a] = nums
	}
	var check int64
	for p := int64(0); p < 10; p++ {
		for a := range arrays {
			n := int64(len(arrays[a]))
			i, j := check%n, (check/n)%n
			arrays[a][i], arrays[a][j] = arrays[a][j], arrays[a][i]
			k := 1 + check%6
			v := int64(1)
			if isPossibleDivide(arrays[a], k) {
				v = 2
			}
			check = (check*31 + v + p) % 1000000007
		}
	}
	fmt.Printf("10 passes over 20 arrays of 99996: checksum %d\n", check)
}
