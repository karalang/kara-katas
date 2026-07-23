fn range_and(left: i64, right: i64) -> i64 {
    let mut lo = left;
    let mut hi = right;
    let mut shift = 0i64;
    while lo < hi {
        lo >>= 1;
        hi >>= 1;
        shift += 1;
    }
    lo << shift
}

fn main() {
    let iters: i64 = 20000000;
    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _ in 0..iters {
        state = (state * 1103515245 + 12345) & 2147483647;
        let x = state;
        state = (state * 1103515245 + 12345) & 2147483647;
        let y = state;
        let lo = if x < y { x } else { y };
        let hi = if x < y { y } else { x };
        sink += range_and(lo, hi);
    }
    println!("{}", sink);
}
