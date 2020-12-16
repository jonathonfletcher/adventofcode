#[macro_use]
extern crate lazy_static;
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{self, BufRead, Error};

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

#[derive(Debug)]
enum AOCInputPhase {
    Definitions,
    MyTicket,
    OtherTicket,
}

struct AOCProcessor {
    source: String,
    input_phase: AOCInputPhase,
    class_map: HashMap<String, Vec<(u32, u32)>>,
    ticket_scanning_error_rate: u32,
    my_ticket: Vec<u32>,
    my_ticket_classes: Vec<HashSet<String>>,
}

impl AOCProcessor {
    pub fn new(source: String) -> AOCProcessor {
        AOCProcessor {
            source,
            input_phase: AOCInputPhase::Definitions,
            class_map: HashMap::new(),
            ticket_scanning_error_rate: 0,
            my_ticket: Vec::new(),
            my_ticket_classes: Vec::new(),
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

    pub fn initialize(&mut self) {
        self.input_phase = AOCInputPhase::Definitions;
        self.class_map.clear();
        self.ticket_scanning_error_rate = 0;
        self.my_ticket.clear();
        self.my_ticket_classes.clear();
    }

    pub fn finalize(&mut self) {
        fn collapse_ticket_classes(input: &Vec<HashSet<String>>) -> Vec<HashSet<String>> {
            let mut output: Vec<HashSet<String>> = Vec::new();
            let mut found_singles: HashSet<String> = HashSet::new();
            for idx in 0..input.len() {
                if input[idx].len() == 1 {
                    match input[idx].iter().next() {
                        Some(e) => {
                            if found_singles.contains(e) {
                                panic!("REPEAT OF {} in {:?}", e, input);
                            } else {
                                found_singles.insert(String::from(e));
                            }
                        }
                        None => {}
                    }
                }
            }

            if AOCDEBUG {
                println!("found_singles: {:?}", found_singles);
            }

            for idx in 0..input.len() {
                let mut new_val = input[idx].clone();
                if input[idx].len() > 1 {
                    for e in found_singles.iter() {
                        if new_val.contains(e) {
                            new_val.remove(e);
                        }
                    }
                }
                output.push(new_val);
            }
            output
        }

        println!("result_a:{}", self.ticket_scanning_error_rate);
        if AOCDEBUG {
            println!("{:?} - {:?}", self.my_ticket, self.my_ticket_classes);
        }
        loop {
            let previous_state = self.my_ticket_classes.clone();
            self.my_ticket_classes = collapse_ticket_classes(&previous_state);
            if AOCDEBUG {
                println!("{:?} - {:?}", self.my_ticket, self.my_ticket_classes);
            }
            if previous_state == self.my_ticket_classes {
                break;
            }
        }
        if self.my_ticket.len() != self.my_ticket_classes.len() {
            panic!("IMPOSSIBLE COMBINATION OF TICKET AND CLASSES");
        }
        lazy_static! {
            static ref DEPARTURE_RE: Regex = Regex::new(r"^departure").unwrap();
        }
        let mut departure_product: i64 = 1;
        for idx in 0..self.my_ticket_classes.len() {
            match self.my_ticket_classes[idx].iter().next() {
                Some(v) => {
                    if DEPARTURE_RE.is_match(v) {
                        println!("{} - {}", v, self.my_ticket[idx]);
                        departure_product *= self.my_ticket[idx] as i64;
                    }
                }
                None => {}
            }
        }
        println!("result_b:{}", departure_product);
    }

    fn process_definition_line(&mut self, line: &str) {
        lazy_static! {
            static ref DEFINITION_RE: Regex = Regex::new(r"(?:or)?\s(\d+)\-(\d+)").unwrap();
        }
        let mut tokens = line.splitn(2, ':');
        let field_name = tokens.next().unwrap();
        let mut mm_vec: Vec<(u32, u32)> = Vec::new();
        for cap in DEFINITION_RE.captures_iter(tokens.next().unwrap()) {
            let min_c = &cap[1].parse::<u32>().unwrap();
            let max_c = &cap[2].parse::<u32>().unwrap();
            mm_vec.push((*min_c, *max_c));
        }
        if AOCDEBUG {
            println!("{} -> {:?}", field_name, mm_vec);
        }
        self.class_map.insert(String::from(field_name), mm_vec);
    }

    fn process_ticket_line(&mut self, line: &str) {
        fn potential_ticket_classes(
            class_map: &HashMap<String, Vec<(u32, u32)>>,
            ticket: &Vec<u32>,
        ) -> Vec<HashSet<String>> {
            let mut field_classes: Vec<HashSet<String>> = Vec::new();
            for tv in ticket.iter() {
                let mut classes: HashSet<String> = HashSet::new();
                for (fname, franges) in class_map.iter() {
                    for (r_min, r_max) in franges.iter() {
                        if tv >= r_min && tv <= r_max {
                            classes.insert(fname.clone());
                            break;
                        }
                    }
                }
                field_classes.push(classes);
            }
            field_classes
        }

        fn ticket_class_intersections(
            a: &Vec<HashSet<String>>,
            b: &Vec<HashSet<String>>,
        ) -> Vec<HashSet<String>> {
            let mut field_classes: Vec<HashSet<String>> = Vec::new();
            if a.len() == b.len() {
                for idx in 0..a.len() {
                    let mut nh: HashSet<String> = HashSet::new();
                    for v in a[idx].intersection(&b[idx]) {
                        nh.insert(String::from(v));
                    }
                    field_classes.push(nh);
                }
            } else {
                panic!("impossible ticket combination");
            }
            field_classes
        }

        let mut ticket: Vec<u32> = Vec::new();
        for v in line.split(',') {
            ticket.push(v.parse::<u32>().unwrap());
        }

        match self.input_phase {
            AOCInputPhase::MyTicket => {
                if AOCDEBUG {
                    println!("{:?} - {:?}", self.input_phase, ticket);
                }
                self.my_ticket = ticket;
                self.my_ticket_classes = potential_ticket_classes(&self.class_map, &self.my_ticket);
            }
            AOCInputPhase::OtherTicket => {
                let field_classes = potential_ticket_classes(&self.class_map, &ticket);
                let mut ticket_is_good = true;
                for i in 0..ticket.len() {
                    if field_classes[i].len() == 0 {
                        self.ticket_scanning_error_rate += ticket[i];
                        ticket_is_good = false;
                    }
                }

                if ticket_is_good {
                    self.my_ticket_classes =
                        ticket_class_intersections(&self.my_ticket_classes, &field_classes);
                }
            }
            _ => {}
        }
    }

    fn process_line(&mut self, line: &str) {
        if line.len() > 0 {
            if line.eq("your ticket:") {
                self.input_phase = AOCInputPhase::MyTicket;
            } else if line.eq("nearby tickets:") {
                self.input_phase = AOCInputPhase::OtherTicket;
            } else {
                match self.input_phase {
                    AOCInputPhase::Definitions => {
                        self.process_definition_line(line);
                    }
                    AOCInputPhase::MyTicket => {
                        self.process_ticket_line(line);
                    }
                    AOCInputPhase::OtherTicket => {
                        self.process_ticket_line(line);
                    }
                }
            }
        }
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
