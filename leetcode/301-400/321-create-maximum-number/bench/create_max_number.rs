// Benchmark mirror of LeetCode #321 — same split-shrink-merge as
// bench/create_max_number.kara.

const LEN1: i64 = 1500;
const LEN2: i64 = 1700;
const PASSES: i64 = 24;
const MODULUS: i64 = 1073741789;

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn shrink(nums: &[i64], keep: i64, out: &mut [i64]) {
    let mut top: i64 = 0;
    let mut drop = nums.len() as i64 - keep;
    for &d in nums {
        while drop > 0 && top > 0 && out[(top - 1) as usize] < d {
            top -= 1;
            drop -= 1;
        }
        if top < keep {
            out[top as usize] = d;
            top += 1;
        } else {
            drop -= 1;
        }
    }
}

fn suffix_greater(a: &[i64], alen: i64, i: i64, b: &[i64], blen: i64, j: i64) -> bool {
    let mut x = i;
    let mut y = j;
    while x < alen && y < blen && a[x as usize] == b[y as usize] {
        x += 1;
        y += 1;
    }
    if y == blen {
        return x < alen;
    }
    if x == alen {
        return false;
    }
    a[x as usize] > b[y as usize]
}

fn merge(a: &[i64], alen: i64, b: &[i64], blen: i64, out: &mut [i64]) {
    let mut i = 0;
    let mut j = 0;
    let mut t = 0usize;
    while i < alen || j < blen {
        if suffix_greater(a, alen, i, b, blen, j) {
            out[t] = a[i as usize];
            i += 1;
        } else {
            out[t] = b[j as usize];
            j += 1;
        }
        t += 1;
    }
}

fn main() {
    let mut seed: i64 = 321;
    let mut sink: i64 = 0;
    let mut digits_out: i64 = 0;

    let cap = (LEN1 + LEN2) as usize;
    let mut left = vec![0i64; cap];
    let mut right = vec![0i64; cap];
    let mut cand = vec![0i64; cap];
    let mut best = vec![0i64; cap];

    for p in 0..PASSES {
        let nums1: Vec<i64> = (0..LEN1).map(|_| next(&mut seed) % 10).collect();
        let nums2: Vec<i64> = (0..LEN2).map(|_| next(&mut seed) % 10).collect();

        let ks = [LEN1 / 3, (LEN1 + LEN2) / 2, LEN1 + LEN2 - 7 * (p + 1)];
        for &k in &ks {
            let lo = if k - LEN2 < 0 { 0 } else { k - LEN2 };
            let hi = if k > LEN1 { LEN1 } else { k };
            let mut have = false;
            for i in lo..=hi {
                shrink(&nums1, i, &mut left);
                shrink(&nums2, k - i, &mut right);
                merge(&left, i, &right, k - i, &mut cand);
                if !have || suffix_greater(&cand, k, 0, &best, k, 0) {
                    best[..k as usize].copy_from_slice(&cand[..k as usize]);
                    have = true;
                }
            }

            let mut acc: i64 = 0;
            for x in 0..k as usize {
                acc = (acc * 131 + best[x] + 1) % MODULUS;
            }
            sink = (sink * 1000003 + acc) % MODULUS;
            digits_out += k;
        }
    }

    println!("sink {} digits {}", sink, digits_out);
}
