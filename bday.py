#!/bin/python3
"""
Track birthdays
"""
import sqlite3
import uuid
import datetime
import os
import sys

PATH=os.path.join(os.path.expanduser('~'),".local/share/bday.sqlite")

def print_table(headers, data):
    # Compute column widths
    width = [len(header) for header in headers];
    for row in data:
        assert(len(headers) == len(row)) # All the rows in data should be the same width as the headers
        for (i, point) in enumerate(row):
            width[i] = max(width[i], len(point))

    # Row seperator
    seperator = '+' + "+".join(["-"*(colwidth+2) for colwidth in width]) + "+"
   
    # Format and print header
    line = []
    for (colidx, col) in enumerate(headers):
        line.append(col.ljust(width[colidx]))
    print(seperator)
    print("| " + " | ".join(line) + " |");
    
    # Format and print data
    print(seperator)
    for row in data:
        line = []
        for (colidx, col) in enumerate(row):
            line.append(col.ljust(width[colidx]))
        print("| " + " | ".join(line) + " |");
        print(seperator)

def initalize(db):
    dbc = db.cursor()
    dbc.execute("create table if not exists names (uuid varchar(255), name text);");
    dbc.execute("create index if not exists uuid on names (uuid);");
    dbc.execute("create index if not exists name on names (name);");
    dbc.execute("create table if not exists bday (uuid varchar(255), year int, month int, day int);");
    dbc.execute("create index if not exists uuid on bday (uuid);");
    db.commit()

def deinit(db):
    dbc = db.cursor()
    dbc.execute("drop table names");
    dbc.execute("drop table bday");
    db.commit()

def add(name, bday, db):
    ident = str(uuid.uuid4());
    time = datetime.datetime.strptime(bday, '%Y-%m-%d')
    dbc = db.cursor()
    dbc.execute("insert into names (uuid, name) values (?,?)", (ident, name));
    dbc.execute("insert into bday (uuid, year, month, day) values (?,?,?,?)", (ident, time.year, time.month, time.day));
    db.commit()
    print(f"Added entry for {name} on {bday}. (uuid: {ident})");

def rm(uuid, db):
    dbc = db.cursor()
    dbc.execute("delete from names where uuid=?", (uuid,));
    dbc.execute("delete from bday where uuid=?", (uuid,));
    db.commit()

def ls(db):
    dbc = db.cursor()
    dbc.execute("select names.name,names.uuid,bday.year,bday.month,bday.day from names join bday on bday.uuid = names.uuid");
    formated = []
    for (name, uuid, y, m, d) in dbc:
        today = datetime.date.today()
        bday = datetime.date(today.year,m,d)
        # Compute year of next bday
        year_of_next_bday = 0
        if bday >= today:
            year_of_next_bday = today.year
        else:
            year_of_next_bday = today.year + 1

        age = today.year - y
        if today.day != d or today.month != m:
            age = age + 1
        daysto = (datetime.date(year_of_next_bday,m,d) - today).days
        date = datetime.date(y,m,d).isoformat()
        formated.append([uuid, name, date, str(daysto), str(age)])
    print_table(["ID", "Name", "Date", "Days to birthday", "Age next bday"], formated);

def soon(db):
    dbc = db.cursor()
    dbc.execute("select names.name,names.uuid,bday.year,bday.month,bday.day from names join bday on bday.uuid = names.uuid");
    formated = []
    for (name, uuid, y, m, d) in dbc:
        today = datetime.date.today()
        bday = datetime.date(today.year,m,d)
        # Compute year of next bday
        year_of_next_bday = 0
        if bday >= today:
            year_of_next_bday = today.year
        else:
            year_of_next_bday = today.year + 1

        age = today.year - y
        if today.day != d or today.month != m:
            age = age + 1
        daysto = (datetime.date(year_of_next_bday,m,d) - today).days
        date = datetime.date(y,m,d).isoformat()

        if daysto < 5:
            print(f"{name} has a birthday on {date} in {daysto} days, turning {age}")

def help(name):
    print(f"Usage: {name} [subcommands]")
    print("SUBCOMMANDS:")
    print("\tadd [name] [bday] : Add a person to the database, date should be in iso format")
    print("\tdel [uuid] : remove from database, by id")
    print("\tls : List out all pepole in database")
    print("\tsoon: Shows birthdays closer that 5 days in the future")
    print('\thelp : Show usage information')
    

db = sqlite3.connect(PATH)
initalize(db)

import sys
args = sys.argv[1:]
if len(args) == 0:
    args = ['help']
while len(args) > 0:
    match args[0]:
        case "add":
            name = args[1]
            bday = args[2]
            args = args[3:]
            add(name, bday, db)
        case "del":
            ident = args[1]
            args = args[2:]
            rm(ident, db)
        case "help":
            args = args[1:]
            help(sys.argv[0])
        case "ls":
            args = args[1:]
            ls(db)
        case "soon":
            args = args[1:]
            soon(db)
        case a:
            args = args[1:]
            print(f"unknown subcommand {a}");
            help(sys.argv[0])
