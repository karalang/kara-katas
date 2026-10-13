// Benchmark for #496: Rust mirror of the ★ arm (a stack and a map); see
// next_greater_element.kara. std's HashMap hashes with SipHash, as
// Kāra's Map does.
use std::collections::HashMap;

fn next_greater_element(nums1: &[i64], nums2: &[i64]) -> Vec<i64> {
    let mut next: HashMap<i64, i64> = HashMap::new();
    let mut waiting: Vec<i64> = Vec::new();
    for &x in nums2 {
        while let Some(&top) = waiting.last() {
            if top >= x {
                break;
            }
            next.insert(top, x);
            waiting.pop();
        }
        waiting.push(x);
    }
    let mut out: Vec<i64> = Vec::new();
    for x in nums1 {
        match next.get(x) {
            Some(&g) => out.push(g),
            None => out.push(-1),
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10,000 cases, built once: nums2 is 1,000 distinct numbers from 0
    // to 10,000 (the problem's most), drawn by shuffling the front of a
    // pool of all of them, and nums1 is every other one of them from the
    // end. Then each case is solved once.
    let cases = 10000;
    let mut seed: i64 = 496;
    let mut pool: Vec<i64> = (0..10001).collect();
    let mut all1: Vec<Vec<i64>> = Vec::new();
    let mut all2: Vec<Vec<i64>> = Vec::new();
    for _ in 0..cases {
        for i in 0..1000 {
            let j = i + (next_random(&mut seed) % (10001 - i as i64)) as usize;
            pool.swap(i, j);
        }
        let nums2: Vec<i64> = pool[..1000].to_vec();
        let mut nums1: Vec<i64> = Vec::new();
        let mut k: i64 = 999;
        while k >= 0 {
            nums1.push(nums2[k as usize]);
            k -= 2;
        }
        all1.push(nums1);
        all2.push(nums2);
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for c in 0..cases {
        for a in next_greater_element(&all1[c], &all2[c]) {
            if a >= 0 {
                found += 1;
            }
            checksum = (checksum * 31 + a + 2) % 1000000007;
        }
    }
    println!("{cases} cases of 1000 and 500: {found} with a greater number, checksum {checksum}");
}
