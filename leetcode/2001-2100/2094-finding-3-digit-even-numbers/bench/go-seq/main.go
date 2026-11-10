// LeetCode #2094: Finding 3-Digit Even Numbers -- Go mirror of the ★ arm's
// benchmark (even.kara): the same 100000 lists, each answered by the same
// counts and walk over the even numbers from 100 to 998.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func findEvenNumbers(digits []int64) []int64 {
	var have [10]int64
	for _, d := range digits {
		have[d]++
	}
	var found []int64
	for x := int64(100); x < 1000; x += 2 {
		var need [10]int64
		need[x/100]++
		need[x/10%10]++
		need[x%10]++
		ok := true
		for d := 0; d < 10; d++ {
			if need[d] > have[d] {
				ok = false
				break
			}
		}
		if ok {
			found = append(found, x)
		}
	}
	return found
}

func main() {
	seed := int64(2094)
	count := 0
	check := int64(0)
	tops := []int64{10, 6, 4}
	for t := 0; t < 100000; t++ {
		n := nextRandom(&seed)%98 + 3
		top := tops[nextRandom(&seed)%3]
		digits := make([]int64, n)
		for i := range digits {
			digits[i] = nextRandom(&seed) % top
		}
		got := findEvenNumbers(digits)
		count += len(got)
		for _, x := range got {
			check = (check*31 + x) % 1000000007
		}
	}
	fmt.Printf("100000 answers: %d numbers, checksum %d\n", count, check)
}
