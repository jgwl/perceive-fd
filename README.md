# fd_crawler_raw.py

#### `create_dir(directory)`

Create dir if not exists.

#### `dl_index(year, month, path)`

Download month's index file.

Args:
* year: str, e.g. "2017"
* month: str, e.g., "Jan"
* path: str

Returns:
str: filename that contents were written into


#### `dl_message(year, month, id, path)`

Download individual message.

Args: 
* year: str, e.g. "2017"
* month: str, e.g., "Jan"
* id: str, e.g., "0"
path: str


#### `dl_month(year, month)`

Download entire raw html contents of month.
Contents will be written to subdir, e.g. ./2017_01

Args: 
* year: int
* month: int (Jan = 1)

#### `dl_range(year_start, month_start, year_end, month_end)`

Download multiple months, using start & end year/months.
See dl_month for contents.

Args:
* year_start: int
* month_start: int (Jan = 1)
* year_end: int
* month_end: int (Jan = 1)

#### `parse_index_num(filename)`

Determine how many messages the index file contains. 
Parses the first line (e.g., <!-- SecLists-Message-Count: 108 -->)

Args: 
* filename: str

Returns:
int

