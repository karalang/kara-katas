// LeetCode #2125: Number of Laser Beams in a Bank -- the benchmark, the
// same algorithm as beams.kara.

fn number_of_beams(bank: &[String]) -> i64 {
    let mut prev = 0;
    let mut beams = 0;
    for row in bank.iter() {
        let devices = row.bytes().filter(|&c| c == b'1').count() as i64;
        if devices > 0 {
            beams += prev * devices;
            prev = devices;
        }
    }
    beams
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2125;
    let mut banks: Vec<Vec<String>> = Vec::new();
    for b in 0..12 {
        let mut bank: Vec<String> = Vec::new();
        for _ in 0..500 {
            let cells: Vec<u8> = (0..500)
                .map(|_| if next_random(&mut seed) % 4 < b % 3 + 1 { b'1' } else { b'0' })
                .collect();
            bank.push(String::from_utf8(cells).unwrap());
        }
        banks.push(bank);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..500i64 {
        for b in 0..12 {
            let r = (next_random(&mut seed) % 500) as usize;
            let c = (next_random(&mut seed) % 500) as usize;
            let mut cells = banks[b][r].as_bytes().to_vec();
            cells[c] = if cells[c] == b'1' { b'0' } else { b'1' };
            banks[b][r] = String::from_utf8(cells).unwrap();
            let beams = number_of_beams(&banks[b]);
            total += beams;
            check = (check * 31 + beams + round) % 1000000007;
        }
    }
    println!("6000 solves: {} beams, checksum {}", total, check);
}
