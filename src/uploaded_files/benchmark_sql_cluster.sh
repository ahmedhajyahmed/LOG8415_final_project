#!/bin/bash

RED='\033[0;31m'
NOCOLOR='\033[0m'

echo -e "${RED}Updating package list...${NOCOLOR}"
sudo apt update
echo -e "${RED}Done.${NOCOLOR}"

echo -e "${RED}Installing Sakila DB...${NOCOLOR}"
echo y |wget -c https://downloads.mysql.com/docs/sakila-db.tar.gz -O - | tar -xz
echo -e "${RED}Done.${NOCOLOR}"

echo -e "${RED}Running queries on Sakila DB...${NOCOLOR}"
sudo /opt/mysqlcluster/home/mysqlc/bin/mysql <<BASH_QUERY
SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;
SOURCE /home/ubuntu/sakila-db/sakila-data.sql;
USE sakila;
SHOW FULL TABLES;
SELECT COUNT(*) FROM film;
SELECT COUNT(*) FROM film_text;
BASH_QUERY
echo -e "${RED}Done.${NOCOLOR}"

echo -e "${RED}Installing Sysbench...${NOCOLOR}"
sudo apt update
echo y | sudo apt-get install sysbench
echo -e "${RED}Done."

echo -e "Benchmarking SQL Cluster...${NOCOLOR}"
sudo sysbench --test=oltp_read_write --table-size=1000000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql-password= --mysql-host=127.0.0.1 prepare
sudo sysbench --test=oltp_read_write --table-size=1000000 --db-driver=mysql --num-threads=6 --max-time=60 --max-requests=0 --mysql-db=sakila --mysql-user=root --mysql-password= --mysql-host=127.0.0.1  run >> results.txt
echo -e "${RED}Done.${NOCOLOR}"