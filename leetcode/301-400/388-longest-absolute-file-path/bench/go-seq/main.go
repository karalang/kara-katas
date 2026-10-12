// Benchmark for #388: mirror of length_longest_path.kara (path lengths by depth).
package main

import (
	"fmt"
	"strings"
)

func lengthLongestPath(b string) int64 {
	length := []int64{0}
	var best int64
	i := 0
	for i < len(b) {
		depth := 0
		for i < len(b) && b[i] == '\t' {
			depth++
			i++
		}
		start := i
		isFile := false
		for i < len(b) && b[i] != '\n' {
			if b[i] == '.' {
				isFile = true
			}
			i++
		}
		path := length[depth] + int64(i-start)
		if isFile {
			if path > best {
				best = path
			}
		} else if depth+1 < len(length) {
			length[depth+1] = path + 1
		} else {
			length = append(length, path+1)
		}
		i++
	}
	return best
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func listing(seed *int64, entries int64) string {
	var out strings.Builder
	var open, depth int64
	for k := int64(0); k < entries; k++ {
		r := step(seed) % 100
		if r < 35 {
			depth = open
		} else if r >= 70 {
			up := (r-70)/10 + 1
			if up > depth {
				depth = 0
			} else {
				depth -= up
			}
		}
		if depth > open {
			depth = open
		}
		nameLen := step(seed)%12 + 1
		file := step(seed)%3 == 0
		if k > 0 {
			out.WriteByte('\n')
		}
		for t := int64(0); t < depth; t++ {
			out.WriteByte('\t')
		}
		for t := int64(0); t < nameLen; t++ {
			out.WriteByte(byte(step(seed)%26 + 97))
		}
		if file {
			out.WriteString(".ext")
			open = depth
		} else if depth < 6 {
			open = depth + 1
		} else {
			open = depth
		}
	}
	return out.String()
}

func main() {
	seed := int64(388)
	var listings []string
	bytes := 0
	for k := 0; k < 200; k++ {
		s := listing(&seed, 800)
		bytes += len(s)
		listings = append(listings, s)
	}
	var checksum int64
	for round := int64(0); round < 150; round++ {
		for _, s := range listings {
			r := lengthLongestPath(s)
			checksum = (checksum*31 + r + round) % 1000000007
		}
	}
	fmt.Printf("%d bytes in 200 listings, 150 rounds, checksum %d\n", bytes, checksum)
}
