// Build-once + punch word-break; dictionary is a SET realized as a flat stamped
// bool table keyed by a per-length base-A word encoding (see word_break.kara).
fn main() {
    let alpha: i64 = 5;
    let maxlen: i64 = 4;
    let n: i64 = 5000;
    let dwords: i64 = 120;
    let win: i64 = 24;
    let windows: i64 = 2200000;

    let mut base: Vec<i64> = vec![0, 0];
    let mut pwr = alpha;
    let mut acc = 0i64;
    let mut b = 2i64;
    while b <= maxlen {
        acc += pwr;
        base.push(acc);
        pwr *= alpha;
        b += 1;
    }
    let tsize = acc + pwr;

    let mut table: Vec<bool> = vec![false; tsize as usize];

    let mut state: i64 = 12345;

    let mut s: Vec<i64> = Vec::new();
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let r = state >> 16;
        s.push(r % alpha);
    }

    for _ in 0..dwords {
        state = (state * 1103515245 + 12345) & 2147483647;
        let rl = state >> 16;
        let wlen = 2 + (rl % (maxlen - 1));
        let mut code = 0i64;
        for _ in 0..wlen {
            state = (state * 1103515245 + 12345) & 2147483647;
            let rc = state >> 16;
            code = code * alpha + (rc % alpha);
        }
        table[(base[wlen as usize] + code) as usize] = true;
    }

    let mut dp: Vec<bool> = vec![false; (win + 1) as usize];

    let mut sink: i64 = 0;
    for _ in 0..windows {
        state = (state * 1103515245 + 12345) & 2147483647;
        let ro = state >> 16;
        let off = ro % (n - win);

        for z in 0..=win {
            dp[z as usize] = false;
        }
        dp[0] = true;

        let mut ii = 1i64;
        while ii <= win {
            let low = if ii > maxlen { ii - maxlen } else { 0 };
            let mut code = 0i64;
            let mut pw = 1i64;
            let mut ln = 0i64;
            let mut j = ii - 1;
            while j >= low {
                let ch = s[(off + j) as usize];
                code = ch * pw + code;
                pw *= alpha;
                ln += 1;
                if dp[j as usize] {
                    if table[(base[ln as usize] + code) as usize] {
                        dp[ii as usize] = true;
                        break;
                    }
                }
                j -= 1;
            }
            ii += 1;
        }

        if dp[win as usize] {
            sink += off + 1;
        }
    }

    println!("{}", sink);
}
