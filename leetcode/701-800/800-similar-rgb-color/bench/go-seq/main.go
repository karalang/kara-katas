// LeetCode 800 — Similar RGB Color: the bench, in Go. Mirrors
// similar_rgb.kara: each part rounded to the nearest doubled digit.
package main

import "fmt"

const digits = "0123456789abcdef"

func digit(c byte) int64 {
	if c >= 48 && c <= 57 {
		return int64(c) - 48
	}
	return int64(c) - 97 + 10
}

func similarRGB(color string) string {
	out := make([]byte, 0, 7)
	out = append(out, '#')
	for p := 0; p < 3; p++ {
		part := digit(color[1+2*p])*16 + digit(color[2+2*p])
		d := digits[(part+8)/17]
		out = append(out, d, d)
	}
	return string(out)
}

var seed int64 = 800

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	colors := make([]string, 0, 4096)
	for i := 0; i < 4096; i++ {
		b := []byte{'#'}
		for j := 0; j < 6; j++ {
			b = append(b, digits[nextRandom()%16])
		}
		colors = append(colors, string(b))
	}
	var rounds int64 = 40960000
	var check int64
	for r := int64(0); r < rounds; r++ {
		got := similarRGB(colors[r%4096])
		check = (check*31 + int64(got[1])*65536 + int64(got[3])*256 + int64(got[5])) % 1000000007
	}
	fmt.Printf("%d colours: checksum %d\n", rounds, check)
}
