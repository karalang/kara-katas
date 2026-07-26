// Benchmark harness for LeetCode #274 — H-Index.
// Mirrors h_index.kara algorithm-for-algorithm.
//
// `sort_unstable`, not `sort`: Kara's `Vec[i64].sort()` lowers to the runtime's
// karac_vec_sort_i64_8, which delegates to Rust's `sort_unstable` (pdqsort).
// Using stable `sort` here would compare two different algorithms and hand
// Kara an unearned win. See ../README.md § Benchmarks.

fn h_index(cit: &Vec<i64>) -> i64 {
    let mut v: Vec<i64> = Vec::new();
    let mut i = 0usize;
    while i < cit.len() {
        v.push(cit[i]);
        i += 1;
    }
    v.sort_unstable();
    let n = v.len() as i64;
    let mut j = 0i64;
    while j < n {
        if v[j as usize] >= n - j {
            return n - j;
        }
        j += 1;
    }
    0
}

fn main() {
    let np: i64 = 4;
    let n: i64 = 60000;
    let iters: i64 = 600;

    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut p = 0i64;
    while p < np {
        let mut arr: Vec<i64> = Vec::new();
        let mut x = p + 1;
        let mut t = 0i64;
        while t < n {
            x = (x * 1103515245 + 12345) % 2147483648;
            let r = (x / 65536) % 32768;
            if p == 0 {
                arr.push(r % 30000);
            } else if p == 1 {
                arr.push(r % 40);
            } else if p == 2 {
                arr.push((r % 7) * 3000);
            } else {
                arr.push(t + (r % 5));
            }
            t += 1;
        }
        arrays.push(arr);
        p += 1;
    }

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let idx = ((it * 3) % np) as usize;
        sink = (sink * 31 + h_index(&arrays[idx])) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
