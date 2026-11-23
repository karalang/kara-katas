// LeetCode #2525: Categorize Box According to Criteria -- Go mirror of the
// benchmark (box.kara): the same boxes, passes, order and checksum.
package main

import "fmt"

func categorizeBox(length, width, height, mass int64) string {
	bulky := length >= 10000 || width >= 10000 || height >= 10000 || length*width*height >= 1000000000
	heavy := mass >= 100
	switch {
	case bulky && heavy:
		return "Both"
	case bulky:
		return "Bulky"
	case heavy:
		return "Heavy"
	}
	return "Neither"
}

var seed int64 = 2525

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	boxes := make([][4]int64, 100000)
	for t := range boxes {
		top := int64(2000)
		if t%2 == 0 {
			top = 100000
		}
		boxes[t][0] = wideRandom()%top + 1
		boxes[t][1] = wideRandom()%top + 1
		boxes[t][2] = wideRandom()%top + 1
		boxes[t][3] = nextRandom()%1000 + 1
	}
	const passes = 220
	var check int64
	for p := int64(0); p < passes; p++ {
		start := check % 100000
		for i := int64(0); i < 100000; i++ {
			b := boxes[(start+i)%100000]
			name := categorizeBox(b[0], b[1], b[2], b[3])
			var code int64 = 4
			switch name {
			case "Both":
				code = 1
			case "Bulky":
				code = 2
			case "Heavy":
				code = 3
			}
			check = (check*31 + code + p) % 1000000007
		}
	}
	fmt.Printf("%d passes over 100000 boxes: checksum %d\n", passes, check)
}
