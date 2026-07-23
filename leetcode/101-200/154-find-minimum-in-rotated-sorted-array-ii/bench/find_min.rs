fn find_min(nums: &[i64], n: i64) -> i64 {
    let mut lo: i64 = 0;
    let mut hi: i64 = n - 1;
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if nums[mid as usize] > nums[hi as usize] {
            lo = mid + 1;
        } else if nums[mid as usize] < nums[hi as usize] {
            hi = mid;
        } else {
            hi = hi - 1;
        }
    }
    nums[lo as usize]
}

fn main() {
    let n: i64 = 2000;
    let punches: i64 = 75000;

    let mut arr = vec![0i64; n as usize];

    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _pn in 0..punches {
        state = (state * 1103515245 + 12345) & 2147483647;
        let start = state % 1000000;
        state = (state * 1103515245 + 12345) & 2147483647;
        let rot = state % n;

        let mut cur = start;
        for k in 0..n {
            state = (state * 1103515245 + 12345) & 2147483647;
            let inc = if state % 5 == 0 { (state / 5) % 4 } else { 0 };
            cur += inc;
            arr[((k + rot) % n) as usize] = cur;
        }

        sink += find_min(&arr, n);
    }
    println!("{}", sink);
}
