// Benchmark harness for LeetCode #260 — Single Number III.
// Mirrors single_number_iii.kara algorithm-for-algorithm.

fn two_singles(nums: &Vec<i64>) -> [i64; 2] {
    let mut x: i64 = 0;
    let mut i = 0usize;
    while i < nums.len() {
        x ^= nums[i];
        i += 1;
    }
    let bit = x & (0 - x);

    let mut a: i64 = 0;
    let mut b: i64 = 0;
    let mut j = 0usize;
    while j < nums.len() {
        if (nums[j] & bit) != 0 {
            a ^= nums[j];
        } else {
            b ^= nums[j];
        }
        j += 1;
    }
    if a <= b {
        return [a, b];
    }
    [b, a]
}

fn main() {
    let np: i64 = 4;
    let k: i64 = 100000;
    let iters: i64 = 2600;

    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut p = 0i64;
    while p < np {
        let mut vals: Vec<i64> = Vec::new();
        let mut x = p + 1;
        let mut t = 0i64;
        while t < k {
            x = (x * 1103515245 + 12345) % 2147483648;
            let hi = x / 65536;
            x = (x * 1103515245 + 12345) % 2147483648;
            vals.push((hi * 32768 + x / 65536) % 100000);
            t += 1;
        }
        let mut arr: Vec<i64> = Vec::new();
        let mut pass = 0i64;
        while pass < 2 {
            let mut q = 0usize;
            while q < k as usize {
                arr.push(vals[q]);
                q += 1;
            }
            pass += 1;
        }
        arr.push(999983 + p);
        arr.push(1000003 + p);
        arrays.push(arr);
        p += 1;
    }

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let idx = ((it * 3) % np) as usize;
        let r = two_singles(&arrays[idx]);
        sink = (sink * 31 + r[0] + r[1] * 7) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
