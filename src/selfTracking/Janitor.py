
# As the last column of the data contained 'predicted' written text and ";" is writable on the keyboard,
# the datafiles would sometimes contain some rows with too much apparent columns
# this needs to be fixed. Here i replace the separator ";" with a new one chr(164) (it's printable, but not writable).
# This also requires checking each line by hand and editing only lines with too many columns.
def reseparate(file, source_seperator=";", new_seperator=chr(164), encoding="utf-8"):
    data = []
    with open(file, "r", encoding=encoding) as f:
        for line in f:
            line = line.replace("\n", "")  # get rid of '\n'
            row = line.split(source_seperator)  # treat the line as a row
            if len(row) > 13:  # if it contains too many columns
                last_column = source_seperator.join(row[12:])  # then treat each additional column as a single column
                row = row[:12]
                row.append(last_column)
            data.append(row)

    with open(file, "w", encoding=encoding) as f:
        for idx, row in enumerate(data):
            line = new_seperator.join(row)
            if idx != len(data) - 1:  # we don't want the newline symbol on the last line
                line += "\n"
            f.write(line)

if __name__ == "__main__":
    reseparate("2022-10-25.txt")