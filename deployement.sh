# Mise a jour et Installation dependance logiciels
apt-get update -y  && apt-get upgrade -y 
apt-get install python3 python3-pip python3-psycopg2 software-properties-common figlet curl gpac ffmpeg p7zip-full unzip php php-curl php-xml chromium-browser -y

# Installation de youtube-dl latest
ln -sf /usr/bin/python3 /usr/bin/python ; \
curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl ; \
chmod a+rx /usr/local/bin/youtube-dl ;

# Installation des modules de dependances
pip3 install -r requirements.txt

#Installation du driver du Robot
wget https://chromedriver.storage.googleapis.com/85.0.4183.38/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/
rm chromedriver_linux64.zip


# Mise en place des services
cp services/* /etc/systemd/system/
systemctl start bot
systemctl enable bot


# Generer les dependances pour les certificats
add-apt-repository universe
apt-get update -y ; apt-get install certbot python3-certbot-apache -y
figlet Configuration HTTPS
certbot certonly --apache

# remove depedances not use 
apt-get remove snapd -y