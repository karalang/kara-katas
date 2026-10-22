// Benchmark for #858: Mirror Reflection -- Go twin of the Kāra trace arm (the
// ray traced from wall to wall), in every room LeetCode allows.
package main

import "fmt"

func mirrorReflection(p, q int64) int64 {
	var y int64
	up, east := true, false
	for {
		if up {
			y += q
			if y > p {
				y = 2*p - y
				up = false
			}
		} else {
			y -= q
			if y < 0 {
				y = -y
				up = true
			}
		}
		east = !east
		if y == p {
			if east {
				return 1
			}
			return 2
		}
		// the south-west corner is never reached, so this is the east wall
		if y == 0 {
			return 0
		}
	}
}

func main() {
	var counts [3]int64
	var check int64
	for p := int64(1); p <= 1000; p++ {
		for q := int64(1); q <= p; q++ {
			r := mirrorReflection(p, q)
			counts[r]++
			check = (check*3 + r) % 1000000007
		}
	}
	fmt.Printf("500500 rooms: receptor 0 %d times, 1 %d, 2 %d, checksum %d\n", counts[0], counts[1], counts[2], check)
}
