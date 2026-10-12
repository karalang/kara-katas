// Benchmark for #411: mirror of min_abbreviation.kara (masks over the
// letters).
package main

import (
	"fmt"
	"os"
	"strconv"
)

func abbreviate(t string, mask int64) string {
	out := []byte{}
	run := 0
	for i := 0; i < len(t); i++ {
		if (mask>>i)&1 == 1 {
			if run > 0 {
				out = append(out, strconv.Itoa(run)...)
				run = 0
			}
			out = append(out, t[i])
		} else {
			run++
		}
	}
	if run > 0 {
		out = append(out, strconv.Itoa(run)...)
	}
	return string(out)
}

func maskLength(m int, mask int64) int {
	length := 0
	inRun := false
	for i := 0; i < m; i++ {
		if (mask>>i)&1 == 1 {
			length++
			inRun = false
		} else if !inRun {
			length++
			inRun = true
		}
	}
	return length
}

func minAbbreviation(target string, dictionary []string) string {
	m := len(target)
	diffs := []int64{}
	for _, w := range dictionary {
		if len(w) == m {
			var diff int64
			for i := 0; i < m; i++ {
				if w[i] != target[i] {
					diff |= 1 << i
				}
			}
			diffs = append(diffs, diff)
		}
	}
	bestMask := int64(1)<<m - 1
	bestLength := m
	for mask := int64(0); mask < int64(1)<<m; mask++ {
		length := maskLength(m, mask)
		if length < bestLength {
			unique := true
			for _, d := range diffs {
				if mask&d == 0 {
					unique = false
					break
				}
			}
			if unique {
				bestLength = length
				bestMask = mask
			}
		}
	}
	return abbreviate(target, bestMask)
}

var seed int64 = 411

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	targets := 30
	if len(os.Args) > 1 {
		targets, _ = strconv.Atoi(os.Args[1])
	}
	m := 20
	words := 2
	var total, checksum int64
	for t := 0; t < targets; t++ {
		tb := make([]byte, m)
		for i := range tb {
			tb[i] = byte(97 + step()%2)
		}
		target := string(tb)
		dictionary := []string{}
		for len(dictionary) < words {
			wb := make([]byte, m)
			for i := range wb {
				wb[i] = byte(97 + step()%2)
			}
			if string(wb) != target {
				dictionary = append(dictionary, string(wb))
			}
		}
		abbr := minAbbreviation(target, dictionary)
		total += int64(len(abbr))
		for i := 0; i < len(abbr); i++ {
			checksum = (checksum*31 + int64(abbr[i])) % 1000000007
		}
	}
	fmt.Printf("%d targets of %d letters, %d words each: total %d, checksum %d\n", targets, m, words, total, checksum)
}
