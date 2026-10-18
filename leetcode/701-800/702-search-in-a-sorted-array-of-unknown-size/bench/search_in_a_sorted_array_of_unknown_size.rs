// LeetCode #702: Search in a Sorted Array of Unknown Size -- bench program, Rust mirror of the doubling arm.

struct ArrayReader {
    secret: Vec<i64>,
    reads: i64,
}

impl ArrayReader {
    fn get(&mut self, index: i64) -> i64 {
        self.reads += 1;
        if index < 0 || index >= self.secret.len() as i64 {
            return 2147483647;
        }
        self.secret[index as usize]
    }
}

fn search(reader: &mut ArrayReader, target: i64) -> i64 {
    let mut lo = 0;
    let mut hi = 1;
    while reader.get(hi) < target {
        lo = hi;
        hi *= 2;
    }
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        let v = reader.get(mid);
        if v == target {
            return mid;
        }
        if v < target {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 702;
    let mut readers: Vec<ArrayReader> = Vec::new();
    for _ in 0..100 {
        let mut secret: Vec<i64> = Vec::new();
        let mut v = -10000;
        for _ in 0..10000 {
            secret.push(v);
            v += 1 + next_random(&mut seed) % 2;
        }
        readers.push(ArrayReader { secret, reads: 0 });
    }
    let rounds = 5;
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for reader in readers.iter_mut() {
            let mut target = -10000;
            while target <= 10000 {
                let at = search(reader, target);
                if at >= 0 {
                    found += 1;
                    checksum = (checksum * 31 + at) % 1000000007;
                }
                target += 2;
            }
        }
    }
    let reads: i64 = readers.iter().map(|r| r.reads).sum();
    println!("{rounds} rounds of 100 arrays of 10000: {found} found, {reads} reads, checksum {checksum}");
}
