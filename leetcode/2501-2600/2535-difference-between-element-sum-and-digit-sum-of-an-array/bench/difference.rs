// LeetCode #2535 bench, Rust mirror of difference.kara.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn difference_of_sum(nums: &[i64]) -> i64 {
    let mut element_sum = 0;
    let mut digit_sum = 0;
    for &x in nums {
        element_sum += x;
        let mut rest = x;
        while rest > 0 {
            digit_sum += rest % 10;
            rest /= 10;
        }
    }
    (element_sum - digit_sum).abs()
}

fn main() {
    let passes: i64 = 1000;
    let n: i64 = 2000;
    let mut seed = 2535;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..50 {
        lists.push((0..n).map(|_| next_random(&mut seed) % 2000 + 1).collect());
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for q in 0..50 {
            let at = (check % n) as usize;
            lists[q][at] = (check + p) % 2000 + 1;
            check = (check * 31 + difference_of_sum(&lists[q]) + p) % 1000000007;
        }
    }
    println!("{} passes over 50 lists of 2000: checksum {}", passes, check);
}
