#!/bin/bash

# Create home dir and update vsftpd user db:
mkdir -p /home/vsftpd/${FTP_USER_ADMIN}
mkdir -p /home/vsftpd/${FTP_USER_CLIENT1}
mkdir -p /home/vsftpd/${FTP_USER_CLIENT2}
chown -R ftp:ftp /home/vsftpd
echo -e "${FTP_USER_ADMIN}\n${FTP_PASS_ADMIN}\n${FTP_USER_CLIENT1}\n${FTP_PASS_CLIENT1}\n${FTP_USER_CLIENT2}\n${FTP_PASS_CLIENT2}" > /etc/vsftpd/virtual_users.txt
db_load -T -t hash -f /etc/vsftpd/virtual_users.txt /etc/vsftpd/virtual_users.db

# Set passive mode parameters:
if [ "$PASV_ADDRESS" = "REQUIRED" ]; then
	echo "Please insert IPv4 address of your host"
	exit 1
fi
echo "pasv_address=${PASV_ADDRESS}" >> /etc/vsftpd/vsftpd.conf

# Run vsftpd:
vsftpd /etc/vsftpd/vsftpd.conf
