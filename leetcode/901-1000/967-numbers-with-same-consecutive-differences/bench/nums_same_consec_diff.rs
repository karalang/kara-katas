// Benchmark: LeetCode #967 Numbers With Same Consecutive Differences --
// the ★ arm, level by level, for every n from 2 to 9 and every k from 0
// to 9. Mirrors nums_same_consec_diff.kara, .c, .py and go-seq/.

fn nums_same_consec_diff(n: i64, k: i64) -> Vec<i64> {
    let mut level: Vec<i64> = (1..10).collect();
    for _ in 1..n {
        let mut next = Vec::new();
        for &x in &level {
            let last = x % 10;
            if last + k <= 9 {
                next.push(x * 10 + last + k);
            }
            if k > 0 && last - k >= 0 {
                next.push(x * 10 + last - k);
            }
        }
        level = next;
    }
    level
}

fn main() {
    let rounds = 2000;
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for n in 2..10 {
            for k in 0..10 {
                for x in nums_same_consec_diff(n, k) {
                    found += 1;
                    check = (check * 31 + x) % 1000000007;
                }
            }
        }
    }
    println!("{rounds} rounds over n from 2 to 9 and k from 0 to 9: {found} numbers, checksum {check}");
}
