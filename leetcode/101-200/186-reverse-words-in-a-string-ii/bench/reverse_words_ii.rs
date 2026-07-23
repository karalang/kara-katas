fn reverse_range(a: &mut [i64], lo: i64, hi: i64) {
    let mut i = lo;
    let mut j = hi;
    while i < j {
        a.swap(i as usize, j as usize);
        i += 1;
        j -= 1;
    }
}

fn reverse_words(a: &mut [i64], n: i64) {
    if n > 0 {
        reverse_range(a, 0, n - 1);
    }
    let mut start = 0i64;
    for i in 0..=n {
        if i == n || a[i as usize] == 32 {
            if i > start {
                reverse_range(a, start, i - 1);
            }
            start = i + 1;
        }
    }
}

fn main() {
    let target_len: i64 = 30000;
    let passes: i64 = 3000;

    let mut buf: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    let mut first = true;
    while (buf.len() as i64) < target_len {
        if first {
            first = false;
        } else {
            buf.push(32);
        }
        state = (state * 1103515245 + 12345) & 2147483647;
        let wlen = 1 + (state % 8);
        for _ in 0..wlen {
            state = (state * 1103515245 + 12345) & 2147483647;
            buf.push(97 + (state % 26));
        }
    }

    let n = buf.len() as i64;
    let modv: i64 = 1000000007;
    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p * 131 + 7) % n) as usize;
        if buf[idx] != 32 {
            buf[idx] = 97 + (((buf[idx] - 97) + 1) % 26);
        }
        reverse_words(&mut buf, n);
        let mut cs: i64 = 0;
        for k in 0..n as usize {
            cs = (cs * 131 + buf[k]) % modv;
        }
        sink += cs;
    }
    println!("{}", sink);
}
