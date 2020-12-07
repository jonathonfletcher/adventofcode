use std::fs::File;
use std::io::{self, Error, BufRead};

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    input: String,
    sum_part1: i32,
    sum_part2: i32,
    current_entry: Vec<i32>,
    current_nlines: i32,
}

impl AOCProcessor {
    pub fn new(input: String) -> AOCProcessor {
        AOCProcessor {
            input,
            sum_part1: 0,
            sum_part2: 0,
            current_entry: vec![0; 26],
            current_nlines: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        let file = match File::open(&self.input) {
            Ok(file) => file,
            Err(error) => return Err(error)
        };

        self.initialize();
        for line in io::BufReader::new(file).lines() {
            if let Ok(line) = line {
                self.process_line(&line[..]);
            }
        }
        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {
        self.sum_part1 = 0;
        self.sum_part2 = 0;
        self.current_entry = vec![0; 26];
        self.current_nlines = 0;
    }

    fn process_line(&mut self, line: &str) {
        fn char_to_index(c: char) -> i32 {
            c as i32 - 'a' as i32
        }

        if line.len() > 0 {
            self.current_nlines += 1;
            for c in line.chars() {
                let idx = char_to_index(c) as usize;
                self.current_entry[idx] += 1;
            }
        } else {
            let v_p1: i32 = self
                .current_entry
                .iter()
                .map(|i| if *i > 0 { 1 } else { 0 })
                .sum();
            let v_p2: i32 = self
                .current_entry
                .iter()
                .map(|i| if *i == self.current_nlines { 1 } else { 0 })
                .sum();
            self.sum_part1 += v_p1;
            self.sum_part2 += v_p2;
            self.current_entry = vec![0; 26];
            self.current_nlines = 0;
        }
    }

    pub fn finalize(&mut self) {
        if self.current_nlines > 0 {
            let v_p1: i32 = self
                .current_entry
                .iter()
                .map(|i| if *i > 0 { 1 } else { 0 })
                .sum();
            let v_p2: i32 = self
                .current_entry
                .iter()
                .map(|i| if *i == self.current_nlines { 1 } else { 0 })
                .sum();
            self.sum_part1 += v_p1;
            self.sum_part2 += v_p2;
        }
    }
}

fn main() {
    let mut p = AOCProcessor::new(String::from("input.txt"));

    match p.process() {
        Ok(()) => {
            println!("sum_part1={}", p.sum_part1);
            println!("sum_part2={}", p.sum_part2);
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
