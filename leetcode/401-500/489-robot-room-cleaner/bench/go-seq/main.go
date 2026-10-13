// Benchmark for #489: Go mirror of the ★ arm (backtracking); see
// ../robot_room_cleaner.kara.
package main

import "fmt"

var step = [4][2]int64{{-1, 0}, {0, 1}, {1, 0}, {0, -1}}

type Robot struct {
	room          [][]int64
	row, col      int64
	facing        int
	cleaned       [][]int64
	calls, budget int64
}

func newRobot(room [][]int64, row, col int64, facing int) *Robot {
	copied := make([][]int64, len(room))
	cleaned := make([][]int64, len(room))
	for r := range room {
		copied[r] = append([]int64(nil), room[r]...)
		cleaned[r] = make([]int64, len(room[r]))
	}
	cells := int64(len(room) * len(room[0]))
	return &Robot{copied, row, col, facing, cleaned, 0, 16*cells*cells + 1000}
}

func (b *Robot) forward() bool {
	b.calls++
	if b.calls > b.budget {
		return false
	}
	r, c := b.row+step[b.facing][0], b.col+step[b.facing][1]
	if r < 0 || r >= int64(len(b.room)) || c < 0 || c >= int64(len(b.room[0])) || b.room[r][c] == 0 {
		return false
	}
	b.row, b.col = r, c
	return true
}

func (b *Robot) turnRight() {
	b.calls++
	if b.calls <= b.budget {
		b.facing = (b.facing + 1) % 4
	}
}

func (b *Robot) clean() {
	b.calls++
	if b.calls <= b.budget {
		b.cleaned[b.row][b.col]++
	}
}

func explore(robot *Robot, row, col int64, facing int, visited map[[2]int64]bool) {
	visited[[2]int64{row, col}] = true
	robot.clean()
	d := facing
	for i := 0; i < 4; i++ {
		next := [2]int64{row + step[d][0], col + step[d][1]}
		if !visited[next] && robot.forward() {
			explore(robot, next[0], next[1], d, visited)
			robot.turnRight()
			robot.turnRight()
			robot.forward()
			robot.turnRight()
			robot.turnRight()
		}
		robot.turnRight()
		d = (d + 1) % 4
	}
}

func cleanRoom(robot *Robot) {
	explore(robot, 0, 0, 0, map[[2]int64]bool{})
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rooms := [][][]int64{}
	starts := [][2]int64{}
	var seed int64 = 489
	for k := 0; k < 300; k++ {
		room := make([][]int64, 100)
		for r := range room {
			room[r] = make([]int64, 100)
			for c := range room[r] {
				if nextRandom(&seed)%4 == 0 {
					room[r][c] = 0
				} else {
					room[r][c] = 1
				}
			}
		}
		row := nextRandom(&seed) % 100
		col := nextRandom(&seed) % 100
		room[row][col] = 1
		rooms = append(rooms, room)
		starts = append(starts, [2]int64{row, col})
	}
	var total, checksum int64
	for k := range rooms {
		robot := newRobot(rooms[k], starts[k][0], starts[k][1], 0)
		cleanRoom(robot)
		var cleaned int64
		for r := int64(0); r < 100; r++ {
			for c := int64(0); c < 100; c++ {
				if robot.cleaned[r][c] > 0 {
					cleaned++
					checksum = (checksum*31 + r*100 + c) % 1000000007
				}
			}
		}
		total += cleaned
		checksum = (checksum*31 + robot.calls) % 1000000007
	}
	fmt.Printf("300 rooms of 100 by 100: %d cells cleaned, checksum %d\n", total, checksum)
}
