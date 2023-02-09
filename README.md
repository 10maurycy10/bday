# Birthday tracker

I can never remember when someones birthday is, so I made a script to keep track of it and warn me when it approaches.
To use it, first populate the database (this is stored in `~/.local/share/bday.sqlite`) using the ``add`` subcommand.

```
python3 ./bday.py add test 0001-01-01
```

Now you can list out birthdays:

```
python3 ./bday.py ls
```

You can also show approaching birthdays, this has no output normally, so you can put it in your `.bashrc`.

```
python3 ./bday.py soon
```

Finally, you can use the ``del`` command to remove a person, using the id shown ``ls`` output.

