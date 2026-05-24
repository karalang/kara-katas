// LeetCode 6 — row-buffer Zigzag Conversion, Go seq mirror.
package main

import "fmt"

func convertOff(chars []rune, off, length, numRows int) []rune {
	if numRows <= 1 || numRows >= length {
		out := make([]rune, length)
		copy(out, chars[off:off+length])
		return out
	}

	rows := make([][]rune, numRows)
	cur := 0
	goingDown := false
	for i := 0; i < length; i++ {
		rows[cur] = append(rows[cur], chars[off+i])
		if cur == 0 || cur == numRows-1 {
			goingDown = !goingDown
		}
		if goingDown {
			cur++
		} else {
			cur--
		}
	}

	var out []rune
	for _, row := range rows {
		out = append(out, row...)
	}
	return out
}

func main() {
	const n = 10000
	const rPeriod = 1000
	const kIters = 10000
	const numRows = 4

	pattern := []rune("PAYPALISHIRING")
	need := n + rPeriod
	var chars []rune
	for len(chars) < need {
		chars = append(chars, pattern...)
	}

	var sum int64
	for k := 0; k < kIters; k++ {
		off := k % rPeriod
		result := convertOff(chars, off, n, numRows)
		last := len(result) - 1
		sum += int64(result[0]) + int64(result[last])
	}
	fmt.Println(sum)
}
