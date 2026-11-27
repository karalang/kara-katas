// LeetCode #1823: Find the Winner of the Circular Game -- the bench in
// Rust: the ★ arm over 200000 calls on circles of 250 to 499 friends, each
// circle's size and count drawn from the checksum so far.

fn find_the_winner(n: i64, k: i64) -> i64 {
    let mut winner = 0;
    for i in 2..n + 1 {
        winner = (winner + k) % i;
    }
    winner + 1
}

fn main() {
    let mut check: i64 = 0;
    for call in 0..200000 {
        let n = 250 + (check + call) % 250;
        let k = 1 + (check * 7 + call) % n;
        check = (check * 41 + find_the_winner(n, k)) % 1000000007;
    }
    println!("200000 calls: checksum {}", check);
}
