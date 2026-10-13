// Benchmark for #535: the ★ arm (a counter written in base 62); see
// ../README.md § Benchmarks. Mirrors encode_and_decode_tinyurl.kara.

use std::collections::HashMap;

const PREFIX: &str = "http://tinyurl.com/";

fn digit(d: i64) -> char {
    if d < 10 {
        (b'0' + d as u8) as char
    } else if d < 36 {
        (b'a' + (d - 10) as u8) as char
    } else {
        (b'A' + (d - 36) as u8) as char
    }
}

fn base62(n: i64) -> String {
    let mut rev: Vec<char> = Vec::new();
    let mut m = n;
    loop {
        rev.push(digit(m % 62));
        m /= 62;
        if m == 0 {
            break;
        }
    }
    let mut code = String::new();
    for i in (0..rev.len()).rev() {
        code.push(rev[i]);
    }
    code
}

struct Codec {
    by_code: HashMap<String, String>,
    by_url: HashMap<String, String>,
    next: i64,
}

impl Codec {
    fn new() -> Codec {
        Codec { by_code: HashMap::new(), by_url: HashMap::new(), next: 0 }
    }

    fn encode(&mut self, long_url: &str) -> String {
        let code = match self.by_url.get(long_url) {
            Some(code) => code.clone(),
            None => {
                let code = base62(self.next);
                self.next += 1;
                self.by_code.insert(code.clone(), long_url.to_string());
                self.by_url.insert(long_url.to_string(), code.clone());
                code
            }
        };
        PREFIX.to_string() + &code
    }

    fn decode(&self, short_url: &str) -> String {
        self.by_code.get(&short_url[PREFIX.len()..]).unwrap().clone()
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_url(seed: &mut i64, most: i64) -> String {
    let marks = b"/-_.?=&";
    let mut url = "https://".to_string();
    let host = 3 + next_random(seed) % 8;
    for _ in 0..host {
        url.push((b'a' + (next_random(seed) % 26) as u8) as char);
    }
    url.push_str(".com/");
    let path = next_random(seed) % (most + 1);
    for _ in 0..path {
        let k = next_random(seed) % 69;
        if k < 26 {
            url.push((b'a' + k as u8) as char);
        } else if k < 52 {
            url.push((b'A' + (k - 26) as u8) as char);
        } else if k < 62 {
            url.push((b'0' + (k - 52) as u8) as char);
        } else {
            url.push(marks[(k - 62) as usize] as char);
        }
    }
    url
}

fn main() {
    let mut seed: i64 = 535;
    let mut urls: Vec<String> = Vec::new();
    for i in 0..20000 {
        if i % 5 == 4 {
            let j = (next_random(&mut seed) % urls.len() as i64) as usize;
            urls.push(urls[j].clone());
        } else {
            urls.push(random_url(&mut seed, 100));
        }
    }
    let rounds = 50;
    let mut right: i64 = 0;
    let mut length: i64 = 0;
    for _ in 0..rounds {
        let mut codec = Codec::new();
        let mut shorts: Vec<String> = Vec::new();
        for u in urls.iter() {
            let s = codec.encode(u);
            length += s.len() as i64;
            shorts.push(s);
        }
        for i in 0..urls.len() {
            if codec.decode(&shorts[i]) == urls[i] {
                right += 1;
            }
        }
    }
    println!("{} URLs, {} rounds: {} back, short length {}", urls.len(), rounds, right, length);
}
