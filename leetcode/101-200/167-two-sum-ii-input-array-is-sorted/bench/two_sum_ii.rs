fn two_sum(arr: &[i64], target: i64) -> (i64, i64) {
    let mut lo = 0i64;
    let mut hi = arr.len() as i64 - 1;
    while lo < hi {
        let sum = arr[lo as usize] + arr[hi as usize];
        if sum == target {
            return (lo + 1, hi + 1);
        }
        if sum < target {
            lo += 1;
        } else {
            hi -= 1;
        }
    }
    (-1, -1) // unreachable — a solution is guaranteed
}

fn main() {
    let n: i64 = 20000;
    let passes: i64 = 20000;
    let mut arr = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    let mut val: i64 = 0;
    for c in 0..n as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        val += 1 + (state % 3);
        arr[c] = val;
    }
    let mut sink: i64 = 0;
    for _p in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let a = state % n;
        state = (state * 1103515245 + 12345) & 2147483647;
        let mut b = state % n;
        if a == b {
            b = (a + 1) % n;
        }
        let target = arr[a as usize] + arr[b as usize];
        let (lo, hi) = two_sum(&arr, target);
        sink += lo + hi;
    }
    println!("{}", sink);
}
