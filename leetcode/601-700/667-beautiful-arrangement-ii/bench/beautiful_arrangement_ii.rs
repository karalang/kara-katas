// Benchmark for #667: zigzag from both ends, as the Kara ★ arm.

fn construct_array(n: i64, k: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let (mut lo, mut hi) = (1, k + 1);
    while lo <= hi {
        out.push(lo);
        lo += 1;
        if lo <= hi {
            out.push(hi);
            hi -= 1;
        }
    }
    for x in k + 2..n + 1 {
        out.push(x);
    }
    out
}

fn main() {
    let n: i64 = 10000;
    let rounds: i64 = 10000;
    let mut sum: i64 = 0;
    for r in 0..rounds {
        let k = 1 + r * 7919 % (n - 1);
        let a = construct_array(n, k);
        for &x in a.iter() {
            sum = (sum * 31 + x) % 1000000007;
        }
    }
    println!("n = {}, {} rounds: checksum {}", n, rounds, sum);
}
