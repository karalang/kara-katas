// Benchmark for #443: mirror of compress.kara (reading and writing in
// place) on 1,000 random strings of 2,000 characters, built once, copied
// and compressed 20 times over.

fn compress(chars: &mut Vec<char>) -> usize {
    let n = chars.len();
    let mut read = 0;
    let mut write = 0;
    while read < n {
        let c = chars[read];
        let start = read;
        while read < n && chars[read] == c {
            read += 1;
        }
        chars[write] = c;
        write += 1;
        let count = read - start;
        if count > 1 {
            for digit in count.to_string().chars() {
                chars[write] = digit;
                write += 1;
            }
        }
    }
    write
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let size = 2000;
    let rounds = 20;
    let mut seed: i64 = 443;
    // Runs of 1 to 1, 3, 15 or 120 letters from a three-letter alphabet.
    let mut strings: Vec<Vec<char>> = Vec::new();
    for _ in 0..count {
        let longest = [1, 3, 15, 120][(next_random(&mut seed) % 4) as usize];
        let mut chars: Vec<char> = Vec::new();
        while chars.len() < size {
            let c = (b'a' + (next_random(&mut seed) % 3) as u8) as char;
            let run = 1 + next_random(&mut seed) % longest;
            for _ in 0..run {
                if chars.len() < size {
                    chars.push(c);
                }
            }
        }
        strings.push(chars);
    }
    let mut length = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for i in 0..count {
            let mut chars = strings[i].clone();
            let n = compress(&mut chars);
            length += n;
            checksum = (checksum * 31 + n as i64 + chars[n - 1] as i64 + round) % 1000000007;
        }
    }
    println!(
        "{} rounds on {} strings of {}: compressed length {}, checksum {}",
        rounds, count, size, length, checksum
    );
}
