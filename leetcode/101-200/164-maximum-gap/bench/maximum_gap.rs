// LeetCode 164 — Maximum Gap benchmark kernel (Rust mirror, rustc -O).
//
// Build-once + punch: LCG-filled N values, maximum_gap called K times with a
// one-element perturbation each round. Sink = sum of the K gaps. Identical
// algorithm to the Kāra / C / Go / Python mirrors.

fn maximum_gap(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    if n < 2 {
        return 0;
    }
    let mut lo = nums[0];
    let mut hi = nums[0];
    for &x in &nums[1..] {
        if x < lo {
            lo = x;
        }
        if x > hi {
            hi = x;
        }
    }
    if lo == hi {
        return 0;
    }

    let bsize = ((hi - lo) / (n - 1)).max(1);
    let bcount = ((hi - lo) / bsize + 1) as usize;

    let mut used = vec![false; bcount];
    let mut bmin = vec![0i64; bcount];
    let mut bmax = vec![0i64; bcount];

    for &x in nums {
        let idx = ((x - lo) / bsize) as usize;
        if used[idx] {
            if x < bmin[idx] {
                bmin[idx] = x;
            }
            if x > bmax[idx] {
                bmax[idx] = x;
            }
        } else {
            bmin[idx] = x;
            bmax[idx] = x;
            used[idx] = true;
        }
    }

    let mut gap = 0i64;
    let mut prev_max = lo;
    for b in 0..bcount {
        if used[b] {
            if bmin[b] - prev_max > gap {
                gap = bmin[b] - prev_max;
            }
            prev_max = bmax[b];
        }
    }
    gap
}

fn main() {
    let n: i64 = 1_000_000;
    let k: i64 = 30;
    let range: i64 = 1_000_000_000;

    let mut nums = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    for slot in nums.iter_mut() {
        state = (state * 1103515245 + 12345) % 2147483648;
        *slot = state % range;
    }

    let mut sink: i64 = 0;
    for round in 0..k {
        let idx = ((round * 7919) % n) as usize;
        nums[idx] = (nums[idx] + 1 + round) % range;
        sink += maximum_gap(&nums);
    }
    println!("{}", sink);
}
