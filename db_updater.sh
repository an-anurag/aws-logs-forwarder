#!/usr/bin/env bash

echo "##########################################"
echo "Welcome to GeoLite2 City database updater"
sleep 2s
DIR="GeoLite2*"
echo "Downloading database..."
URL="https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=OwnUnMrcnORi86z8&suffix=tar.gz"
wget -O "GeoLite2.tar.gz" $URL
sleep 2s
echo "Extracting database..."
tar -xzvf GeoLite2.tar.gz
mv $DIR/GeoLite2-City.mmdb resources/GeoLite2-City.mmdb
rm -r $DIR
sleep 2s
echo "Database installed successfully"
echo "##########################################"