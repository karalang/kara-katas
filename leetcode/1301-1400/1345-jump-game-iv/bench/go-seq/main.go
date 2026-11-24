// LeetCode #1345 bench in Go: the ★ arm (a breadth-first search over
// i - 1, i + 1 and the indices of the same value, gathered in a map and
// each value's list deleted the first time it is used) on the same 10
// arrays of 5 * 10^4 values and 30 passes.
package main

import "fmt"

func minJumps(arr []int32) int32 {
	n := len(arr)
	places := make(map[int32][]int)
	for i, v := range arr {
		places[v] = append(places[v], i)
	}
	steps := make([]int32, n)
	for i := range steps {
		steps[i] = -1
	}
	steps[0] = 0
	queue := []int{0}
	for head := 0; head < len(queue); head++ {
		i := queue[head]
		if i == n-1 {
			return steps[i]
		}
		next := places[arr[i]]
		delete(places, arr[i])
		next = append(next, i-1, i+1)
		for _, j := range next {
			if j >= 0 && j < n && steps[j] < 0 {
				steps[j] = steps[i] + 1
				queue = append(queue, j)
			}
		}
	}
	return steps[n-1]
}

var seed int64 = 1345

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := int64(50000)
	arrays := make([][]int32, 10)
	for a := range arrays {
		arrays[a] = make([]int32, n)
		for i := int64(0); i < n; i++ {
			if a%2 == 0 {
				arrays[a][i] = int32(1 + nextRandom()%1000)
			} else {
				arrays[a][i] = int32(i / 2)
			}
		}
	}
	var check int64
	for pass := int64(0); pass < 30; pass++ {
		for a := 0; a < 10; a++ {
			arrays[a][check%n] = int32((check / 7) % 25000)
			answer := minJumps(arrays[a])
			check = (check*31 + int64(answer) + pass) % 1000000007
		}
	}
	fmt.Printf("30 passes over 10 arrays of 5 * 10^4: checksum %d\n", check)
}
