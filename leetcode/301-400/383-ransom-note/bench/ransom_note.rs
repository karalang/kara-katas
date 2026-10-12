// Benchmark mirror of ransom_note.kara (#383).

fn can_construct(ransom_note: &str, magazine: &str) -> bool {
    let mut count = [0i64; 26];
    for b in magazine.bytes() {
        count[(b - b'a') as usize] += 1;
    }
    for b in ransom_note.bytes() {
        let k = (b - b'a') as usize;
        count[k] -= 1;
        if count[k] < 0 {
            return false;
        }
    }
    true
}

fn main() {
    let mut seed: i64 = 383;
    let mut pool = String::new();
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push(((seed / 65536) % 26 + 97) as u8 as char);
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for _ in 0..10000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let n = 30000 + (seed / 64) % 40000;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let m = 40000 + (seed / 64) % 40000;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let a = (seed / 64) % (1000000 - n);
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let b = (seed / 64) % (1000000 - m);
        let ok = can_construct(&pool[a as usize..(a + n) as usize], &pool[b as usize..(b + m) as usize]);
        if ok {
            yes += 1;
        }
        checksum = (checksum * 3 + if ok { 1 } else { 2 }) % 1000000007;
    }
    println!("{} of 10000 can be built, checksum {}", yes, checksum);
}
