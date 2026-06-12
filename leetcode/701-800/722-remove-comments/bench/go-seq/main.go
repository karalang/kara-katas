// LeetCode #722 bench harness — Go peer (go build, single-thread).
//
// Byte-indexed segment-slicing — same canonical algorithm as the Kara mirror:
// scan each line's bytes, classify `/` `*` markers, and append each surviving
// run as one slice (no per-char append). Sink = 30960000.
package main

import "fmt"

const (
	reps  = 60
	iters = 4000
)

var template = []string{
	"int main() {            // entry point",
	"  int a = 1; /* inline */ int b = 2;",
	"  /* a multi-line",
	"     block comment that",
	"     spans several lines */ int c = a + b;",
	"  // a full line comment",
	"  int e = c * 3;        /* trailing block */",
	"  int d = a /* x */ + b /* y */ + c;",
	"  return d * 2;//done",
	"}",
}

func removeComments(source []string) []string {
	result := make([]string, 0, len(source))
	buffer := make([]byte, 0, 64)
	inBlock := false
	for _, line := range source {
		n := len(line)
		segStart := 0
		i := 0
		for i < n {
			if !inBlock {
				if i+1 < n && line[i] == '/' && line[i+1] == '/' {
					buffer = append(buffer, line[segStart:i]...)
					segStart = n
					break
				} else if i+1 < n && line[i] == '/' && line[i+1] == '*' {
					buffer = append(buffer, line[segStart:i]...)
					inBlock = true
					i += 2
				} else {
					i++
				}
			} else {
				if i+1 < n && line[i] == '*' && line[i+1] == '/' {
					inBlock = false
					i += 2
					segStart = i
				} else {
					i++
				}
			}
		}
		if !inBlock {
			buffer = append(buffer, line[segStart:n]...)
			if len(buffer) > 0 {
				result = append(result, string(buffer))
				buffer = buffer[:0]
			}
		}
	}
	return result
}

func passLen(source []string) int64 {
	var total int64
	for _, s := range removeComments(source) {
		total += int64(len(s))
	}
	return total
}

func main() {
	lines := make([]string, 0, reps*len(template))
	for r := 0; r < reps; r++ {
		lines = append(lines, template...)
	}
	var sum int64
	for it := 0; it < iters; it++ {
		sum += passLen(lines)
	}
	fmt.Println(sum)
}
