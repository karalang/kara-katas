// LeetCode #635: Design Log Storage System -- benchmark, Go.
//
// The ★ arm: timestamps compared as text after cutting them, and the
// bounds, to the granularity's length.
package main

import "fmt"

type entry struct {
	id        int64
	timestamp string
}

type LogSystem struct {
	logs []entry
}

func (s *LogSystem) Put(id int64, timestamp string) {
	s.logs = append(s.logs, entry{id, timestamp})
}

func length(granularity string) int {
	switch granularity {
	case "Year":
		return 4
	case "Month":
		return 7
	case "Day":
		return 10
	case "Hour":
		return 13
	case "Minute":
		return 16
	}
	return 19
}

func (s *LogSystem) Retrieve(start, end, granularity string) []int64 {
	n := length(granularity)
	low, high := start[:n], end[:n]
	var ids []int64
	for _, e := range s.logs {
		cut := e.timestamp[:n]
		if cut >= low && cut <= high {
			ids = append(ids, e.id)
		}
	}
	return ids
}

var seed int64 = 635

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomTime() string {
	year := 2000 + nextRandom()%18
	month := 1 + nextRandom()%12
	day := 1 + nextRandom()%31
	hour := nextRandom() % 24
	minute := nextRandom() % 60
	second := nextRandom() % 60
	return fmt.Sprintf("%d:%02d:%02d:%02d:%02d:%02d", year, month, day, hour, minute, second)
}

func main() {
	names := []string{"Year", "Month", "Day", "Hour", "Minute", "Second"}
	logs := &LogSystem{}
	for id := int64(1); id <= 20000; id++ {
		logs.Put(id, randomTime())
	}
	var found, checksum int64
	for r := 0; r < 2000; r++ {
		start := randomTime()
		end := randomTime()
		granularity := names[nextRandom()%6]
		for _, id := range logs.Retrieve(start, end, granularity) {
			found++
			checksum = (checksum*31 + id) % 1000000007
		}
	}
	fmt.Printf("20000 logs, 2000 retrieves: %d ids, checksum %d\n", found, checksum)
}
