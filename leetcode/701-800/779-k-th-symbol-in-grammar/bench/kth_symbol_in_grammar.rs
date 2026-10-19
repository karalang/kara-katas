// Benchmark for #779: K-th Symbol in Grammar -- mirror of the ★ arm (the
// ones in k - 1), with the same workload as the Kāra program.

fn kth_grammar(_n: i64, k: i64) -> i64 {
    ((k - 1).count_ones() % 2) as i64
}

fn main() {
    let mut x: i64 = 779;
    let mut ones: i64 = 0;
    for _ in 0..200000000 {
        let k = 1 + x % 536870912;
        let answer = kth_grammar(30, k);
        ones += answer;
        x = (x * 1103515245 + 12345 + answer) % 2147483648;
    }
    println!("200000000 queries of row 30: {ones} ones, last state {x}");
}
