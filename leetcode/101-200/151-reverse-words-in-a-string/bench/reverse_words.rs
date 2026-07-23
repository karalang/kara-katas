fn main() {
    let len: i64 = 200000;
    let passes: i64 = 320;
    let modp: i64 = 1000000007;
    let space: i64 = 32;

    let mut buf = vec![0i64; len as usize];
    let mut ws = vec![0i64; len as usize];
    let mut we = vec![0i64; len as usize];
    let mut state: i64 = 12345;
    for i in 0..len as usize {
        state = (state * 1103515245 + 12345) & 2147483647;
        buf[i] = if state % 100 < 15 { space } else { 97 + state % 26 };
    }

    let mut sink: i64 = 0;
    for _p in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let idx = (state % len) as usize;
        state = (state * 1103515245 + 12345) & 2147483647;
        buf[idx] = if state % 100 < 15 { space } else { 97 + state % 26 };

        let mut i: i64 = 0;
        let mut m: i64 = 0;
        while i < len {
            while i < len && buf[i as usize] == space {
                i += 1;
            }
            if i >= len {
                break;
            }
            let start = i;
            while i < len && buf[i as usize] != space {
                i += 1;
            }
            ws[m as usize] = start;
            we[m as usize] = i;
            m += 1;
        }

        let mut k = m - 1;
        while k >= 0 {
            if k < m - 1 {
                sink = (sink * 131 + space) % modp;
            }
            let e = we[k as usize];
            let mut j = ws[k as usize];
            while j < e {
                sink = (sink * 131 + buf[j as usize]) % modp;
                j += 1;
            }
            k -= 1;
        }
    }
    println!("{}", sink);
}
