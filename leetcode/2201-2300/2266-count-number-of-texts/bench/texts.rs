// LeetCode #2266: Count Number of Texts -- Rust mirror of the ★ arm
// (texts.kara): ways[i] adds ways[i - j] for each run of j equal presses
// ending at i, up to 3, or 4 on `7` and `9`. Output is byte-identical to
// texts.kara.

const MOD: i64 = 1000000007;

fn count_texts(pressed_keys: &str) -> i64 {
    let keys = pressed_keys.as_bytes();
    let n = keys.len();
    let mut ways = vec![0i64; n + 1];
    ways[0] = 1;
    for i in 1..n + 1 {
        let key = keys[i - 1];
        let most = if key == b'7' || key == b'9' { 4 } else { 3 };
        let mut j = 1;
        while j <= most && j <= i && keys[i - j] == key {
            ways[i] = (ways[i] + ways[i - j]) % MOD;
            j += 1;
        }
    }
    ways[n]
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2266;
    let mut check = 0;
    for t in 0..40 {
        let keys = ["2", "79", "234", "23456789"][t % 4].as_bytes();
        let mut pressed = String::new();
        for _ in 0..100000 {
            pressed.push(keys[(next_random(&mut seed) % keys.len() as i64) as usize] as char);
        }
        check = (check * 31 + count_texts(&pressed)) % 1000000007;
    }
    println!("40 strings of 10^5: checksum {check}");
}
