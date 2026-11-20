// LeetCode #1236 bench: the ★ arm in Rust, over the same 50 webs of 1000
// urls, 4 starts and 100 passes as the Kāra bench.

use std::collections::{HashMap, HashSet, VecDeque};

trait HtmlParser {
    fn get_urls(&self, url: &str) -> Vec<String>;
}

fn hostname(url: &str) -> &str {
    url.strip_prefix("http://").unwrap().split('/').next().unwrap()
}

fn crawl(start_url: &str, parser: &dyn HtmlParser) -> Vec<String> {
    let host = hostname(start_url).to_string();
    let mut seen: HashSet<String> = HashSet::new();
    let mut queue: VecDeque<String> = VecDeque::new();
    seen.insert(start_url.to_string());
    queue.push_back(start_url.to_string());
    while let Some(url) = queue.pop_front() {
        for next in parser.get_urls(&url) {
            if hostname(&next) == host && !seen.contains(&next) {
                seen.insert(next.clone());
                queue.push_back(next);
            }
        }
    }
    seen.into_iter().collect()
}

struct Site {
    links: HashMap<String, Vec<String>>,
}

impl HtmlParser for Site {
    fn get_urls(&self, url: &str) -> Vec<String> {
        self.links.get(url).cloned().unwrap_or_default()
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let names = ["news.yahoo.com", "news.google.com", "yahoo.com"];
    let mut seed = 1236;
    let mut webs: Vec<(Vec<String>, Site)> = Vec::new();
    for _ in 0..50 {
        let urls: Vec<String> = (0..1000)
            .map(|i| format!("http://{}/page/{i}", names[(next_random(&mut seed) % 3) as usize]))
            .collect();
        let mut links: HashMap<String, Vec<String>> = HashMap::new();
        for url in &urls {
            links.insert(url.clone(), Vec::new());
        }
        for _ in 0..5000 {
            let from = (next_random(&mut seed) % 1000) as usize;
            let to = (next_random(&mut seed) % 1000) as usize;
            links.get_mut(&urls[from]).unwrap().push(urls[to].clone());
        }
        webs.push((urls, Site { links }));
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        for (urls, web) in &webs {
            for s in 0..4 {
                check = (check * 131 + crawl(&urls[s * 250], web).len() as i64) % 1000000007;
            }
        }
    }
    println!("50 webs of 1000 urls, 4 starts, 100 passes: checksum {check}");
}
