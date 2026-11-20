// LeetCode #1238: the benchmark, mirroring the Kāra file.
package main

import "fmt"

func circularPermutation(n int64, start int64) []int64 {
	size := int64(1) << n
	p := make([]int64, size)
	for i := int64(0); i < size; i++ {
		p[i] = start ^ i ^ (i >> 1)
	}
	return p
}

func isCycle(n int64, start int64, p []int64) bool {
	size := int64(1) << n
	if int64(len(p)) != size || p[0] != start {
		return false
	}
	seen := make([]bool, size)
	for _, v := range p {
		if v < 0 || v >= size || seen[v] {
			return false
		}
		seen[v] = true
	}
	for i := int64(0); i < size; i++ {
		d := p[i] ^ p[(i+1)%size]
		if d == 0 || d&(d-1) != 0 {
			return false
		}
	}
	return true
}

func main() {
	var cycles, check int64
	for k := int64(0); k < 64; k++ {
		start := (k * 1031) % 65536
		p := circularPermutation(16, start)
		if isCycle(16, start, p) {
			cycles++
		}
		check = (check*131 + p[32768]) % 1000000007
	}
	fmt.Printf("n = 16, 64 starts: %d cycles, checksum %d\n", cycles, check)
}
