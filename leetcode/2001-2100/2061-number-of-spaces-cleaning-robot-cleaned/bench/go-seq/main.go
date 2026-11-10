// LeetCode #2061: Number of Spaces Cleaning Robot Cleaned -- Go mirror of
// the ★ arm's benchmark (robot.kara): 600 spiral rooms of 200 to 300 by
// 200 to 300, the robot walked one move at a time, states and cells kept
// in flat `[]bool`s.
package main

import "fmt"

var dr = [4]int64{0, 1, 0, -1}
var dc = [4]int64{1, 0, -1, 0}

func numberOfCleanRooms(room [][]int64) int64 {
	m, n := int64(len(room)), int64(len(room[0]))
	seen := make([]bool, m*n*4)
	cleaned := make([]bool, m*n)
	count := int64(0)
	r, c, d := int64(0), int64(0), int64(0)
	for !seen[(r*n+c)*4+d] {
		seen[(r*n+c)*4+d] = true
		if !cleaned[r*n+c] {
			cleaned[r*n+c] = true
			count++
		}
		nr, nc := r+dr[d], c+dc[d]
		if nr >= 0 && nr < m && nc >= 0 && nc < n && room[nr][nc] == 0 {
			r, c = nr, nc
		} else {
			d = (d + 1) % 4
		}
	}
	return count
}

var seed int64 = 2061

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func spiral(m, n int64) [][]int64 {
	room := make([][]int64, m)
	for i := range room {
		room[i] = make([]int64, n)
	}
	top, left, bottom, right := int64(0), int64(0), m-1, n-1
	for {
		if top+2 > bottom {
			break
		}
		room[top+1][left] = 1
		top += 2
		if left+2 > right {
			break
		}
		room[top][right-1] = 1
		right -= 2
		if bottom-2 < top {
			break
		}
		room[bottom-1][right] = 1
		bottom -= 2
		if right-2 < left {
			break
		}
		room[bottom][left+1] = 1
		left += 2
	}
	return room
}

func main() {
	total, check := int64(0), int64(0)
	for t := 0; t < 600; t++ {
		m := nextRandom()%101 + 200
		n := nextRandom()%101 + 200
		a := numberOfCleanRooms(spiral(m, n))
		total += a
		check = (check*31 + a) % 1000000007
	}
	fmt.Printf("600 rooms: %d cleaned, checksum %d\n", total, check)
}
