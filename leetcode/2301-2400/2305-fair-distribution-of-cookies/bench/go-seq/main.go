// LeetCode #2305: Fair Distribution of Cookies -- the bench, the ★ arm in
// Go. Backtrack each bag over the children whose load stays under the
// best so far, trying only the first child with nothing yet.
package main

import (
	"fmt"
	"math"
)

func place(cookies []int64, i int, loads []int64, best *int64) {
	if i == len(cookies) {
		most := loads[0]
		for _, l := range loads[1:] {
			if l > most {
				most = l
			}
		}
		if most < *best {
			*best = most
		}
		return
	}
	for c := range loads {
		if loads[c]+cookies[i] < *best {
			loads[c] += cookies[i]
			place(cookies, i+1, loads, best)
			loads[c] -= cookies[i]
		}
		if loads[c] == 0 {
			break
		}
	}
}

func distributeCookies(cookies []int64, k int) int64 {
	loads := make([]int64, k)
	best := int64(math.MaxInt64)
	place(cookies, 0, loads, &best)
	return best
}

var seed int64 = 2305

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 2000)
	for a := range lists {
		cookies := make([]int64, 8)
		for i := range cookies {
			hi := nextRandom()
			cookies[i] = (hi*32768+nextRandom())%100000 + 1
		}
		lists[a] = cookies
	}
	var check int64
	for p := 0; p < 50; p++ {
		for a := 0; a < 2000; a++ {
			check = (check*31 + distributeCookies(lists[a], 2+(a+p)%7)) % 1000000007
		}
	}
	fmt.Printf("50 passes over 2000 lists of 8 bags: checksum %d\n", check)
}
