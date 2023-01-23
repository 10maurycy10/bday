# Birthday tracker

I can never remember when someones birthday is, so I made a script to keep track of it and warn me when it aproches.

To use it, first populate the database (this is stored in the current directory) using the ``add`` subcommand.

```
python3 ./bday.py add test 0001-01-01
```

Now you can list out birthdays:

```
python3 ./bday.py ls
```

You can also show aproching birthdays, this has no output normaly, so you can put it in your .bashrc (make sure to pushd and popd):

```
python3 ./bday.py soon
```

Finaly, you can use the ``del`` command to remove a person, using the id shown ``ls`` output.

