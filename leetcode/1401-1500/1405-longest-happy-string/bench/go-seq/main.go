// LeetCode #1405 bench, Go: the same greedy, a sort of the three letters
// before each one placed, workload and checksum as
// longest_diverse_string.kara.
package main

import (
	"fmt"
	"sort"
	"strings"
)

type left struct {
	n  int32
	ch byte
}

func longestDiverseString(a, b, c int32) string {
	ls := []left{{a, 'a'}, {b, 'b'}, {c, 'c'}}
	var out strings.Builder
	for {
		sort.SliceStable(ls, func(i, j int) bool { return ls[i].n > ls[j].n })
		placed := false
		for i := 0; i < 3; i++ {
			n, ch := ls[i].n, ls[i].ch
			if n == 0 {
				break
			}
			if strings.HasSuffix(out.String(), string([]byte{ch, ch})) {
				continue
			}
			out.WriteByte(ch)
			ls[i].n = n - 1
			placed = true
			break
		}
		if !placed {
			return out.String()
		}
	}
}

func main() {
	var seed int64 = 1405
	var check int64
	for r := 0; r < 20000; r++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		a := int32(seed / 65536 % 101)
		seed = (seed*1103515245 + 12345) % 2147483648
		b := int32(seed / 65536 % 101)
		seed = (seed*1103515245 + 12345) % 2147483648
		c := int32(1 + seed/65536%100)
		s := longestDiverseString(a, b, c)
		for i := 0; i < len(s); i++ {
			check = (check*131 + int64(s[i])) % 1000000007
		}
	}
	fmt.Printf("20000 strings of up to 300 letters: checksum %d\n", check)
}
