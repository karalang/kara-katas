fn missing_ranges(arr: &[i64], start: i64, len: i64, lower: i64, upper: i64) -> (i64, i64) {
    let mut count = 0i64;
    let mut checksum = 0i64;
    let mut prev = lower - 1;
    let mut i = 0i64;
    while i <= len {
        let cur = if i < len { arr[(start + i) as usize] } else { upper + 1 };
        if cur - prev >= 2 {
            count += 1;
            checksum += (prev + 1) + (cur - 1);
        }
        prev = cur;
        i += 1;
    }
    (count, checksum)
}

fn main() {
    let n: i64 = 1000000;
    let window: i64 = 2000;
    let passes: i64 = 120000;
    let mut arr = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    let mut val: i64 = 0;
    for c in 0..n as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        val += 1 + (state % 3);
        arr[c] = val;
    }
    let span = n - window;
    let mut sink: i64 = 0;
    for p in 0..passes {
        let start = (p * 7919) % span;
        let lower = arr[start as usize];
        let upper = arr[(start + window - 1) as usize] + (p % 5);
        let (count, checksum) = missing_ranges(&arr, start, window, lower, upper);
        sink += count + checksum;
    }
    println!("{}", sink);
}
