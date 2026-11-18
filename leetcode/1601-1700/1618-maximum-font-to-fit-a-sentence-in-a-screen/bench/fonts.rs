// LeetCode #1618: Maximum Font to Fit a Sentence in a Screen -- the bench in
// Rust, mirroring fonts.kara: a binary search for the last size that fits.

trait FontInfo {
    fn get_width(&self, font_size: i32, ch: char) -> i32;
    fn get_height(&self, font_size: i32) -> i32;
}

struct Font {
    base: Vec<i32>,
}

impl FontInfo for Font {
    fn get_width(&self, font_size: i32, ch: char) -> i32 {
        (font_size * self.base[(ch as u32 - 'a' as u32) as usize] + 3) / 4
    }

    fn get_height(&self, font_size: i32) -> i32 {
        font_size + font_size / 4
    }
}

fn fits(text: &str, w: i32, h: i32, size: i32, info: &impl FontInfo) -> bool {
    info.get_height(size) <= h && text.chars().map(|c| info.get_width(size, c) as i64).sum::<i64>() <= w as i64
}

fn max_font(text: &str, w: i32, h: i32, fonts: &[i32], info: &impl FontInfo) -> i32 {
    let (mut lo, mut hi) = (0, fonts.len());
    while lo < hi {
        let mid = (lo + hi) / 2;
        if fits(text, w, h, fonts[mid], info) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    if lo == 0 { -1 } else { fonts[lo - 1] }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1618;
    let texts: Vec<String> = (0..200)
        .map(|_| (0..5000).map(|_| (b'a' + (next_random(&mut seed) % 26) as u8) as char).collect())
        .collect();
    let font = Font { base: (0..26).map(|_| (next_random(&mut seed) % 8 + 1) as i32).collect() };
    let fonts: Vec<i32> = (1..61).map(|k| k * 3).collect();
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for text in &texts {
        for _ in 0..40 {
            let w = (next_random(&mut seed) * 8 + 1) as i32;
            let h = (next_random(&mut seed) % 240 + 1) as i32;
            let answer = max_font(text, w, h, &fonts, &font);
            check = (check * 31 + answer as i64 + 1) % 1000000007;
            total += answer as i64;
        }
    }
    println!("8000 screens of 5000 letters: sizes total {total}, checksum {check}");
}
