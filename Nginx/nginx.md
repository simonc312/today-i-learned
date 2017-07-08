Nginx 

typically place in /etc/nginx directory as nginx.conf

include conf.d/feature_specific_dir;

#context block could also be
# events – General connection processing
# mail – Mail traffic
# stream – TCP traffic
#
http {
	server {
		#unsecured http 
		listen 80 default_server;
		server_name _;
		root absolute/path/directory;

		location = /exactMatchingPath {
			alias absolute/path/directory/not/requiring/exactMatchingPath; 
		}

		location ~ /regexMatchingPath {
			root absolute/path/directory/plus/regexMatchingPath;
		} 
		return 403 https:$server_name://$request_uri
	}

	server {
		#https ssl port
		listen 443; 
		server_name domain.com;

		ssl                  on;
	    ssl_certificate      /path/to/my/cert;
	    ssl_certificate_key  /path/to/my/key;

	    location / {
	        try_files $uri $uri/ @proxy /index.php;
	    }

	    location @proxy {
	    	#do stuff
	    }

	    location ~ \.php$ {
	        include fastcgi_params;
	        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
	        fastcgi_pass unix:/tmp/phpcgi.socket;
	    }

	}
}

commands

sudo nginx -s signal

The signal value can be one of the following:

quit – Shut down gracefully
reload – Reload the configuration file
reopen – Reopen log files
stop – Shut down immediately (fast shutdown)