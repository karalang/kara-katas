// LeetCode #1166: Design File System -- the ★ arm's bench in Rust: one
// HashMap from a made path to its value.

use std::collections::HashMap;

struct FileSystem {
    paths: HashMap<String, i64>,
}

impl FileSystem {
    fn new() -> FileSystem {
        FileSystem { paths: HashMap::new() }
    }

    fn create_path(&mut self, path: &str, value: i64) -> bool {
        if path.is_empty() || path == "/" || self.paths.contains_key(path) {
            return false;
        }
        let parent = &path[..path.rfind('/').unwrap()];
        if !parent.is_empty() && !self.paths.contains_key(parent) {
            return false;
        }
        self.paths.insert(path.to_string(), value);
        true
    }

    fn get(&self, path: &str) -> i64 {
        match self.paths.get(path) {
            Some(&v) => v,
            None => -1,
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let names = ["a", "b", "ab", "le", "leet", "code"];
    let mut seed = 1166;
    let mut paths: Vec<Vec<String>> = Vec::new();
    let mut creates: Vec<Vec<bool>> = Vec::new();
    for _ in 0..16 {
        let mut ps = Vec::new();
        let mut cs = Vec::new();
        for _ in 0..10000 {
            let parts = 1 + next_random(&mut seed) % 5;
            let mut p = String::new();
            for _ in 0..parts {
                p = p + "/" + names[(next_random(&mut seed) % 6) as usize];
            }
            ps.push(p);
            cs.push(next_random(&mut seed) % 4 != 0);
        }
        paths.push(ps);
        creates.push(cs);
    }
    let mut made: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..100 {
        for k in 0..16 {
            let from = (next_random(&mut seed) % 5000) as usize;
            let mut fs = FileSystem::new();
            for i in from..10000 {
                let a = if creates[k][i] {
                    if fs.create_path(&paths[k][i], i as i64) { 1 } else { 0 }
                } else {
                    fs.get(&paths[k][i])
                };
                if creates[k][i] {
                    made += a;
                }
                check = (check * 31 + a + 2) % 1000000007;
            }
        }
    }
    println!("100 rounds over 16 lists of 10^4 operations: made {made}, checksum {check}");
}
