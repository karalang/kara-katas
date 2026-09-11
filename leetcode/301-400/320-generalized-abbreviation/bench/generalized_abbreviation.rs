// Benchmark mirror of LeetCode #320 — same mask walk as
// bench/generalized_abbreviation.kara.

const WORD_LEN: i64 = 20;
const PASSES: i64 = 8;
const MODULUS: i64 = 1073741789;

fn main() {
    let mut sink: i64 = 0;
    let mut total_chars: i64 = 0;

    for p in 0..PASSES {
        let mut bs = [0u8; WORD_LEN as usize];
        for i in 0..WORD_LEN {
            bs[i as usize] = ((i * 7 + p * 11) % 26) as u8 + b'a';
        }

        let mut buf = [0u8; (WORD_LEN + 8) as usize];
        let limit: i64 = 1 << WORD_LEN;
        let mut acc: i64 = 0;
        let mut chars: i64 = 0;

        let mut mask: i64 = 0;
        while mask < limit {
            let mut len: usize = 0;
            let mut run: i64 = 0;
            for i in 0..WORD_LEN {
                if mask & (1 << i) != 0 {
                    run += 1;
                } else {
                    if run > 0 {
                        if run >= 10 {
                            buf[len] = (run / 10) as u8 + b'0';
                            len += 1;
                        }
                        buf[len] = (run % 10) as u8 + b'0';
                        len += 1;
                        run = 0;
                    }
                    buf[len] = bs[i as usize];
                    len += 1;
                }
            }
            if run > 0 {
                if run >= 10 {
                    buf[len] = (run / 10) as u8 + b'0';
                    len += 1;
                }
                buf[len] = (run % 10) as u8 + b'0';
                len += 1;
            }

            for j in 0..len {
                acc = (acc * 131 + buf[j] as i64) % MODULUS;
            }
            acc = (acc * 131 + 7) % MODULUS;
            chars += len as i64;
            mask += 1;
        }

        sink = (sink * 1000003 + acc) % MODULUS;
        total_chars += chars;
    }

    println!("sink {} chars {}", sink, total_chars);
}
