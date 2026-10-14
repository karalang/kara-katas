// Benchmark for #598: Go mirror of the ★ arm (the smallest corner); see
// ../max_count.kara. Each operation is its own slice.
package main

import "fmt"

func maxCount(m, n int64, ops [][]int64) int64 {
	rows, cols := m, n
	for _, op := range ops {
		rows = min(rows, op[0])
		cols = min(cols, op[1])
	}
	return rows * cols
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := step(seed)
	lo := step(seed)
	return hi*32768 + lo
}

func main() {
	count, rounds := 100, 300
	seed := int64(598)
	sizes := [][2]int64{}
	lists := [][][]int64{}
	for k := 0; k < count; k++ {
		m := 1 + wide(&seed)%40000
		n := 1 + wide(&seed)%40000
		ops := [][]int64{}
		for j := 0; j < 10000; j++ {
			a := m - step(&seed)%(1+m/8)
			b := n - step(&seed)%(1+n/8)
			ops = append(ops, []int64{a, b})
		}
		sizes = append(sizes, [2]int64{m, n})
		lists = append(lists, ops)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			c := (round*7 + g) % count
			got := maxCount(sizes[c][0], sizes[c][1], lists[c])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d lists, %d rounds: total %d, checksum %d\n", count, rounds, total, checksum)
}
