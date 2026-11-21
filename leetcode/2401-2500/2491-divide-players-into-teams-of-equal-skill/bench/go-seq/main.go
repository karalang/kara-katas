// LeetCode #2491: Divide Players Into Teams of Equal Skill -- Go mirror of
// the ★ arm's benchmark (divide.kara): the same 20 lists and 25 passes,
// each list copied and sorted for every answer.
package main

import (
	"fmt"
	"slices"
)

func dividePlayers(skill []int64) int64 {
	sorted := slices.Clone(skill)
	slices.Sort(sorted)
	n := len(sorted)
	target := sorted[0] + sorted[n-1]
	chemistry := int64(0)
	for i := 0; i < n/2; i++ {
		a, b := sorted[i], sorted[n-1-i]
		if a+b != target {
			return -1
		}
		chemistry += a * b
	}
	return chemistry
}

var seed int64 = 2491

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := int64(100000)
	passes := int64(25)
	lists := make([][]int64, 20)
	for l := range lists {
		total := int64(500 + l*50)
		skill := make([]int64, 0, n)
		for k := int64(0); k < n/2; k++ {
			a := nextRandom()%(total-1) + 1
			skill = append(skill, a, total-a)
		}
		for i := n - 1; i >= 1; i-- {
			hi := nextRandom()
			j := (hi*32768 + nextRandom()) % (i + 1)
			skill[i], skill[j] = skill[j], skill[i]
		}
		lists[l] = skill
	}
	check := int64(0)
	for p := int64(0); p < passes; p++ {
		for l := 0; l < 20; l++ {
			at := check % n
			was := lists[l][at]
			lists[l][at] = (check/n+p)%1000 + 1
			check = (check*31 + dividePlayers(lists[l]) + 1 + p) % 1000000007
			lists[l][at] = was
		}
	}
	fmt.Printf("%d passes over 20 lists of 10^5: checksum %d\n", passes, check)
}
