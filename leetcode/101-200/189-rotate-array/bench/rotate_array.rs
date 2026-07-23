fn reverse_range(a: &mut [i64], lo: i64, hi: i64) {
    let mut i = lo;
    let mut j = hi;
    while i < j {
        a.swap(i as usize, j as usize);
        i += 1;
        j -= 1;
    }
}

fn rotate(a: &mut [i64], k: i64) {
    let n = a.len() as i64;
    if n == 0 {
        return;
    }
    let kk = k % n;
    reverse_range(a, 0, n - 1);
    reverse_range(a, 0, kk - 1);
    reverse_range(a, kk, n - 1);
}

fn checksum(a: &[i64], n: i64) -> i64 {
    let mut chk: i64 = 0;
    let mut i: i64 = 0;
    while i < n {
        chk = ((chk * 131) + a[i as usize]) & 2147483647;
        i += 1;
    }
    chk
}

fn main() {
    let n: i64 = 30000;
    let passes: i64 = 4000;

    let mut a: Vec<i64> = Vec::with_capacity(n as usize);
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        a.push(state);
    }

    let mut sink: i64 = 0;
    for _ in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let k = state % n;
        rotate(&mut a, k);
        sink += checksum(&a, n);
    }
    println!("{}", sink);
}
