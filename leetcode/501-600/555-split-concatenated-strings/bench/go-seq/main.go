// Benchmark for #555: Go mirror of the ★ arm (every cut, the rest at its
// best); see ../split_concatenated_strings.kara.
package main

import (
	"fmt"
	"strings"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func reverse(s string) string {
	b := []byte(s)
	for i, j := 0, len(b)-1; i < j; i, j = i+1, j-1 {
		b[i], b[j] = b[j], b[i]
	}
	return string(b)
}

func splitLoop(strs []string) string {
	n := len(strs)
	larger := make([]string, 0, n)
	for _, s := range strs {
		r := reverse(s)
		if r > s {
			larger = append(larger, r)
		} else {
			larger = append(larger, s)
		}
	}
	answer := ""
	for i := 0; i < n; i++ {
		var mb strings.Builder
		for j := 1; j < n; j++ {
			mb.WriteString(larger[(i+j)%n])
		}
		middle := mb.String()
		for _, t := range []string{strs[i], reverse(strs[i])} {
			for k := 0; k < len(t); k++ {
				candidate := t[k:] + middle + t[:k]
				if candidate > answer {
					answer = candidate
				}
			}
		}
	}
	return answer
}

func main() {
	count := 100
	seed := int64(555)
	lists := [][]string{}
	strs_ := 0
	for i := 0; i < count; i++ {
		alphabet := 2 + nextRandom(&seed)%25
		strs := []string{}
		left := int64(1000)
		for left > 0 {
			length := 1 + nextRandom(&seed)%40
			if length > left {
				length = left
			}
			b := make([]byte, length)
			for k := range b {
				b[k] = byte('a' + nextRandom(&seed)%alphabet)
			}
			strs = append(strs, string(b))
			left -= length
		}
		strs_ += len(strs)
		lists = append(lists, strs)
	}
	var checksum int64
	for round := 0; round < 30; round++ {
		for g := 0; g < count; g++ {
			b := splitLoop(lists[(round*7+g)%count])
			checksum = (checksum*31 + int64(len(b)) + int64(b[0])*7 + int64(b[len(b)/2])) % 1000000007
		}
	}
	fmt.Printf("%d lists, %d strings, 30 rounds each: checksum %d\n", count, strs_, checksum)
}
