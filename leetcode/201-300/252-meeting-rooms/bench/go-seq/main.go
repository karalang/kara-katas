// Benchmark workload for LeetCode #252 — Meeting Rooms (Go mirror).
// Mirrors meeting_rooms.kara algorithm-for-algorithm.
package main

import (
	"fmt"
	"sort"
)

type Iv struct{ s, e int64 }

func main() {
	var n int64 = 120000
	var rounds int64 = 40

	base := make([]Iv, n)
	var state int64 = 252252
	var cursor int64 = 0
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		dur := (state/65536)%7 + 1
		state = (state*1103515245 + 12345) & 2147483647
		gap := (state / 65536) % 3
		base[i] = Iv{cursor, cursor + dur}
		cursor += dur + gap
	}
	for k := n - 1; k > 0; k-- {
		state = (state*1103515245 + 12345) & 2147483647
		wd0 := state / 65536
		state = (state*1103515245 + 12345) & 2147483647
		swap := (wd0 * 32768 + state / 65536) % (k + 1)
		base[k], base[swap] = base[swap], base[k]
	}

	s := make([]Iv, n)
	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		copy(s, base)
		sort.Slice(s, func(a, b int) bool { return s[a].s < s[b].s })
		ok := true
		for j := int64(1); j < n; j++ {
			if s[j].s < s[j-1].e {
				ok = false
			}
		}
		if ok {
			sink = (sink*31 + 1) % 1000000007
		} else {
			sink = (sink * 31) % 1000000007
		}
		sink = (sink*131 + s[n-1].e - s[0].s) % 1000000007
	}
	fmt.Println(sink)
}
