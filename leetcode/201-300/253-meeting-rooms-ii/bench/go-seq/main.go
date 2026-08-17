// Benchmark workload for LeetCode #253 — Meeting Rooms II (Go mirror).
// Mirrors min_meeting_rooms.kara algorithm-for-algorithm, including the
// hand-rolled binary heap (not container/heap, so both sides run the same sifts).
package main

import (
	"fmt"
	"sort"
)

type Iv struct{ s, e int64 }

var H []int64

func heapPush(v int64) {
	H = append(H, v)
	i := len(H) - 1
	for i > 0 {
		p := (i - 1) / 2
		if H[i] < H[p] {
			H[i], H[p] = H[p], H[i]
			i = p
		} else {
			break
		}
	}
}

func heapPop() {
	n := len(H)
	if n == 0 {
		return
	}
	last := H[n-1]
	H = H[:n-1]
	if len(H) == 0 {
		return
	}
	H[0] = last
	m := len(H)
	i := 0
	for {
		l, r := 2*i+1, 2*i+2
		sm := i
		if l < m && H[l] < H[sm] {
			sm = l
		}
		if r < m && H[r] < H[sm] {
			sm = r
		}
		if sm == i {
			break
		}
		H[i], H[sm] = H[sm], H[i]
		i = sm
	}
}

func main() {
	var n int64 = 150000
	var rounds int64 = 25

	base := make([]Iv, n)
	var state int64 = 253253
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		jitter := (state / 65536) % 8
		state = (state*1103515245 + 12345) & 2147483647
		dur := (state/65536)%60 + 1
		base[i] = Iv{i + jitter, i + jitter + dur}
	}
	for k := n - 1; k > 0; k-- {
		state = (state*1103515245 + 12345) & 2147483647
		wd0 := state / 65536
		state = (state*1103515245 + 12345) & 2147483647
		sw := (wd0 * 32768 + state / 65536) % (k + 1)
		base[k], base[sw] = base[sw], base[k]
	}

	s := make([]Iv, n)
	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		copy(s, base)
		sort.Slice(s, func(a, b int) bool { return s[a].s < s[b].s })
		H = H[:0]
		var rooms int64 = 0
		for j := int64(0); j < n; j++ {
			for len(H) > 0 && H[0] <= s[j].s {
				heapPop()
			}
			heapPush(s[j].e)
			if int64(len(H)) > rooms {
				rooms = int64(len(H))
			}
		}
		sink = (sink*31 + rooms) % 1000000007
	}
	fmt.Println(sink)
}
