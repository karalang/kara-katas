// LeetCode #2358: Maximum Number of Groups Entering a Competition -- the
// bench, the ★ arm in Go: group sizes 1, 2, 3, ... added while the next
// still fits in the class.
package main

import "fmt"

func maximumGroups(grades []int64) int64 {
	n := int64(len(grades))
	k := int64(0)
	used := int64(0)
	for used+k+1 <= n {
		k++
		used += k
	}
	return k
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// class a holds 10^4 (a + 1) - a students graded 1 to 10^5
	seed := int64(2358)
	classes := make([][]int64, 0, 10)
	for a := int64(0); a < 10; a++ {
		grades := make([]int64, 10000*(a+1)-a)
		for i := range grades {
			grades[i] = 1 + nextRandom(&seed)%100000
		}
		classes = append(classes, grades)
	}
	check := int64(0)
	for p := int64(0); p < 20000; p++ {
		for _, grades := range classes {
			check = (check*31 + maximumGroups(grades) + p) % 1000000007
		}
	}
	fmt.Printf("20000 passes over 10 classes: checksum %d\n", check)
}
