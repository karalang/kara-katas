// LeetCode #735: Asteroid Collision -- a stack of survivors.
// Benchmark mirror of the Kara star arm: walk the row keeping the
// survivors so far on a stack; a left-mover destroys the smaller
// right-movers on top, then is destroyed by a larger one, dies with an
// equal one, or survives onto the stack.
package main

import "fmt"

func asteroidCollision(asteroids []int64) []int64 {
	var stack []int64
	for _, a := range asteroids {
		alive := true
		for alive && a < 0 && len(stack) > 0 && stack[len(stack)-1] > 0 {
			top := stack[len(stack)-1]
			if top < -a {
				stack = stack[:len(stack)-1]
			} else {
				if top == -a {
					stack = stack[:len(stack)-1]
				}
				alive = false
			}
		}
		if alive {
			stack = append(stack, a)
		}
	}
	return stack
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(735)
	rows := make([][]int64, 20)
	for k := range rows {
		for i := 0; i < 10000; i++ {
			size := 1 + nextRandom(&seed)%1000
			if nextRandom(&seed)%2 == 0 {
				rows[k] = append(rows[k], size)
			} else {
				rows[k] = append(rows[k], -size)
			}
		}
	}
	var left, sum int64
	for r := 0; r < 500; r++ {
		for k := 0; k < 20; k++ {
			j := nextRandom(&seed) % 10000
			rows[k][j] = -rows[k][j]
			survivors := asteroidCollision(rows[k])
			left += int64(len(survivors))
			for _, a := range survivors {
				sum = (sum*31 + a + 1000) % 1000000007
			}
		}
	}
	fmt.Printf("500 rounds of 20 rows of 10000 asteroids: %d left, checksum %d\n", left, sum)
}
