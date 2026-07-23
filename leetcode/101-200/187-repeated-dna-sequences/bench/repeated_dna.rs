fn scan(bases: &[i64], stamp: &mut [i64], cnt: &mut [i64], n: i64, pass: i64) -> i64 {
    let mask: i64 = 1048575; // 2^20 - 1
    let mut hash: i64 = 0;
    let mut dups: i64 = 0;
    let mut i: i64 = 0;
    while i < n {
        hash = ((hash << 2) | bases[i as usize]) & mask;
        if i >= 9 {
            let key = hash as usize;
            if stamp[key] != pass {
                stamp[key] = pass;
                cnt[key] = 0;
            }
            let c = cnt[key] + 1;
            cnt[key] = c;
            if c == 2 {
                dups += 1;
            }
        }
        i += 1;
    }
    dups
}

fn main() {
    let n: i64 = 1000000;
    let passes: i64 = 30;
    let tablesize: i64 = 1048576; // 2^20

    let mut bases: Vec<i64> = Vec::with_capacity(n as usize);
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        bases.push((state >> 16) % 4);
    }

    let mut stamp: Vec<i64> = vec![-1; tablesize as usize];
    let mut cnt: Vec<i64> = vec![0; tablesize as usize];

    let mut sink: i64 = 0;
    for p in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (state % n) as usize;
        bases[idx] = (state >> 16) % 4;
        sink += scan(&bases, &mut stamp, &mut cnt, n, p);
    }
    println!("{}", sink);
}
