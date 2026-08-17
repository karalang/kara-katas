// Benchmark harness for LeetCode #137 — Single Number II.
// Mirrors single_number.kara algorithm-for-algorithm.

fn mask32() -> i64 {
    4294967295
}

fn sign_extend32(v: i64) -> i64 {
    if v >= 2147483648 {
        v - 4294967296
    } else {
        v
    }
}

fn single_ones_twos(nums: &Vec<i64>) -> i64 {
    let mask = mask32();
    let mut ones: i64 = 0;
    let mut twos: i64 = 0;
    let mut i = 0usize;
    while i < nums.len() {
        let x = nums[i] & mask;
        ones = (ones ^ x) & (!twos) & mask;
        twos = (twos ^ x) & (!ones) & mask;
        i += 1;
    }
    sign_extend32(ones)
}

fn single_bitcount(nums: &Vec<i64>) -> i64 {
    let mut res: i64 = 0;
    let mut b = 0i64;
    while b < 32 {
        let mut cnt: i64 = 0;
        let mut i = 0usize;
        while i < nums.len() {
            if ((nums[i] >> b) & 1) == 1 {
                cnt += 1;
            }
            i += 1;
        }
        if (cnt % 3) != 0 {
            res |= 1i64 << b;
        }
        b += 1;
    }
    sign_extend32(res)
}

fn main() {
    let np: i64 = 4;
    let k: i64 = 30000;
    let iters: i64 = 40;

    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut j = 0i64;
    while j < np {
        let mut vals: Vec<i64> = Vec::new();
        let mut x = j + 1;
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
        while pass < 3 {
            let mut q = 0usize;
            while q < k as usize {
                arr.push(vals[q]);
                q += 1;
            }
            pass += 1;
        }
        arr.push(999983 + j);
        arrays.push(arr);
        j += 1;
    }

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let idx = ((it * 3) % np) as usize;
        let a = single_ones_twos(&arrays[idx]);
        let b = single_bitcount(&arrays[idx]);
        if a != b {
            sink += 1000000000;
        }
        sink = (sink + a + b) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
