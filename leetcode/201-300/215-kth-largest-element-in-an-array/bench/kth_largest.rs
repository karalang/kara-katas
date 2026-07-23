fn partition(a: &mut [i64], lo: i64, hi: i64) -> i64 {
    let pivot = a[hi as usize];
    let mut i = lo;
    let mut j = lo;
    while j < hi {
        if a[j as usize] < pivot {
            a.swap(i as usize, j as usize);
            i += 1;
        }
        j += 1;
    }
    a.swap(i as usize, hi as usize);
    i
}

fn quickselect(a: &mut [i64], lo: i64, hi: i64, target: i64) -> i64 {
    if lo == hi { return a[lo as usize]; }
    let p = partition(a, lo, hi);
    if p == target { return a[p as usize]; }
    if target < p { return quickselect(a, lo, p - 1, target); }
    quickselect(a, p + 1, hi, target)
}

fn main() {
    let n: i64 = 120000;
    let passes: i64 = 420;
    let k: i64 = 40000;
    let target = n - k;

    let mut a: Vec<i64> = vec![0; n as usize];
    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _ in 0..passes {
        for i in 0..n {
            state = (state * 1103515245 + 12345) & 2147483647;
            a[i as usize] = state;
        }
        sink += quickselect(&mut a, 0, n - 1, target);
    }
    println!("{}", sink);
}
