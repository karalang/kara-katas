// LeetCode #1242 bench: the ★ arm in Rust, a crawl by levels, each level's
// pages fetched by up to 8 scoped threads, each a contiguous part of the
// level, the handles joined in order,
// over the same 50 webs of 1000 urls, 4 starts and 10 passes as the Kāra
// bench.

use std::collections::{HashMap, HashSet};

trait HtmlParser: Sync {
    fn get_urls(&self, url: &str) -> Vec<String>;
}

fn hostname(url: &str) -> &str {
    url.strip_prefix("http://").unwrap().split('/').next().unwrap()
}

fn crawl(start_url: &str, parser: &dyn HtmlParser) -> Vec<String> {
    let host = hostname(start_url).to_string();
    let mut seen: HashSet<String> = HashSet::new();
    seen.insert(start_url.to_string());
    let mut level = vec![start_url.to_string()];
    while !level.is_empty() {
        // A thread per eighth of the level: an OS thread per page, as the
        // Kāra arm spawns a task per page, costs tens of microseconds each.
        let chunk = level.len().div_ceil(8);
        let pages: Vec<Vec<String>> = std::thread::scope(|s| {
            let handles: Vec<_> = level
                .chunks(chunk)
                .map(|part| s.spawn(move || part.iter().map(|url| parser.get_urls(url)).collect::<Vec<_>>()))
                .collect();
            handles.into_iter().flat_map(|h| h.join().unwrap()).collect()
        });
        let mut next_level = Vec::new();
        for links in pages {
            for next in links {
                if hostname(&next) == host && seen.insert(next.clone()) {
                    next_level.push(next);
                }
            }
        }
        level = next_level;
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
    let mut seed = 1242;
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
    for _ in 0..10 {
        for (urls, web) in &webs {
            for s in 0..4 {
                check = (check * 131 + crawl(&urls[s * 250], web).len() as i64) % 1000000007;
            }
        }
    }
    println!("50 webs of 1000 urls, 4 starts, 10 passes: checksum {check}");
}
