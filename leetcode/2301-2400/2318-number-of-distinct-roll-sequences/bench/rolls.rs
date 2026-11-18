// LeetCode #2318: Number of Distinct Roll Sequences -- the bench, the ★
// arm in Rust. The count of sequences ending in each pair of rolls, a 6
// by 6 table rolled forward once per roll, each next roll coprime with
// the last and unlike the last two. O(216 n).

fn gcd(a: i64, b: i64) -> i64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn distinct_sequences(n: i64) -> i64 {
    let modulus = 1000000007i64;
    if n == 1 {
        return 6;
    }
    let mut ends = [[0i64; 6]; 6];
    for a in 0..6 {
        for b in 0..6 {
            if a != b && gcd(a as i64 + 1, b as i64 + 1) == 1 {
                ends[a][b] = 1;
            }
        }
    }
    for _ in 2..n {
        let mut next = [[0i64; 6]; 6];
        for a in 0..6 {
            for b in 0..6 {
                if ends[a][b] > 0 {
                    for c in 0..6 {
                        if c != a && c != b && gcd(b as i64 + 1, c as i64 + 1) == 1 {
                            next[b][c] = (next[b][c] + ends[a][b]) % modulus;
                        }
                    }
                }
            }
        }
        ends = next;
    }
    let mut total = 0;
    for a in 0..6 {
        for b in 0..6 {
            total = (total + ends[a][b]) % modulus;
        }
    }
    total
}

fn main() {
    let mut check = 0i64;
    for p in 0..5 {
        for n in 9981..=10000 {
            check = (check * 31 + distinct_sequences(n) + p) % 1000000007;
        }
    }
    println!("5 passes over 20 counts of rolls up to 10^4: checksum {}", check);
}
