fn main() {
    let len: i64 = 600000;
    let w: i64 = 200;
    let a: i64 = 20011;
    let mut s = vec![0i64; len as usize];
    let mut t = vec![0i64; len as usize];
    let mut state: i64 = 12345;
    for i in 0..len as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        s[i] = state % a;
    }
    for i in 0..len as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        t[i] = state % a;
    }

    let mut st_val = vec![0i64; a as usize];
    let mut st_ver = vec![-1i64; a as usize];
    let mut ts_val = vec![0i64; a as usize];
    let mut ts_ver = vec![-1i64; a as usize];

    let mut sink: i64 = 0;
    let last = len - w + 1;
    for start in 0..last {
        let stamp = start;
        let mut iso = true;
        let mut k: i64 = 0;
        while iso && k < w {
            let ch = s[(start + k) as usize];
            let dh = t[(start + k) as usize];
            if st_ver[ch as usize] != stamp {
                st_ver[ch as usize] = stamp;
                st_val[ch as usize] = dh;
            } else if st_val[ch as usize] != dh {
                iso = false;
            }
            if iso {
                if ts_ver[dh as usize] != stamp {
                    ts_ver[dh as usize] = stamp;
                    ts_val[dh as usize] = ch;
                } else if ts_val[dh as usize] != ch {
                    iso = false;
                }
            }
            k += 1;
        }
        if iso {
            sink += 1;
        }
    }
    println!("{}", sink);
}
