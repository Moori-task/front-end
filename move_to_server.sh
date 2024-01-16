docker build . -t moori
docker save moori -o bot.tar
scp bot.tar root@45.149.77.203:/home/sepehr