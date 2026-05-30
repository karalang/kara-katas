// Benchmark workload — Valid Parentheses (LeetCode #20).
// Go single-threaded mirror of bench/valid_parentheses.{kara,rs,c}.
// Idiomatic Go: byte slices grown via append (GC-managed, no manual
// free), a fresh stack slice per call. Same depth/K, type rotation,
// 1/7 corruption, and count-valid sink. Built with `go build` (Go has no
// -O flag; the default build is already optimized). See ../README.md.

package main

import "fmt"

func isValidBytes(bytes []byte) bool {
	stack := make([]byte, 0)
	for _, b := range bytes {
		if b == '(' || b == '[' || b == '{' {
			var closer byte
			switch b {
			case '(':
				closer = ')'
			case '[':
				closer = ']'
			default:
				closer = '}'
			}
			stack = append(stack, closer)
		} else {
			if len(stack) == 0 {
				return false
			}
			top := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			if top != b {
				return false
			}
		}
	}
	return len(stack) == 0
}

func buildBrackets(depth int64, kind int64, corrupt bool) []byte {
	var op, cl, wrong byte = '(', ')', ']'
	switch kind {
	case 1:
		op, cl, wrong = '[', ']', ')'
	case 2:
		op, cl, wrong = '{', '}', ')'
	}
	buf := make([]byte, 0)
	for i := int64(0); i < depth; i++ {
		buf = append(buf, op)
	}
	for i := int64(0); i < depth-1; i++ {
		buf = append(buf, cl)
	}
	if corrupt {
		buf = append(buf, wrong)
	} else {
		buf = append(buf, cl)
	}
	return buf
}

func main() {
	const depth int64 = 1000
	const kIters int64 = 500_000

	var count int64
	for k := int64(0); k < kIters; k++ {
		kind := k % 3
		corrupt := (k % 7) == 0
		buf := buildBrackets(depth, kind, corrupt)
		if isValidBytes(buf) {
			count++
		}
	}
	fmt.Println(count)
}
