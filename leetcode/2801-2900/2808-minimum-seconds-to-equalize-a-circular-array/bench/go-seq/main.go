// LeetCode #2808: Minimum Seconds to Equalize a Circular Array -- the
// bench in Go: the ★ arm over 20 arrays of 10^5 numbers from 1000
// values, all drawn first, then each answered 20 times.
package main

import "fmt"

func minimumSeconds(nums []int64) int64 {
	n := int64(len(nums))
	places := map[int64][]int64{}
	for i, v := range nums {
		places[v] = append(places[v], int64(i))
	}
	best := n
	for _, at := range places {
		widest := at[0] + n - at[len(at)-1]
		for k := 1; k < len(at); k++ {
			if at[k]-at[k-1] > widest {
				widest = at[k] - at[k-1]
			}
		}
		if widest/2 < best {
			best = widest / 2
		}
	}
	return best
}

var seed int64 = 2808

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count := 20
	rounds := 20
	cases := make([][]int64, count)
	for c := range cases {
		cases[c] = make([]int64, 100000)
		for i := range cases[c] {
			cases[c][i] = wide()%1000*1000003 + 1
		}
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for _, nums := range cases {
			a := minimumSeconds(nums)
			total += a
			check = (check*31 + a + r) % 1000000007
		}
	}
	fmt.Printf("%d arrays of 10^5, %d rounds: seconds sum to %d, checksum %d\n", count, rounds, total, check)
}
