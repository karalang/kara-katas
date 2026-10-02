// Benchmark workload for LeetCode #327 — Rust mirror of count_range_sum.kara.

const LEN: i64 = 100000;
const PUNCHES: i64 = 20;
const MODULUS: i64 = 1073741789;

fn count_and_sort(p: &mut Vec<i64>, tmp: &mut Vec<i64>, lo: usize, hi: usize, lower: i64, upper: i64) -> i64 {
    if hi - lo <= 1 {
        return 0;
    }
    let mid = lo + (hi - lo) / 2;
    let mut count = count_and_sort(p, tmp, lo, mid, lower, upper) + count_and_sort(p, tmp, mid, hi, lower, upper);

    let mut start = mid;
    let mut end = mid;
    for a in lo..mid {
        while start < hi && p[start] < p[a] + lower {
            start += 1;
        }
        while end < hi && p[end] <= p[a] + upper {
            end += 1;
        }
        count += (end - start) as i64;
    }

    let mut i = lo;
    let mut j = mid;
    let mut k = lo;
    while i < mid && j < hi {
        if p[i] <= p[j] {
            tmp[k] = p[i];
            i += 1;
        } else {
            tmp[k] = p[j];
            j += 1;
        }
        k += 1;
    }
    while i < mid {
        tmp[k] = p[i];
        i += 1;
        k += 1;
    }
    while j < hi {
        tmp[k] = p[j];
        j += 1;
        k += 1;
    }
    for t in lo..hi {
        p[t] = tmp[t];
    }
    count
}

fn count_range_sum(nums: &[i64], lower: i64, upper: i64) -> i64 {
    let mut p: Vec<i64> = Vec::new();
    p.push(0);
    let mut s = 0;
    for &x in nums {
        s += x;
        p.push(s);
    }
    let mut tmp: Vec<i64> = Vec::new();
    for _ in 0..p.len() {
        tmp.push(0);
    }
    let n = p.len();
    count_and_sort(&mut p, &mut tmp, 0, n, lower, upper)
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 327;
    let mut a: Vec<i64> = Vec::new();
    for _ in 0..LEN {
        a.push(next(&mut seed) % 2001 - 1000);
    }
    let mut sink = 0;
    for _ in 0..PUNCHES {
        let pos = (next(&mut seed) * 32768 + next(&mut seed)) % LEN;
        a[pos as usize] = next(&mut seed) % 2001 - 1000;
        let w = next(&mut seed) % 1000;
        let count = count_range_sum(&a, -w, w);
        sink = (sink * 31 + count % MODULUS) % MODULUS;
    }
    println!("sink {}", sink);
}
