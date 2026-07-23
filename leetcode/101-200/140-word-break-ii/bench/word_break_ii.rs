// Exponential-backtracking segmentation COUNT for LeetCode #140 (see
// word_break_ii.kara). Dict SET is a flat stamped base-A table.
const ALPHA: i64 = 3;
const MINLEN: i64 = 1;
const MAXLEN: i64 = 3;
const SLEN: i64 = 16;

fn count(s: &[i64], table: &[bool], base: &[i64], start: i64) -> i64 {
    if start == SLEN {
        return 1;
    }
    let mut total = 0i64;
    let mut code = 0i64;
    let mut end = start + 1;
    while end <= SLEN && end - start <= MAXLEN {
        code = code * ALPHA + s[(end - 1) as usize];
        let ln = end - start;
        if ln >= MINLEN {
            if table[(base[ln as usize] + code) as usize] {
                total += count(s, table, base, end);
            }
        }
        end += 1;
    }
    total
}

fn main() {
    let dwords: i64 = 25;
    let cases: i64 = 80000;

    let mut base: Vec<i64> = vec![0, 0];
    let mut pwr = ALPHA;
    let mut acc = 0i64;
    let mut b = 2i64;
    while b <= MAXLEN {
        acc += pwr;
        base.push(acc);
        pwr *= ALPHA;
        b += 1;
    }
    let tsize = acc + pwr;

    let mut table: Vec<bool> = vec![false; tsize as usize];
    let mut s: Vec<i64> = vec![0; SLEN as usize];

    let mut state: i64 = 12345;
    let mut sink: i64 = 0;

    for _ in 0..cases {
        for z in 0..tsize {
            table[z as usize] = false;
        }
        for i in 0..SLEN {
            state = (state * 1103515245 + 12345) & 2147483647;
            let r = state >> 16;
            s[i as usize] = r % ALPHA;
        }
        for _ in 0..dwords {
            state = (state * 1103515245 + 12345) & 2147483647;
            let rl = state >> 16;
            let span = MAXLEN - MINLEN + 1;
            let wlen = MINLEN + (rl % span);
            let mut code = 0i64;
            for _ in 0..wlen {
                state = (state * 1103515245 + 12345) & 2147483647;
                let rc = state >> 16;
                code = code * ALPHA + (rc % ALPHA);
            }
            table[(base[wlen as usize] + code) as usize] = true;
        }

        sink += count(&s, &table, &base, 0);
    }

    println!("{}", sink);
}
