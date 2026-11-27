// LeetCode #1817: Finding the Users Active Minutes -- the bench in Go: the
// ★ arm over 5000 calls on runs of 5000 to 9999 logs cut from one list of
// 10^4 logs over 1000 users and 100 minutes, built once, each run's length
// drawn from the checksum so far.
package main

import "fmt"

func findingUsersActiveMinutes(logs [][]int64, k int64) []int64 {
	minutes := map[int64]map[int64]struct{}{}
	for _, log := range logs {
		seen, ok := minutes[log[0]]
		if !ok {
			seen = map[int64]struct{}{}
			minutes[log[0]] = seen
		}
		seen[log[1]] = struct{}{}
	}
	answer := make([]int64, k)
	for _, seen := range minutes {
		answer[len(seen)-1]++
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1817)
	base := make([][]int64, 0, 10000)
	for i := 0; i < 10000; i++ {
		user := nextRandom(&seed) % 1000
		base = append(base, []int64{user, nextRandom(&seed) % 100})
	}
	var check int64
	for call := int64(0); call < 5000; call++ {
		n := 5000 + (check+call)%5000
		run := make([][]int64, n)
		for i := range run {
			run[i] = append([]int64(nil), base[i]...)
		}
		for _, x := range findingUsersActiveMinutes(run, 100) {
			check = (check*31 + x) % 1000000007
		}
	}
	fmt.Printf("5000 calls: checksum %d\n", check)
}
