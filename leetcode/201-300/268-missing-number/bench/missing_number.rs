// Benchmark harness for LeetCode #268 — Missing Number.
// Mirrors missing_number.kara algorithm-for-algorithm.

fn missing_number(nums: &Vec<i64>) -> i64 {
    let n = nums.len() as i64;
    let mut acc = n;
    let mut i = 0i64;
    while i < n {
        acc = acc ^ i ^ nums[i as usize];
        i += 1;
    }
    acc
}

fn main() {
    let np: i64 = 4;
    let n: i64 = 1000000;
    let iters: i64 = 850;

    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut p = 0i64;
    while p < np {
        let missing = 200000 * p + 137;

        let mut arr: Vec<i64> = Vec::new();
        let mut z = 0i64;
        while z < n {
            arr.push(0);
            z += 1;
        }
        let mut t = 0i64;
        let mut v = 0i64;
        while t < n {
            if v == missing {
                v += 1;
            }
            let idx = (t * 499979) % n;
            arr[idx as usize] = v;
            v += 1;
            t += 1;
        }
        arrays.push(arr);
        p += 1;
    }

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let idx = ((it * 3) % np) as usize;
        sink = (sink * 31 + missing_number(&arrays[idx])) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
