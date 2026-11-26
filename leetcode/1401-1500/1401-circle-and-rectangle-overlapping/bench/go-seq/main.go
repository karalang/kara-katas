// LeetCode #1401 bench, Go: the same clamp and squared distance, workload
// and checksum as check_overlap.kara.
package main

import "fmt"

func clamp(v, lo, hi int32) int32 {
	if v < lo {
		return lo
	}
	if v > hi {
		return hi
	}
	return v
}

func checkOverlap(radius, xCenter, yCenter, x1, y1, x2, y2 int32) bool {
	dx := clamp(xCenter, x1, x2) - xCenter
	dy := clamp(yCenter, y1, y2) - yCenter
	return dx*dx+dy*dy <= radius*radius
}

func main() {
	var seed int64 = 1401
	cases := make([][]int32, 0, 100000)
	for i := 0; i < 100000; i++ {
		v := make([]int32, 0, 7)
		for k := 0; k < 5; k++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			v = append(v, int32(seed%2001-1000))
		}
		seed = (seed*1103515245 + 12345) % 2147483648
		w := int32(1 + seed%300)
		seed = (seed*1103515245 + 12345) % 2147483648
		h := int32(1 + seed%300)
		if v[0] < 0 {
			v[0] = -v[0]
		}
		v[0] = v[0]/10 + 1
		v = append(v, v[3]+w, v[4]+h)
		cases = append(cases, v)
	}
	var check int64
	for round := int32(0); round < 1000; round++ {
		var overlaps int64
		for _, c := range cases {
			if checkOverlap(c[0]+round, c[1], c[2], c[3], c[4], c[5], c[6]) {
				overlaps++
			}
		}
		check = (check*131 + overlaps) % 1000000007
	}
	fmt.Printf("1000 rounds over 10^5 circles and rectangles: checksum %d\n", check)
}
