// Benchmark mirror of LeetCode #318 — build-once + punch.
//
// Same algorithm as bench/max_product.kara: a flat WORDS x LMAX letter grid,
// 26-bit letter masks rebuilt every pass, and a full pair scan that records
// each word's best disjoint partner. One word is rewritten per pass.

const WORDS: usize = 6000;
const LMAX: usize = 16;
const WINDOW: i64 = 7;
const PASSES: i64 = 15;
const MASKMOD: i64 = 1073741823;

fn next_rand(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn write_word(letters: &mut [i64], lens: &mut [i64], w: usize, seed: &mut i64) {
    let len = next_rand(seed) % LMAX as i64 + 1;
    let base = next_rand(seed) % (26 - WINDOW + 1);
    lens[w] = len;
    for k in 0..len as usize {
        letters[w * LMAX + k] = base + next_rand(seed) % WINDOW;
    }
}

fn build_masks(letters: &[i64], lens: &[i64], masks: &mut [i64]) {
    for w in 0..WORDS {
        let mut m: i64 = 0;
        for k in 0..lens[w] as usize {
            m |= 1i64 << letters[w * LMAX + k];
        }
        masks[w] = m;
    }
}

fn main() {
    let mut seed: i64 = 318318;
    let mut letters = vec![0i64; WORDS * LMAX];
    let mut lens = vec![0i64; WORDS];
    let mut masks = vec![0i64; WORDS];
    let mut best = vec![0i64; WORDS];

    for w in 0..WORDS {
        write_word(&mut letters, &mut lens, w, &mut seed);
    }

    let mut sink: i64 = 0;
    for p in 0..PASSES {
        write_word(&mut letters, &mut lens, (p * 977 % WORDS as i64) as usize, &mut seed);
        build_masks(&letters, &lens, &mut masks);

        for i in 0..WORDS {
            best[i] = 0;
        }
        for i in 0..WORDS {
            let mi = masks[i];
            let li = lens[i];
            for j in (i + 1)..WORDS {
                if mi & masks[j] == 0 {
                    let q = li * lens[j];
                    if q > best[i] {
                        best[i] = q;
                    }
                    if q > best[j] {
                        best[j] = q;
                    }
                }
            }
        }

        let mut total: i64 = 0;
        let mut top: i64 = 0;
        for i in 0..WORDS {
            total += best[i];
            if best[i] > top {
                top = best[i];
            }
        }
        sink = (sink * 31 + total + top) % MASKMOD;
    }

    println!("checksum {}", sink);
}
