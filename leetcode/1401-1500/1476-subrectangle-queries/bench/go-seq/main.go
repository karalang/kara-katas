// LeetCode #1476: Subrectangle Queries -- bench, Go mirror of
// subrectangle_queries.kara
package main

import "fmt"

type SubrectangleQueries struct {
	rect [][]int32
}

func (q *SubrectangleQueries) updateSubrectangle(row1, col1, row2, col2, newValue int32) {
	for r := row1; r <= row2; r++ {
		for c := col1; c <= col2; c++ {
			q.rect[r][c] = newValue
		}
	}
}

func (q *SubrectangleQueries) getValue(row, col int32) int32 {
	return q.rect[row][col]
}

var seed int64 = 1476

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rect := make([][]int32, 100)
	for r := range rect {
		rect[r] = make([]int32, 100)
		for c := range rect[r] {
			hi := nextRandom()
			rect[r][c] = int32(1 + (hi*32768+nextRandom())%1000000000)
		}
	}
	q := &SubrectangleQueries{rect: rect}
	var check int64
	for pass := int64(0); pass < 5000; pass++ {
		for k := 0; k < 250; k++ {
			r1 := nextRandom() % 100
			r2 := r1 + nextRandom()%(100-r1)
			c1 := nextRandom() % 100
			c2 := c1 + nextRandom()%(100-c1)
			q.updateSubrectangle(int32(r1), int32(c1), int32(r2), int32(c2), int32(1+check%1000000000))
			r := nextRandom() % 100
			c := nextRandom() % 100
			check = (check*31 + int64(q.getValue(int32(r), int32(c))) + pass) % 1000000007
		}
	}
	fmt.Printf("5000 passes of 250 updates on 100 by 100: checksum %d\n", check)
}
