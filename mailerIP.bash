
#!/bin/sh

ip=$(hostname -I)

echo "$ip" | mail -s "RPi IP Address" t.acox1@yahoo.com

