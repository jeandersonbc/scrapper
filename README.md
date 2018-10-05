# scrapper
Extract data from HTML pages

## Why this?
I had some disappointing experiences exporting queries to CSV from sites like ACM Digital Library, IEEEXplorer, and so on.
Therefore, I decided to make this simple script that parses the data from those pages and outputs a simple CSV with all a need at the moment.


## In a nutshell...

1. Make a query
2. Save all the HTML pages you want into a directory
3. Adjust the script with the path to the directory containing the pages
4. Run the script
5. Import the CSV on LibreOffice, Google Drive, etc...

I've provided a sample, so you can try running the script in your local machine.
At some point, I might want to convert this to a browser plugin, which is more convenient.

#### Requirements

* Tested with `Python 3` and `lxml`

#### Usage

```
scrapper jeandersonbc
$ ./main.py
Checking html-acm
Extracted 20 entries
Checking html-ieee
Extracted 25 entries
Checking html-google-scholar
Extracted 10 entries
```

After the execution, you should see an `output.csv` in the current directory.

## Contact

If you have any questions, or concerns, feel free open an issue here.
