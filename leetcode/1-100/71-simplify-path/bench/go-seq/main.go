// Benchmark workload — Go mirror of simplify.kara, single-goroutine.
//
// Same N=8 inputs, K=1_000_000 iters cycled by k % N. Sink is the
// sum of the simplified-output string lengths (i64). Output prints
// match the kara/rust/c/py mirrors so all five impls print the same
// number before timing.
//
// strings.Builder is the idiomatic per-iter String accumulator —
// roughly the same allocation shape as kara's f-string append and
// rust's String::new()+push.

package main

import (
	"fmt"
	"strings"
)

func simplify(s string) string {
	cs := []rune(s)
	n := int64(len(cs))

	starts := make([]int64, 0, 16)
	ends := make([]int64, 0, 16)

	var i int64 = 0
	for i < n {
		for i < n && cs[i] == '/' {
			i++
		}
		if i >= n {
			break
		}
		j := i
		for j < n && cs[j] != '/' {
			j++
		}
		length := j - i

		isDot := length == 1 && cs[i] == '.'
		isDotDot := length == 2 && cs[i] == '.' && cs[i+1] == '.'

		switch {
		case isDot:
			// skip
		case isDotDot:
			if len(starts) > 0 {
				starts = starts[:len(starts)-1]
				ends = ends[:len(ends)-1]
			}
		default:
			starts = append(starts, i)
			ends = append(ends, j)
		}
		i = j
	}

	if len(starts) == 0 {
		return "/"
	}

	var b strings.Builder
	for k := 0; k < len(starts); k++ {
		b.WriteRune('/')
		a := starts[k]
		e := ends[k]
		for p := a; p < e; p++ {
			b.WriteRune(cs[p])
		}
	}
	return b.String()
}

func main() {
	inputs := []string{
		"/home/",
		"/home/user/Documents/../Pictures",
		"/.../a/../b/c/../d/./",
		"/a/b/c/../..",
		"/a//b////c/d//././/..",
		"/abc_123",
		"/a/b/../c/../../d",
		"/...hidden",
	}
	var n int64 = int64(len(inputs))
	var kIters int64 = 1_000_000

	var sum int64 = 0
	for k := int64(0); k < kIters; k++ {
		r := simplify(inputs[k%n])
		sum += int64(len(r))
	}
	fmt.Println(sum)
}
