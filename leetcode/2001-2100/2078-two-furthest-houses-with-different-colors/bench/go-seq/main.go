// LeetCode #2078: Two Furthest Houses With Different Colors -- Go mirror of
// the ★ arm's benchmark (houses.kara): 20000 streets of 100 houses, 1000
// rounds each recoloring one house of every street and answering every
// street that still has two colors with a scan in from each end.
package main

import "fmt"

var seed int64 = 2078

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxDistance(colors []int64) int64 {
	n := len(colors)
	j := n - 1
	for colors[j] == colors[0] {
		j--
	}
	i := 0
	for colors[i] == colors[n-1] {
		i++
	}
	if j > n-1-i {
		return int64(j)
	}
	return int64(n - 1 - i)
}

func main() {
	streets := make([][]int64, 20000)
	for s := range streets {
		colors := make([]int64, 100)
		a := nextRandom() % 100
		colors[a] = nextRandom()%3 + 1
		b := nextRandom() % 100
		colors[b] = nextRandom()%3 + 1
		streets[s] = colors
	}
	var answered, total, check int64
	for r := 0; r < 1000; r++ {
		for _, colors := range streets {
			k := nextRandom() % 100
			if nextRandom()%2 == 0 {
				colors[k] = 0
			} else {
				colors[k] = nextRandom()%3 + 1
			}
			mixed := false
			for _, c := range colors {
				if c != colors[0] {
					mixed = true
					break
				}
			}
			if mixed {
				a := maxDistance(colors)
				answered++
				total += a
				check = (check*31 + a) % 1000000007
			}
		}
	}
	fmt.Printf("%d answers: sum %d, checksum %d\n", answered, total, check)
}
