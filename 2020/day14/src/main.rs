use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    source: String,
    input: Vec<String>,
    result_a: i64,
    result_b: i64,
}

impl AOCProcessor {
    pub fn new(source: String) -> AOCProcessor {
        AOCProcessor {
            source,
            input: Vec::new(),
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();

        let _ = match File::open(&self.source) {
            Ok(file) => {
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..]);
                    }
                }
            }
            Err(error) => return Err(error),
        };

        self.finalize();

        Ok(())
    }

    pub fn initialize(&mut self) {}

    pub fn finalize(&mut self) {
        self.finalize_a();
        self.finalize_b();
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            self.input.push(String::from(line));
        }
    }

    fn finalize_a(&mut self) {
        let mut and_mask: u64 = 0; // mask for forcing 0
        let mut or_mask: u64 = 0; // mask for forcing 1
        let mut memory: HashMap<u64, u64> = HashMap::new();
        for line in self.input.iter() {
            let tokens: Vec<&str> = line.split_ascii_whitespace().collect();
            if tokens[0].eq("mask") {
                and_mask = 0; // mask for forcing 0
                or_mask = 0; // mask for forcing 1
                let new_mask: Vec<char> = tokens[2].chars().collect();
                for bit in 0..36 {
                    match new_mask[new_mask.len() - 1 - bit as usize] {
                        '0' => {
                            and_mask |= 0 << bit;
                            or_mask |= 0 << bit;
                        }
                        '1' => {
                            and_mask |= 1 << bit;
                            or_mask |= 1 << bit;
                        }
                        'X' => {
                            and_mask |= 1 << bit;
                            or_mask |= 0 << bit;
                        }
                        _ => {}
                    }
                }
                if AOCDEBUG {
                    println!("new_mask:{:?}", tokens[2]);
                    println!("and_mask:\"{:036b}\"", and_mask);
                    println!("or_mask: \"{:036b}\"", or_mask);
                }
            } else {
                let address = &tokens[0][4..tokens[0].len() - 1].parse::<u64>().unwrap();
                let mut value = tokens[2].parse::<u64>().unwrap();
                value = value | or_mask;
                value = value & and_mask;
                if AOCDEBUG {
                    println!("{} -> {}", address, value);
                }
                memory.insert(*address, value);
            }
        }
        let mut total = 0;
        for (_, v) in memory.iter() {
            total += v;
        }
        self.result_a = total as i64;
        println!("result_a:{}", self.result_a);
    }

    fn finalize_b(&mut self) {
        let mut memory: HashMap<u64, u64> = HashMap::new();

        let mut input_mask: Vec<char> = "000000000000000000000000000000000000".chars().collect();
        for line in self.input.iter() {
            let tokens: Vec<&str> = line.split_ascii_whitespace().collect();
            if tokens[0].eq("mask") {
                input_mask = tokens[2].chars().collect();
                let s: String = input_mask.iter().collect();
                if AOCDEBUG {
                    println!("new input mask:{}", s);
                }
        } else {
                let mut address = tokens[0][4..tokens[0].len() - 1].parse::<u64>().unwrap();
                let mut mask_string: Vec<char> = "000000000000000000000000000000000000".chars().collect();
                let mut mask_vec: Vec<u64> = Vec::new();
                if AOCDEBUG {
                    println!(" input address:{:036b}", address);
                }
                let value = tokens[2].parse::<u64>().unwrap();
                for bit in 0..36 {
                    match input_mask[36 - bit - 1] {
                        '1' => {
                            address |= 1<<bit;
                        },
                        'X' => {
                            address &= !(1<<bit);
                            mask_vec.push(bit as u64);
                            mask_string[36 - bit - 1] = 'X';
                        },
                        _ => {}
                    }
                }
                let s : String = mask_string.iter().collect();
                if AOCDEBUG {
                    println!("          mask:{}", s);
                    println!("masked address:{:036b}", address);
                    println!("{:?}", mask_vec);
                }
                for i in 0..(2 as u64).pow(mask_vec.len() as u32) {
                    let mut mask_v: u64 = 0;
                    for j in 0..mask_vec.len() {
                        if i & 1<<j > 0 {
                            mask_v |= 1<<mask_vec[j];
                        }

                    }
                    if AOCDEBUG {
                        println!(" iterated mask:{:036b}", mask_v);
                    }
                    memory.insert(address | mask_v, value);
                }

            }
    
        }
        let mut total = 0;
        for (_, v) in memory.iter() {
            total += v;
        }
        self.result_b = total as i64;
        println!("result_b:{}", self.result_b);
    }
}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
