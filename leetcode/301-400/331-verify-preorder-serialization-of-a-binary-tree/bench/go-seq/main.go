// Benchmark workload for LeetCode #331 — mirrors verify_preorder.kara.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

const (
	NODES    = 100000
	VARIANTS = 16
	PUNCHES  = 160
	MODULUS  = 1073741789
)

var seed int64 = 331

func next() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func isValidSerialization(preorder string) bool {
	slots := int64(1)
	for _, tok := range strings.Split(preorder, ",") {
		if slots == 0 {
			return false
		}
		if tok == "#" {
			slots--
		} else {
			slots++
		}
	}
	return slots == 0
}

func tree(n int64, out *[]string) {
	if n == 0 {
		*out = append(*out, "#")
		return
	}
	*out = append(*out, strconv.FormatInt(next()%100, 10))
	left := next() % n
	tree(left, out)
	tree(n-1-left, out)
}

func main() {
	var tokens []string
	tree(NODES, &tokens)
	variants := make([]string, 0, VARIANTS)
	for v := int64(0); v < VARIANTS; v++ {
		kind := v % 4
		hi := next()
		at := (hi*32768 + next()) % int64(len(tokens))
		edited := make([]string, 0, len(tokens)+2)
		for i, t := range tokens {
			ii := int64(i)
			if ii == at && kind == 1 {
				continue
			}
			if ii == at && kind == 3 {
				edited = append(edited, "#")
			}
			if ii == at && kind == 2 && t == "#" {
				edited = append(edited, "7", "#")
			}
			edited = append(edited, t)
		}
		variants = append(variants, strings.Join(edited, ","))
	}
	var sink int64
	for p := 0; p < PUNCHES; p++ {
		v := next() % VARIANTS
		answer := int64(0)
		if isValidSerialization(variants[v]) {
			answer = 1
		}
		sink = (sink*1000003 + answer*64 + v) % MODULUS
	}
	fmt.Println(sink)
}
