fn revisions(v: &str) -> Vec<i64> {
    let bytes = v.as_bytes();
    let n = bytes.len();
    let mut revs: Vec<i64> = Vec::new();
    let mut i = 0usize;
    while i < n {
        let mut val: i64 = 0;
        while i < n && bytes[i] != b'.' {
            val = val * 10 + (bytes[i] as i64 - b'0' as i64);
            i += 1;
        }
        revs.push(val);
        i += 1; // skip the '.'
    }
    revs
}

fn compare_version(v1: &str, v2: &str) -> i64 {
    let a = revisions(v1);
    let b = revisions(v2);
    let na = a.len();
    let nb = b.len();
    let m = na.max(nb);
    for i in 0..m {
        let x = if i < na { a[i] } else { 0 };
        let y = if i < nb { b[i] } else { 0 };
        if x < y {
            return -1;
        }
        if x > y {
            return 1;
        }
    }
    0
}

fn main() {
    let m: i64 = 4096;
    let passes: i64 = 10000000;
    let mut pool: Vec<String> = Vec::new();
    let mut state: i64 = 12345;
    for _k in 0..m {
        state = (state * 1103515245 + 12345) & 2147483647;
        let r = 1 + (state % 4);
        let mut vs = String::new();
        for t in 0..r {
            state = (state * 1103515245 + 12345) & 2147483647;
            let rev = state % 1000;
            if t > 0 {
                vs.push('.');
            }
            vs.push_str(&rev.to_string());
        }
        pool.push(vs);
    }
    let mut sink: i64 = 0;
    for _p in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let i = (state % m) as usize;
        state = (state * 1103515245 + 12345) & 2147483647;
        let j = (state % m) as usize;
        sink += compare_version(&pool[i], &pool[j]) + 1;
    }
    println!("{}", sink);
}
