package main

import "fmt"

// Build-once + punch reorder-list over an index pool (see reorder_list.kara).
// Each pass generates the interleaved order, rewires nxt, and walks it, folding a
// position-weighted checksum into the sink.
func main() {
	var n int64 = 100000
	var k int64 = 1000
	var valmod int64 = 1000

	vals := make([]int64, n)
	nxt := make([]int64, n)
	order := make([]int64, n)

	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		vals[i] = (state >> 16) % valmod
	}

	var sink int64 = 0
	for p := int64(0); p < k; p++ {
		pi := p % n
		vals[pi] = (vals[pi] + 1) % valmod

		var lo int64 = 0
		hi := n - 1
		var idx int64 = 0
		takeLo := true
		for lo <= hi {
			if takeLo {
				order[idx] = lo
				lo++
			} else {
				order[idx] = hi
				hi--
			}
			takeLo = !takeLo
			idx++
		}

		for r := int64(0); r+1 < n; r++ {
			nxt[order[r]] = order[r+1]
		}
		nxt[order[n-1]] = -1

		cur := order[0]
		var pos int64 = 0
		for cur >= 0 {
			w := (pos % 997) + 1
			sink += w * vals[cur]
			pos++
			cur = nxt[cur]
		}
	}

	fmt.Println(sink)
}
