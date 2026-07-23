fn find_peak(arr: &[i64], lo0: i64, hi0: i64) -> i64 {
    let mut lo = lo0;
    let mut hi = hi0;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if arr[mid as usize] < arr[(mid + 1) as usize] {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    lo
}

fn main() {
    let n: i64 = 4000000;
    let window: i64 = 4096;
    let passes: i64 = 1000000;
    let mut arr = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    for c in 0..n as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        arr[c] = state % 1000003;
    }
    let span = n - window;
    let mut sink: i64 = 0;
    for p in 0..passes {
        let base = (p * 4099) % span;
        let bu = base as usize;
        arr[bu] = (arr[bu] + 1) % 1000003;
        sink += find_peak(&arr, base, base + window - 1);
    }
    println!("{}", sink);
}
