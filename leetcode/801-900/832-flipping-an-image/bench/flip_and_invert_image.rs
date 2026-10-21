// Benchmark for #832: Flipping an Image -- the ★ arm (two pointers in place).
//
// Mirrors flip_and_invert_image.kara: each row is flipped and inverted in
// one walk from both ends, the middle cell of an odd row only inverted.
// The image is taken owned and changed in place.

fn flip_and_invert_image(image: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let mut img = image;
    let n = img.len();
    for r in 0..n {
        let mut i = 0;
        let mut j = n - 1;
        while i < j {
            let left = img[r][i];
            img[r][i] = 1 - img[r][j];
            img[r][j] = 1 - left;
            i += 1;
            j -= 1;
        }
        if i == j {
            img[r][i] = 1 - img[r][i];
        }
    }
    img
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64i64;
    let rounds = 4000000i64;
    let mut seed = 832i64;
    let mut images: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..count {
        let n = 17 + g % 4;
        let mut image: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..n {
                row.push(next_random(&mut seed) % 2);
            }
            image.push(row);
        }
        images.push(image);
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for round in 0..rounds {
        let k = (round % count) as usize;
        let image = std::mem::take(&mut images[k]);
        images[k] = flip_and_invert_image(image);
        let row = (round / count) as usize % images[k].len();
        for &x in images[k][row].iter() {
            total += x;
            checksum = (checksum * 3 + x) % 1000000007;
        }
    }
    println!("{} rounds of {} images: {} ones, checksum {}", rounds, count, total, checksum);
}
