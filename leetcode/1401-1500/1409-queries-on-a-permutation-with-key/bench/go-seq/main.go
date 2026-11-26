// LeetCode #1409 bench, Go: the same P, each query found and the part up
// to it turned one place, workload and checksum as process_queries.kara.
package main

import "fmt"

func processQueries(queries []int32, m int32) []int32 {
	p := make([]int32, m)
	for i := range p {
		p[i] = int32(i) + 1
	}
	answer := make([]int32, 0, len(queries))
	for _, q := range queries {
		at := 0
		for p[at] != q {
			at++
		}
		answer = append(answer, int32(at))
		copy(p[1:at+1], p[:at])
		p[0] = q
	}
	return answer
}

func main() {
	var seed, check int64 = 1409, 0
	for r := 0; r < 300; r++ {
		queries := make([]int32, 0, 1000)
		for k := 0; k < 1000; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			queries = append(queries, int32(1+seed/65536%1000))
		}
		for _, x := range processQueries(queries, 1000) {
			check = (check*131 + int64(x)) % 1000000007
		}
	}
	fmt.Printf("300 rounds of 10^3 queries: checksum %d\n", check)
}
