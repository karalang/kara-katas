// LeetCode #1472: Design Browser History -- bench, Rust mirror of
// browser_history.kara (LeetCode's Rust signatures: a visit takes an
// owned `String`, back and forward return one)

struct BrowserHistory {
    pages: Vec<String>,
    at: i64,
    end: i64,
}

impl BrowserHistory {
    fn new(homepage: String) -> Self {
        BrowserHistory { pages: vec![homepage], at: 0, end: 1 }
    }

    fn visit(&mut self, url: String) {
        self.at += 1;
        if (self.at as usize) < self.pages.len() {
            self.pages[self.at as usize] = url;
        } else {
            self.pages.push(url);
        }
        self.end = self.at + 1;
    }

    fn back(&mut self, steps: i32) -> String {
        self.at = (self.at - steps as i64).max(0);
        self.pages[self.at as usize].clone()
    }

    fn forward(&mut self, steps: i32) -> String {
        self.at = (self.at + steps as i64).min(self.end - 1);
        self.pages[self.at as usize].clone()
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn fold(check: i64, url: &str) -> i64 {
    let mut c = check;
    for &b in url.as_bytes() {
        c = (c * 131 + b as i64) % 1000000007;
    }
    c
}

fn main() {
    let pool: Vec<String> = (0..1000).map(|i| format!("site{i}.example.com")).collect();
    let mut seed: i64 = 1472;
    let mut check: i64 = 0;
    for _ in 0..400 {
        let mut h = BrowserHistory::new("home.example.com".to_string());
        for _ in 0..5000 {
            let r = next_random(&mut seed) % 3;
            let x = next_random(&mut seed);
            if r == 0 {
                h.visit(pool[(x % 1000) as usize].clone());
            } else if r == 1 {
                check = fold(check, &h.back((1 + x % 10) as i32));
            } else {
                check = fold(check, &h.forward((1 + x % 10) as i32));
            }
        }
    }
    println!("400 sessions of 5000 calls: checksum {check}");
}
