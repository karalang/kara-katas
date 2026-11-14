// LeetCode #1537: Get the Maximum Score -- bench: the ★ arm over 100
// random pairs of arrays built from 100000 values each, steps up to 50,
// built once and answered 20 times. Rust mirror of score.kara.

fn max_sum(nums1: &[i64], nums2: &[i64]) -> i64 {
    let (n, m) = (nums1.len(), nums2.len());
    let (mut i, mut j) = (0, 0);
    let (mut a, mut b) = (0i64, 0i64);
    while i < n || j < m {
        if i < n && (j == m || nums1[i] < nums2[j]) {
            a += nums1[i];
            i += 1;
        } else if j < m && (i == n || nums2[j] < nums1[i]) {
            b += nums2[j];
            j += 1;
        } else {
            let best = a.max(b) + nums1[i];
            a = best;
            b = best;
            i += 1;
            j += 1;
        }
    }
    a.max(b) % 1000000007
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn arrays(count: i64, gap: i64, seed: &mut i64) -> (Vec<i64>, Vec<i64>) {
    let mut first = Vec::new();
    let mut second = Vec::new();
    let mut value = 0;
    let both = next_random(seed) % 30 + 1;
    for _ in 0..count {
        value += next_random(seed) % gap + 1;
        let roll = next_random(seed) % 100;
        if roll < both {
            first.push(value);
            second.push(value);
        } else if roll < 50 + both / 2 {
            first.push(value);
        } else {
            second.push(value);
        }
    }
    if first.is_empty() {
        first.push(value + 1);
    }
    if second.is_empty() {
        second.push(value + 2);
    }
    (first, second)
}

fn main() {
    let mut seed = 1537i64;
    let pairs: Vec<(Vec<i64>, Vec<i64>)> = (0..100).map(|_| arrays(100000, 50, &mut seed)).collect();
    let mut check = 0;
    for _ in 0..20 {
        for (first, second) in &pairs {
            check = mix(check, max_sum(first, second));
        }
    }
    println!("20 passes over 100 pairs of 100000 values: checksum {}", check);
}
