docker build . -t moori
docker run -d -p 5000:5000 moori
# docker save moori -o bot.tar
# scp bot.tar root@45.149.77.203:/home/sepehr