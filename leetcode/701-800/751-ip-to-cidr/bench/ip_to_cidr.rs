// LeetCode 751 — IP to CIDR, bench: the ★ arm (greedy by the lowest
// set bit) on half a million ranges from a pool of 1000 addresses.
// Mirrors ip_to_cidr.kara.

fn address(ip: &str) -> i64 {
    ip.split('.').fold(0, |x, part| x * 256 + part.parse::<i64>().unwrap())
}

fn dotted(x: i64) -> String {
    format!("{}.{}.{}.{}", x / 16777216 % 256, x / 65536 % 256, x / 256 % 256, x % 256)
}

fn ip_to_cidr(ip: &str, n: i64) -> Vec<String> {
    let mut x = address(ip);
    let mut left = n;
    let mut out = Vec::new();
    while left > 0 {
        let mut size = if x == 0 { 4294967296 } else { x & -x };
        while size > left {
            size /= 2;
        }
        let mut bits = 0;
        while (1i64 << bits) < size {
            bits += 1;
        }
        out.push(format!("{}/{}", dotted(x), 32 - bits));
        x += size;
        left -= size;
    }
    out
}

struct Rng(i64);
impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let queries = 500000;
    let mut rng = Rng(751);
    let pool: Vec<String> = (0..1000)
        .map(|_| {
            let a = rng.next() % 255;
            let b = rng.next() % 256;
            let c = rng.next() % 256;
            let d = rng.next() % 256;
            format!("{}.{}.{}.{}", a, b, c, d)
        })
        .collect();
    let mut blocks = 0i64;
    let mut check = 0i64;
    for q in 0..queries {
        let n = 1 + rng.next() % 1000;
        let found = ip_to_cidr(&pool[q % 1000], n);
        blocks += found.len() as i64;
        for block in &found {
            check = (check * 31 + block.len() as i64) % 1000000007;
        }
    }
    println!("{} ranges: {} blocks in all, checksum {}", queries, blocks, check);
}
