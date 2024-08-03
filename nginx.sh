pip install flask gunicorn


server_name=sitename.com
port_number=15067


mkdir -p /var/www/nginx/sites/$server_name/public
mkdir -p /var/www/nginx/sites/$server_name/logs
mkdir -p /var/www/nginx/sites/$server_name/data

chmod 777 /var/www/nginx/sites/$server_name
mkdir -p /var/www/services
chmod 777  /var/www/services

cat > "/var/www/nginx/conf.d/$server_name.conf" <<END
server {
		client_max_body_size 200M;
		listen       80;
		server_name $server_name;
		root         /usr/share/nginx/html;
		error_log /var/www/nginx/log/$server_name-error.log warn;
		access_log  /var/www/nginx/log/$server_name-access.log main;

		# Load configuration files for the default server block.
		include /etc/nginx/default.d/*.conf;

		location / {
			proxy_pass http://127.0.0.1:$port_number;
			proxy_redirect off;
			proxy_set_header Host \$host;
			proxy_set_header X-Real-IP \$remote_addr;
			proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto \$scheme;
		}

		error_page 404 /404.html;
			location = /40x.html {
		}
		error_page 500 502 503 504 /50x.html;
			location = /50x.html {
		}
}
server {
    server_name www.$server_name;
    return 301 \$scheme://$server_name\$request_uri;
}
END


cat > "/var/www/services/$server_name.service"  <<END
[Unit]
Description=$server_name


[Service]
WorkingDirectory=/var/www/nginx/sites/$server_name/public
#ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:$port_number unix:flask_app.sock -m 007 app:app
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:$port_number -m 007 app:app
Restart=always
# Restart service after 10 seconds if the dotnet service crashes:
RestartSec=10
KillSignal=SIGINT
SyslogIdentifier=$server_name
User=root

[Install]
WantedBy=multi-user.target
END




systemctl daemon-reload
systemctl restart nginx
systemctl enable /var/www/services/$server_name.service
service $server_name start
echo "========================================================="
echo "Install nginx done, please upload your code to: /var/www/nginx/sites/$server_name/public"
echo "Service edit it at /var/www/services/$server_name.service"
echo "Domain name $server_name, nginx config at /var/www/nginx/conf.d/$server_name.conf"
echo "Local port number $port_number"
echo "========================================================="