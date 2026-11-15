// LeetCode #2184: Number of Ways to Build Sturdy Brick Wall -- the
// benchmark's Go mirror of sturdy_wall.kara.
package main

import "fmt"

func fill(at, joints, width int64, bricks []int64, rows *[]int64) {
	if at == width {
		*rows = append(*rows, joints)
		return
	}
	for _, b := range bricks {
		end := at + b
		if end < width {
			fill(end, joints|(1<<end), width, bricks, rows)
		} else if end == width {
			fill(end, joints, width, bricks, rows)
		}
	}
}

func buildWall(height, width int64, bricks []int64) int64 {
	var rows []int64
	fill(0, 0, width, bricks, &rows)
	n := len(rows)
	fits := make([][]int, n)
	for a := 0; a < n; a++ {
		for b := 0; b < n; b++ {
			if rows[a]&rows[b] == 0 {
				fits[a] = append(fits[a], b)
			}
		}
	}
	ways := make([]int64, n)
	for a := range ways {
		ways[a] = 1
	}
	for h := int64(1); h < height; h++ {
		next := make([]int64, n)
		for a := 0; a < n; a++ {
			for _, b := range fits[a] {
				next[b] = (next[b] + ways[a]) % 1000000007
			}
		}
		ways = next
	}
	var total int64
	for _, w := range ways {
		total = (total + w) % 1000000007
	}
	return total
}

var seed int64 = 2184

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var check int64
	for r := 0; r < 1000; r++ {
		height := nextRandom()%51 + 50
		bricks := []int64{1}
		for b := int64(2); b <= 10; b++ {
			if nextRandom()%2 == 0 {
				bricks = append(bricks, b)
			}
		}
		check = (check*31 + buildWall(height, 10, bricks)) % 1000000007
	}
	fmt.Printf("1000 walls: checksum %d\n", check)
}
