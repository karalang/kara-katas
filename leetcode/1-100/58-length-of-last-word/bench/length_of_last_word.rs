fn last_word_len(buf: &[i64], end: i64) -> i64 {
    let mut i = end;
    while i >= 0 && buf[i as usize] == 32 {
        i -= 1;
    }
    let mut len = 0i64;
    while i >= 0 && buf[i as usize] != 32 {
        len += 1;
        i -= 1;
    }
    len
}

fn main() {
    let n: i64 = 4000000;
    let passes: i64 = 6500000;

    let mut buf: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let r = state >> 16;
        if r % 100 < 18 {
            buf.push(32);
        } else {
            buf.push(65 + r % 26);
        }
    }

    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p * 97 + 13) % n) as usize;
        if buf[idx] == 32 {
            buf[idx] = 65 + p % 26;
        } else {
            buf[idx] = 32;
        }
        let e = (p * 89 + 41) % n;
        sink += last_word_len(&buf, e);
    }
    println!("{}", sink);
}
