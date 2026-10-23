// LeetCode #874 bench: Go mirror of robot_sim.kara (the ★ arm, a map of
// obstacles) on the same 600 walks.
package main

import "fmt"

func robotSim(commands []int64, obstacles [][2]int64) int64 {
	blocked := make(map[int64]struct{})
	for _, o := range obstacles {
		blocked[square(o[0], o[1])] = struct{}{}
	}
	dx := [4]int64{0, 1, 0, -1}
	dy := [4]int64{1, 0, -1, 0}
	facing := 0
	var x, y, best int64
	for _, c := range commands {
		if c == -2 {
			facing = (facing + 3) % 4
		} else if c == -1 {
			facing = (facing + 1) % 4
		} else {
			for s := int64(0); s < c; s++ {
				nx := x + dx[facing]
				ny := y + dy[facing]
				if _, hit := blocked[square(nx, ny)]; hit {
					break
				}
				x, y = nx, ny
				if x*x+y*y > best {
					best = x*x + y*y
				}
			}
		}
	}
	return best
}

func square(x, y int64) int64 {
	return (x+200000)*400001 + (y + 200000)
}

var seed int64 = 874

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomCommands(n int, turns int64) []int64 {
	commands := make([]int64, 0, n)
	for i := 0; i < n; i++ {
		if nextRandom()%turns == 0 {
			commands = append(commands, -1-nextRandom()%2)
		} else {
			commands = append(commands, nextRandom()%9+1)
		}
	}
	return commands
}

func randomObstacles(n int, reach int64) [][2]int64 {
	obstacles := make([][2]int64, 0, n)
	for i := 0; i < n; i++ {
		x := nextRandom()%(2*reach+1) - reach
		y := nextRandom()%(2*reach+1) - reach
		obstacles = append(obstacles, [2]int64{x, y})
	}
	return obstacles
}

func main() {
	var commandLists [][]int64
	var obstacleLists [][][2]int64
	for k := 0; k < 20; k++ {
		commandLists = append(commandLists, randomCommands(10000, int64(2+k%3)))
		obstacleLists = append(obstacleLists, randomObstacles(10000, int64(100+10*k)))
	}
	var total, check int64
	for k := 0; k < 600; k++ {
		answer := robotSim(commandLists[k%20], obstacleLists[(k*7+k/20)%20])
		total += answer
		check = (check*131 + answer) % 1000000007
	}
	fmt.Printf("600 walks of 10000 commands among 10000 obstacles: distances sum to %d, checksum %d\n", total, check)
}
