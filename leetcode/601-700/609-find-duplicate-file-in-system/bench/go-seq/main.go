// Benchmark mirror for #609: the same workload and algorithm as
// find_duplicate.kara (a map from content to paths).
package main

import (
	"fmt"
	"strings"
)

func findDuplicate(paths []string) [][]string {
	byContent := map[string][]string{}
	for _, line := range paths {
		parts := strings.Split(line, " ")
		dir := parts[0]
		for _, file := range parts[1:] {
			open := strings.IndexByte(file, '(')
			content := file[open+1 : len(file)-1]
			byContent[content] = append(byContent[content], dir+"/"+file[:open])
		}
	}
	var groups [][]string
	for _, g := range byContent {
		if len(g) > 1 {
			groups = append(groups, g)
		}
	}
	return groups
}

var seed int64 = 609

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	systems, rounds := int64(10), int64(300)
	pool := make([]string, 0, 3000)
	for i := 0; i < 3000; i++ {
		size := 8 + step()%13
		b := make([]byte, 0, size)
		for j := int64(0); j < size; j++ {
			b = append(b, byte(97+step()%4))
		}
		pool = append(pool, string(b))
	}
	all := make([][]string, 0, systems)
	for s := int64(0); s < systems; s++ {
		paths := make([]string, 0, 2000)
		counter := 0
		for d := 0; d < 2000; d++ {
			line := fmt.Sprintf("root/s%d/d%d", s, d)
			files := 1 + step()%6
			for k := int64(0); k < files; k++ {
				counter++
				line += fmt.Sprintf(" f%d.txt(%s)", counter, pool[step()%3000])
			}
			paths = append(paths, line)
		}
		all = append(all, paths)
	}
	var groups, files, checksum int64
	for r := int64(0); r < rounds; r++ {
		found := findDuplicate(all[(r*3)%systems])
		groups += int64(len(found))
		for _, g := range found {
			files += int64(len(g))
			var length int64
			for _, p := range g {
				length += int64(len(p))
			}
			checksum = (checksum + int64(len(g))*length) % 1000000007
		}
	}
	fmt.Printf("%d systems, %d rounds: %d groups, %d files, checksum %d\n", systems, rounds, groups, files, checksum)
}
