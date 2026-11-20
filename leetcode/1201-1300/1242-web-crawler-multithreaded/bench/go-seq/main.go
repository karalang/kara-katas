// LeetCode #1242 bench: the ★ arm in Go, a crawl by levels, each level's
// pages fetched by one goroutine each into its slot of the level's results,
// a WaitGroup joining them, over the same 50 webs of 1000 urls, 4 starts and
// 10 passes as the Kāra bench.
package main

import (
	"fmt"
	"strings"
	"sync"
)

type HtmlParser interface {
	GetUrls(url string) []string
}

func hostname(url string) string {
	return strings.SplitN(strings.TrimPrefix(url, "http://"), "/", 2)[0]
}

func crawl(startURL string, parser HtmlParser) []string {
	host := hostname(startURL)
	seen := map[string]bool{startURL: true}
	level := []string{startURL}
	for len(level) > 0 {
		pages := make([][]string, len(level))
		var wg sync.WaitGroup
		for i, url := range level {
			wg.Add(1)
			go func(i int, url string) {
				defer wg.Done()
				pages[i] = parser.GetUrls(url)
			}(i, url)
		}
		wg.Wait()
		var next []string
		for _, links := range pages {
			for _, u := range links {
				if hostname(u) == host && !seen[u] {
					seen[u] = true
					next = append(next, u)
				}
			}
		}
		level = next
	}
	out := make([]string, 0, len(seen))
	for u := range seen {
		out = append(out, u)
	}
	return out
}

type Site struct {
	links map[string][]string
}

func (s *Site) GetUrls(url string) []string {
	return append([]string(nil), s.links[url]...)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	names := []string{"news.yahoo.com", "news.google.com", "yahoo.com"}
	seed := int64(1242)
	type web struct {
		urls []string
		site *Site
	}
	var webs []web
	for w := 0; w < 50; w++ {
		urls := make([]string, 1000)
		for i := range urls {
			urls[i] = fmt.Sprintf("http://%s/page/%d", names[nextRandom(&seed)%3], i)
		}
		links := make(map[string][]string, 1000)
		for _, u := range urls {
			links[u] = nil
		}
		for k := 0; k < 5000; k++ {
			from := nextRandom(&seed) % 1000
			to := nextRandom(&seed) % 1000
			links[urls[from]] = append(links[urls[from]], urls[to])
		}
		webs = append(webs, web{urls, &Site{links}})
	}
	var check int64
	for pass := 0; pass < 10; pass++ {
		for _, w := range webs {
			for s := 0; s < 4; s++ {
				check = (check*131 + int64(len(crawl(w.urls[s*250], w.site)))) % 1000000007
			}
		}
	}
	fmt.Printf("50 webs of 1000 urls, 4 starts, 10 passes: checksum %d\n", check)
}
