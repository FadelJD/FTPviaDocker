FROM ubuntu:latest

RUN apt-get update && \
		apt-get install -y --no-install-recommends vsftpd db-util && \
		apt-get clean


ENV FTP_USER_ADMIN admin
ENV FTP_PASS_ADMIN admin
ENV FTP_USER_CLIENT1 client1
ENV FTP_PASS_CLIENT1 client1
ENV FTP_USER_CLIENT2 client2
ENV FTP_PASS_CLIENT2 client2

ENV PASV_ADDRESS REQUIRED

COPY ftp/vsftpd.conf /etc/vsftpd/
COPY ftp/vsftpd_virtual /etc/pam.d/
COPY ftp/run-vsftpd.sh /usr/sbin/

RUN chmod +x /usr/sbin/run-vsftpd.sh && \
		mkdir -p /var/run/vsftpd/empty

VOLUME /home/vsftpd
VOLUME /var/log/vsftpd

EXPOSE 20 21

CMD ["/usr/sbin/run-vsftpd.sh"]
