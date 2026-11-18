// LeetCode #2320: Count Number of Ways to Place Houses -- the bench, the
// ★ arm in Rust. One side's placements ending in an empty plot and in a
// house rolled forward a plot at a time, and their sum squared. O(n).

fn count_house_placements(n: i64) -> i64 {
    let modulus: i64 = 1000000007;
    let mut empty: i64 = 1;
    let mut house: i64 = 1;
    for _ in 1..n {
        let next_empty = (empty + house) % modulus;
        house = empty;
        empty = next_empty;
    }
    let side = (empty + house) % modulus;
    side * side % modulus
}

fn main() {
    let mut check: i64 = 0;
    for p in 0..10 {
        for n in 1..=10000 {
            check = (check * 31 + count_house_placements(n) + p) % 1000000007;
        }
    }
    println!("10 passes over every count of plots up to 10^4: checksum {}", check);
}
