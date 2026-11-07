// LeetCode #2001: Number of Pairs of Interchangeable Rectangles -- the
// benchmark, the same algorithm as rectangles.kara.
package main

import "fmt"

type ratio struct{ w, h int64 }

func gcd(a, b int64) int64 {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func interchangeable(rects []ratio) int64 {
	seen := map[ratio]int64{}
	var pairs int64
	for _, r := range rects {
		g := gcd(r.w, r.h)
		key := ratio{r.w / g, r.h / g}
		before := seen[key]
		pairs += before
		seen[key] = before + 1
	}
	return pairs
}

var seed int64 = 2001

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var calls, sum, check int64
	pools := []int64{10, 100, 1000, 10000}
	for a := 0; a < 20; a++ {
		shapes := pools[a%4]
		bases := make([]ratio, 0, shapes)
		for i := int64(0); i < shapes; i++ {
			w := nextRandom()%300 + 1
			h := nextRandom()%300 + 1
			bases = append(bases, ratio{w, h})
		}
		rects := make([]ratio, 0, 100000)
		for i := 0; i < 100000; i++ {
			b := bases[nextRandom()%shapes]
			side := b.w
			if b.h > side {
				side = b.h
			}
			m := nextRandom()%(100000/side) + 1
			rects = append(rects, ratio{b.w * m, b.h * m})
		}
		for i := 0; i < 10; i++ {
			answer := interchangeable(rects)
			sum += answer
			check = (check*31 + answer%1000003) % 1000000007
			calls++
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
