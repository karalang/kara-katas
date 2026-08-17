// LeetCode 277 bench mirror — Rust. Same algorithm as celebrity.kara.
const N: i64 = 2500000;
const INSTANCES: i64 = 64;

fn knows(star: i64, a: i64, b: i64) -> bool {
    if b == star { return true; }
    if a == star { return false; }
    let h = (a * 1103515245i64 + b * 12345i64) % 2147483647i64;
    h % 2 == 0
}

fn find_celebrity(n: i64, star: i64) -> i64 {
    let mut cand = 0i64;
    for i in 1..n {
        if knows(star, cand, i) { cand = i; }
    }
    for j in 0..n {
        if j != cand {
            if knows(star, cand, j) { return -1; }
            if !knows(star, j, cand) { return -1; }
        }
    }
    cand
}

fn main() {
    let mut sink = 0i64;
    for i in 0..INSTANCES {
        let star = (i * 7919) % N;
        sink = (sink + (i * 1000003 + find_celebrity(N, star)) % 1000000007) % 1000000007;
    }
    println!("{}", sink);
}
