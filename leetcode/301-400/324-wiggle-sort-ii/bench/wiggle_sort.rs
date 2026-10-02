// Benchmark mirror of LeetCode #324 — same select arm as
// bench/wiggle_sort.kara.

const LEN: i64 = 1000000;
const PASSES: i64 = 16;
const STRIDE: i64 = 9973;
const MODULUS: i64 = 1073741789;

fn median3(x: i64, y: i64, z: i64) -> i64 {
    if (x <= y && y <= z) || (z <= y && y <= x) {
        return y;
    }
    if (y <= x && x <= z) || (z <= x && x <= y) {
        return x;
    }
    z
}

fn select(a: &mut [i64], k: i64) -> i64 {
    let mut lo = 0i64;
    let mut hi = a.len() as i64 - 1;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        let pivot = median3(a[lo as usize], a[mid as usize], a[hi as usize]);
        let mut lt = lo;
        let mut i = lo;
        let mut gt = hi;
        while i <= gt {
            if a[i as usize] < pivot {
                a.swap(lt as usize, i as usize);
                lt += 1;
                i += 1;
            } else if a[i as usize] > pivot {
                a.swap(i as usize, gt as usize);
                gt -= 1;
            } else {
                i += 1;
            }
        }
        if k < lt {
            hi = lt - 1;
        } else if k > gt {
            lo = gt + 1;
        } else {
            return pivot;
        }
    }
    a[k as usize]
}

fn wiggle_sort(nums: &mut [i64]) {
    let n = nums.len() as i64;
    let median = select(nums, n / 2);
    let m = n | 1;
    let mut left = 0i64;
    let mut i = 0i64;
    let mut right = n - 1;
    while i <= right {
        let vi = ((1 + 2 * i) % m) as usize;
        if nums[vi] > median {
            nums.swap(((1 + 2 * left) % m) as usize, vi);
            left += 1;
            i += 1;
        } else if nums[vi] < median {
            nums.swap(vi, ((1 + 2 * right) % m) as usize);
            right -= 1;
        } else {
            i += 1;
        }
    }
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64, bound: i64) -> i64 {
    let hi = next(seed);
    let lo = next(seed);
    (hi * 32768 + lo) % bound
}

fn refill(nums: &mut [i64], k: i64, seed: &mut i64) {
    let n = nums.len();
    for i in 0..n {
        if i % 2 == 0 {
            nums[i] = draw(seed, k);
        } else {
            nums[i] = k + draw(seed, k);
        }
    }
    let mut i = n - 1;
    while i > 0 {
        let j = draw(seed, i as i64 + 1) as usize;
        nums.swap(i, j);
        i -= 1;
    }
}

fn violations(a: &[i64]) -> i64 {
    let mut bad = 0;
    for i in 1..a.len() {
        if i % 2 == 1 {
            if a[i] <= a[i - 1] {
                bad += 1;
            }
        } else if a[i] >= a[i - 1] {
            bad += 1;
        }
    }
    bad
}

fn main() {
    let mut seed = 324i64;
    let mut sink = 0i64;
    let mut nums = vec![0i64; LEN as usize];
    let ks = [2i64, 3, 50, 2500];
    let mut bad = 0;
    for p in 0..PASSES {
        refill(&mut nums, ks[(p % 4) as usize], &mut seed);
        wiggle_sort(&mut nums);
        bad = violations(&nums);
        let mut probe = 0i64;
        let mut i = 0i64;
        while i < LEN {
            probe = (probe * 31 + nums[i as usize]) % MODULUS;
            i += STRIDE;
        }
        sink = (sink * 131 + bad * 7 + probe) % MODULUS;
    }
    println!("sink {} violations {}", sink, bad);
}
