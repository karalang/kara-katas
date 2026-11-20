// LeetCode #1237 bench: the ★ arm in Go, over the same 9 functions, z from
// 1 to 100 and 30 passes as the Kāra bench.
package main

import "fmt"

type CustomFunction struct {
	id int32
}

func (c *CustomFunction) f(x, y int32) int32 {
	switch c.id {
	case 1:
		return x + y
	case 2:
		return x * y
	case 3:
		return x*x + y
	case 4:
		return x + y*y
	case 5:
		return x*x + y*y
	case 6:
		return (x + y) * (x + y)
	case 7:
		return x*x*x + y*y*y
	case 8:
		return x * x * y
	default:
		return x * y * y
	}
}

func findSolution(c *CustomFunction, z int32) [][]int32 {
	var out [][]int32
	x, y := int32(1), int32(1000)
	for x <= 1000 && y >= 1 {
		v := c.f(x, y)
		if v < z {
			x++
		} else if v > z {
			y--
		} else {
			out = append(out, []int32{x, y})
			x++
			y--
		}
	}
	return out
}

func main() {
	var check int64
	for pass := 0; pass < 30; pass++ {
		for id := int32(1); id <= 9; id++ {
			for z := int32(1); z <= 100; z++ {
				for _, p := range findSolution(&CustomFunction{id}, z) {
					check = (check*131 + int64(p[0])*1001 + int64(p[1])) % 1000000007
				}
			}
		}
	}
	fmt.Printf("9 functions, z from 1 to 100, 30 passes: checksum %d\n", check)
}
