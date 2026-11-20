// LeetCode #2358: Maximum Number of Groups Entering a Competition -- the
// bench, the ★ arm in Rust: group sizes 1, 2, 3, ... added while the next
// still fits in the class.

fn maximum_groups(grades: &[i64]) -> i64 {
    let n = grades.len() as i64;
    let mut k = 0i64;
    let mut used = 0i64;
    while used + k + 1 <= n {
        k += 1;
        used += k;
    }
    k
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // class a holds 10^4 (a + 1) - a students graded 1 to 10^5
    let mut seed = 2358i64;
    let mut classes: Vec<Vec<i64>> = Vec::new();
    for a in 0..10i64 {
        let grades: Vec<i64> = (0..10000 * (a + 1) - a).map(|_| 1 + next_random(&mut seed) % 100000).collect();
        classes.push(grades);
    }
    let mut check = 0i64;
    for p in 0..20000i64 {
        for grades in &classes {
            check = (check * 31 + maximum_groups(grades) + p) % 1000000007;
        }
    }
    println!("20000 passes over 10 classes: checksum {}", check);
}
