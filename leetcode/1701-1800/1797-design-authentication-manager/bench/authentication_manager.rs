// LeetCode #1797: Design Authentication Manager -- the bench in Rust: the ★
// arm, a `HashMap` from each token to the second it expires, over 50
// random scripts of 2000 calls built once, 2000 runs.
use std::collections::HashMap;

struct AuthenticationManager {
    ttl: i32,
    expiry: HashMap<String, i32>,
}

impl AuthenticationManager {
    fn new(time_to_live: i32) -> Self {
        AuthenticationManager { ttl: time_to_live, expiry: HashMap::new() }
    }

    fn generate(&mut self, token_id: String, current_time: i32) {
        self.expiry.insert(token_id, current_time + self.ttl);
    }

    fn renew(&mut self, token_id: String, current_time: i32) {
        if let Some(&e) = self.expiry.get(&token_id) {
            if e > current_time {
                self.expiry.insert(token_id, current_time + self.ttl);
            }
        }
    }

    fn count_unexpired_tokens(&self, current_time: i32) -> i32 {
        self.expiry.values().filter(|&&e| e > current_time).count() as i32
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn name(k: i64) -> String {
    let letters = b"abcdefghijklmnopqrstuvwxyz";
    let mut s = String::new();
    let mut k = k;
    loop {
        s.push(letters[(k % 26) as usize] as char);
        k /= 26;
        if k == 0 {
            break;
        }
    }
    s
}

fn main() {
    let mut seed = 1797;
    let mut scripts: Vec<(i32, Vec<(i64, String, i32)>)> = Vec::new();
    for _ in 0..50 {
        let ttl = 1 + next_random(&mut seed) % 100000;
        let mut calls = Vec::new();
        let mut made = 0;
        let mut now = 0i64;
        for _ in 0..2000 {
            now += 1 + next_random(&mut seed) % 100;
            let pick = next_random(&mut seed) % 10;
            if pick < 4 {
                calls.push((0, name(made), now as i32));
                made += 1;
            } else if pick < 8 {
                calls.push((1, name(next_random(&mut seed) % (made + 2)), now as i32));
            } else {
                calls.push((2, String::new(), now as i32));
            }
        }
        scripts.push((ttl as i32, calls));
    }
    let mut check: i64 = 0;
    for run in 0..2000i64 {
        let (ttl, calls) = &scripts[((check + run) % 50) as usize];
        let mut m = AuthenticationManager::new(*ttl);
        for c in calls.iter() {
            match c.0 {
                0 => m.generate(c.1.clone(), c.2),
                1 => m.renew(c.1.clone(), c.2),
                _ => check = (check * 31 + m.count_unexpired_tokens(c.2) as i64) % 1000000007,
            }
        }
    }
    println!("2000 runs over 50 scripts of 2000 calls: checksum {}", check);
}
