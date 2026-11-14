// LeetCode #2121: Intervals Between Identical Elements -- the benchmark,
// the same algorithm as intervals.kara: each value's indices gathered in
// a map, then one running sum per list.

package main

import "fmt"

func getDistances(arr []int64) []int64 {
	positions := map[int64][]int64{}
	for i := range arr {
		positions[arr[i]] = append(positions[arr[i]], int64(i))
	}
	answer := make([]int64, len(arr))
	for _, p := range positions {
		c := int64(len(p))
		var total int64
		for _, x := range p {
			total += x
		}
		var before int64
		for k := int64(0); k < c; k++ {
			pk := p[k]
			after := total - before - pk
			answer[pk] = k*pk - before + after - (c-k-1)*pk
			before += pk
		}
	}
	return answer
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2121)
	arrays := make([][]int64, 0, 40)
	for g := 0; g < 40; g++ {
		top := []int64{10, 100, 1000, 10000}[g%4]
		arr := make([]int64, 50000)
		for i := range arr {
			arr[i] = nextRandom(&seed)%top + 1
		}
		arrays = append(arrays, arr)
	}
	var total, check int64
	for round := 0; round < 20; round++ {
		for g := 0; g < 40; g++ {
			arrays[g][(round*7919+g*104729)%50000]++
			var sum int64
			for _, d := range getDistances(arrays[g]) {
				sum += d
			}
			total += sum
			check = (check*31 + sum%1000000007) % 1000000007
		}
	}
	fmt.Printf("800 solves: distances sum to %d, checksum %d\n", total, check)
}
