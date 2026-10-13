// Benchmark for #471 -- Go mirror of the ★ arm (encode_string.kara):
// interval DP over the encodings, with the shortest unit found where t
// first appears again in t + t.
package main

import (
	"fmt"
	"strings"
)

func encode(s string) string {
	n := len(s)
	best := make([][]string, n)
	for i := range best {
		best[i] = make([]string, n)
	}
	for length := 1; length <= n; length++ {
		for i := 0; i <= n-length; i++ {
			j := i + length - 1
			t := s[i : j+1]
			doubled := t + t
			unit := 1 + strings.Index(doubled[1:], t)
			shortest := t
			if unit < length {
				packed := fmt.Sprintf("%d[%s]", length/unit, best[i][i+unit-1])
				if len(packed) < len(shortest) {
					shortest = packed
				}
			}
			for k := i; k < j; k++ {
				if len(best[i][k])+len(best[k+1][j]) < len(shortest) {
					shortest = best[i][k] + best[k+1][j]
				}
			}
			best[i][j] = shortest
		}
	}
	return best[0][n-1]
}

// ---- bench ------------------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomString(seed *int64, letters int64, depth int64) string {
	var b strings.Builder
	pieces := 1 + nextRandom(seed)%4
	for p := int64(0); p < pieces; p++ {
		if depth > 0 && nextRandom(seed)%2 == 0 {
			unit := randomString(seed, letters, depth-1)
			copies := 2 + nextRandom(seed)%11
			for c := int64(0); c < copies; c++ {
				b.WriteString(unit)
			}
		} else {
			b.WriteByte(byte(97 + nextRandom(seed)%letters))
		}
	}
	return b.String()
}

func main() {
	count := 400
	size := 150
	seed := int64(471)
	stringsIn := make([]string, 0, count)
	for c := 0; c < count; c++ {
		letters := 2 + nextRandom(&seed)%2
		s := ""
		for len(s) < size {
			s += randomString(&seed, letters, 2)
		}
		stringsIn = append(stringsIn, s[:size])
	}
	total := 0
	checksum := int64(0)
	for i := 0; i < count; i++ {
		e := encode(stringsIn[i])
		total += len(e)
		checksum = (checksum*31 + int64(len(e))) % 1000000007
	}
	fmt.Printf("%d strings of %d letters: %d letters encoded, checksum %d\n", count, size, total, checksum)
}
