// LeetCode #2064: Minimized Maximum of Products Distributed to Any Store --
// Rust mirror of the ★ arm's benchmark (stores.kara): 200 problems of 50000
// types, quantities from 1 to 100000, and from 50000 to 100000 stores.

fn minimized_maximum(n: i64, quantities: &[i64]) -> i64 {
    let mut lo = 1;
    let mut hi = *quantities.iter().max().unwrap();
    while lo < hi {
        let mid = (lo + hi) / 2;
        let mut need = 0;
        for &q in quantities {
            need += (q + mid - 1) / mid;
        }
        if need <= n {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2064i64;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..200 {
        let mut qs: Vec<i64> = Vec::new();
        for _ in 0..50000 {
            let hi = next_random(&mut seed);
            qs.push((hi * 32768 + next_random(&mut seed)) % 100000 + 1);
        }
        let hi = next_random(&mut seed);
        let n = 50000 + (hi * 32768 + next_random(&mut seed)) % 50001;
        let a = minimized_maximum(n, &qs);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("200 problems: sum {}, checksum {}", total, check);
}
