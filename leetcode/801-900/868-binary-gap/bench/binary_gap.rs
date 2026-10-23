// LeetCode #868: Binary Gap -- Rust mirror of the bench program (the ★
// arm, one pass over the bits).

fn binary_gap(n: i64) -> i64 {
    let mut best = 0;
    let mut last = -1;
    let mut rest = n;
    let mut position = 0;
    while rest > 0 {
        if rest % 2 == 1 {
            if last >= 0 {
                best = best.max(position - last);
            }
            last = position;
        }
        rest /= 2;
        position += 1;
    }
    best
}

fn main() {
    let limit: i64 = 10000000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for n in 1..=limit {
        let g = binary_gap(n);
        total += g;
        check = (check * 31 + g) % 1000000007;
    }
    println!("n from 1 to {}: gaps sum to {}, checksum {}", limit, total, check);
}
