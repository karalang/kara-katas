package main

import "fmt"

// The Go mirror of build_array.kara. Go's strings are immutable, so each
// operation appends the literal's header and copies no bytes.
func buildArray(target []int32, n int32) []string {
	ops := []string{}
	next := 0
	for x := int32(1); x <= n; x++ {
		if next == len(target) {
			break
		}
		ops = append(ops, "Push")
		if target[next] == x {
			next++
		} else {
			ops = append(ops, "Pop")
		}
	}
	return ops
}

func main() {
	seed := int64(1441)
	targets := [][]int32{}
	for t := 0; t < 1000; t++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		keep := 1 + seed/65536%100
		target := []int32{}
		for x := int32(1); x <= 100; x++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			if seed/65536%100 < keep {
				target = append(target, x)
			}
		}
		if len(target) == 0 {
			target = append(target, 100)
		}
		targets = append(targets, target)
	}
	check := int64(0)
	for r := 0; r < 200; r++ {
		for _, target := range targets {
			ops := buildArray(target, 100)
			h := int64(0)
			for _, op := range ops {
				v := int64(2)
				if op == "Push" {
					v = 1
				}
				h = (h*3 + v) % 1000000007
			}
			check = (check*131 + h) % 1000000007
		}
	}
	fmt.Printf("2 * 10^5 targets: checksum %d\n", check)
}
