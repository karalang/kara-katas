// LeetCode #1032: Stream of Characters -- bench
// Mirrors ./stream_checker.kara; see ../README.md § Benchmarks.

struct StreamChecker {
    next: Vec<Vec<i64>>,
    end: Vec<bool>,
    stream: Vec<i64>,
}

impl StreamChecker {
    fn new(words: Vec<String>) -> StreamChecker {
        let mut next: Vec<Vec<i64>> = vec![vec![-1; 26]];
        let mut end: Vec<bool> = vec![false];
        for word in words.iter() {
            let mut node = 0usize;
            for c in word.chars().rev() {
                let k = c as usize - 'a' as usize;
                if next[node][k] == -1 {
                    next[node][k] = next.len() as i64;
                    next.push(vec![-1; 26]);
                    end.push(false);
                }
                node = next[node][k] as usize;
            }
            end[node] = true;
        }
        StreamChecker { next, end, stream: Vec::new() }
    }

    fn query(&mut self, letter: char) -> bool {
        self.stream.push(letter as i64 - 'a' as i64);
        let mut node: i64 = 0;
        let mut i = self.stream.len();
        while i > 0 {
            i -= 1;
            node = self.next[node as usize][self.stream[i] as usize];
            if node == -1 {
                return false;
            }
            if self.end[node as usize] {
                return true;
            }
        }
        false
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(seed: &mut i64, len: i64) -> String {
    let mut s = String::new();
    for _ in 0..len {
        s.push((97 + next_random(seed) % 2) as u8 as char);
    }
    s
}

fn main() {
    let rounds = 50;
    let mut seed = 1032;
    let mut words: Vec<String> = Vec::new();
    for _ in 0..2000 {
        let len = 50 + next_random(&mut seed) % 151;
        words.push(random_text(&mut seed, len));
    }
    let stream = random_text(&mut seed, 40000);
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut checker = StreamChecker::new(words.clone());
        for c in stream.chars() {
            let hit = if checker.query(c) { 1 } else { 0 };
            found += hit;
            check = (check * 3 + hit + 1) % 1000000007;
        }
    }
    println!("2000 words, 40000 queries, {} rounds: {} found, checksum {}", rounds, found, check);
}
