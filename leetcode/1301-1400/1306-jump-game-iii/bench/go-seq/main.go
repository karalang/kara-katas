// LeetCode #1306 bench in Go: the ★ arm (a breadth-first walk from the
// start, the queue a slice read from a moving head, each place queued once)
// on the same 10 arrays and 300 passes.
package main

import "fmt"

func canReach(arr []int64, start int64) bool {
	n := int64(len(arr))
	seen := make([]bool, n)
	queue := []int64{start}
	seen[start] = true
	for head := 0; head < len(queue); head++ {
		i := queue[head]
		if arr[i] == 0 {
			return true
		}
		for _, j := range [2]int64{i + arr[i], i - arr[i]} {
			if j >= 0 && j < n && !seen[j] {
				seen[j] = true
				queue = append(queue, j)
			}
		}
	}
	return false
}

var seed int64 = 1306

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := int64(50000)
	arrays := make([][]int64, 10)
	for a := range arrays {
		arr := make([]int64, n)
		for k := range arr {
			arr[k] = 1 + nextRandom()%10
		}
		arr[nextRandom()%n] = 0
		arrays[a] = arr
	}
	var check int64
	for pass := int64(0); pass < 300; pass++ {
		for a := 0; a < 10; a++ {
			arrays[a][check%n] = (check / 7) % 11
			start := (check / 13) % n
			got := canReach(arrays[a], start)
			v := int64(2)
			if got {
				v = 1
			}
			check = (check*31 + v + pass) % 1000000007
		}
	}
	fmt.Printf("300 passes over 10 arrays of 5 * 10^4: checksum %d\n", check)
}
