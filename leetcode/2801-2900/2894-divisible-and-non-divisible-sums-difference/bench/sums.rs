// LeetCode #2894: Divisible and Non-divisible Sums Difference -- the
// bench, as sums.kara: every n and m from 1 to 1000, 100 rounds, by the
// formula arm.

fn difference_of_sums(n: i64, m: i64) -> i64 {
    let k = n / m;
    n * (n + 1) / 2 - m * k * (k + 1)
}

fn main() {
    let (rounds, top) = (100i64, 1000i64);
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for n in 1..top + 1 {
            for m in 1..top + 1 {
                let d = difference_of_sums(n, (m + r) % top + 1);
                total += d;
                check = (check * 31 + d + 1000000) % 1000000007;
            }
        }
    }
    println!("{top} by {top} pairs, {rounds} rounds: differences total {total}, checksum {check}");
}
