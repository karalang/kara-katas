fn prefix_lps(base: &[i64], w: i64, width: i64, comb: &mut [i64], fail: &mut [i64]) -> i64 {
    let m = 2 * width + 1;
    for i in 0..width { comb[i as usize] = base[(w + i) as usize]; }
    comb[width as usize] = -1;
    for i in 0..width { comb[(width + 1 + i) as usize] = base[(w + width - 1 - i) as usize]; }

    fail[0] = 0;
    let mut len = 0i64;
    let mut idx = 1i64;
    while idx < m {
        if comb[idx as usize] == comb[len as usize] {
            len += 1;
            fail[idx as usize] = len;
            idx += 1;
        } else if len > 0 {
            len = fail[(len - 1) as usize];
        } else {
            fail[idx as usize] = 0;
            idx += 1;
        }
    }
    fail[(m - 1) as usize]
}

fn main() {
    let big: i64 = 260000;
    let width: i64 = 512;
    let alpha: i64 = 2;

    let mut base: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..big {
        state = (state * 1103515245 + 12345) & 2147483647;
        base.push(state % alpha);
    }

    let m = 2 * width + 1;
    let mut comb: Vec<i64> = vec![0; m as usize];
    let mut fail: Vec<i64> = vec![0; m as usize];

    let windows = big - width;
    let mut sink: i64 = 0;
    for w in 0..windows {
        sink += prefix_lps(&base, w, width, &mut comb, &mut fail);
    }
    println!("{}", sink);
}
