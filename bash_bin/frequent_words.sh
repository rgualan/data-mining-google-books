

name=$1

tr -c '[:alnum:]' '[\n*]' < $name | sort | uniq -c | sort -nr | head  -20
