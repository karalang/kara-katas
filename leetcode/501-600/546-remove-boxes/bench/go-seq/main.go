// Benchmark for #546: Go mirror of the ★ arm (memoized, with the boxes
// carried along); see ../remove_boxes.kara.
package main

import "fmt"

func best(boxes []int64, l, r, k int, memo []int64) int64 {
	if l > r {
		return 0
	}
	n := len(boxes)
	key := (l*n+r)*n + k
	if memo[key] >= 0 {
		return memo[key]
	}
	i, run := l, k+1
	for i < r && boxes[i+1] == boxes[l] {
		i++
		run++
	}
	most := int64(run*run) + best(boxes, i+1, r, 0, memo)
	for m := i + 2; m <= r; m++ {
		if boxes[m] == boxes[l] && boxes[m-1] != boxes[l] {
			most = max(most, best(boxes, i+1, m-1, 0, memo)+best(boxes, m, r, run, memo))
		}
	}
	memo[key] = most
	return most
}

func removeBoxes(boxes []int64) int64 {
	n := len(boxes)
	memo := make([]int64, n*n*n)
	for i := range memo {
		memo[i] = -1
	}
	return best(boxes, 0, n-1, 0, memo)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 40 random rows of 100 boxes (the problem's most), from 2 to 9
	// colours by the row, built once. Then 5 times over every row is
	// answered and the points go into the checksum.
	rows := 40
	seed := int64(546)
	all := make([][]int64, rows)
	for g := 0; g < rows; g++ {
		colours := int64(2 + g%8)
		all[g] = make([]int64, 100)
		for i := range all[g] {
			all[g][i] = 1 + nextRandom(&seed)%colours
		}
	}
	var total, checksum int64
	for round := 0; round < 5; round++ {
		for t := 0; t < rows; t++ {
			points := removeBoxes(all[t])
			total += points
			checksum = (checksum*31 + points) % 1000000007
		}
	}
	fmt.Printf("%d rows, 5 times each: %d points, checksum %d\n", rows, total, checksum)
}
