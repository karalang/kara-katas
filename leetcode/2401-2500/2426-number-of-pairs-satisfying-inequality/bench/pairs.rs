// LeetCode #2426: Number of Pairs Satisfying Inequality -- the bench, the
// ★ arm: with `a[i] = nums1[i] - nums2[i]`, a merge sort counting the
// pairs `i < j` with `a[i] <= a[j] + diff`.

fn count_pairs(a: &mut Vec<i64>, lo: usize, hi: usize, diff: i64) -> i64 {
    if hi - lo < 2 {
        return 0;
    }
    let mid = (lo + hi) / 2;
    let mut count = count_pairs(a, lo, mid, diff) + count_pairs(a, mid, hi, diff);
    let mut p = lo;
    for j in mid..hi {
        while p < mid && a[p] <= a[j] + diff {
            p += 1;
        }
        count += (p - lo) as i64;
    }
    let mut merged: Vec<i64> = Vec::new();
    let mut i = lo;
    let mut j = mid;
    while i < mid || j < hi {
        if j == hi || (i < mid && a[i] <= a[j]) {
            merged.push(a[i]);
            i += 1;
        } else {
            merged.push(a[j]);
            j += 1;
        }
    }
    for k in 0..merged.len() {
        a[lo + k] = merged[k];
    }
    count
}

fn number_of_pairs(nums1: &[i64], nums2: &[i64], diff: i64) -> i64 {
    let mut a: Vec<i64> = Vec::new();
    for i in 0..nums1.len() {
        a.push(nums1[i] - nums2[i]);
    }
    let n = a.len();
    count_pairs(&mut a, 0, n, diff)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2426;
    let mut firsts: Vec<Vec<i64>> = Vec::new();
    let mut seconds: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut nums1: Vec<i64> = Vec::new();
        let mut nums2: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            nums1.push(next_random(&mut seed) % 20001 - 10000);
            nums2.push(next_random(&mut seed) % 20001 - 10000);
        }
        firsts.push(nums1);
        seconds.push(nums2);
    }
    let mut check: i64 = 0;
    for p in 0..4i64 {
        for c in 0..10usize {
            let diff = 2000 * c as i64 - 10000 + p - 2;
            check = (check * 31 + number_of_pairs(&firsts[c], &seconds[c], diff) + p) % 1000000007;
        }
    }
    println!("4 passes over 10 cases of 10^5 values: checksum {}", check);
}
