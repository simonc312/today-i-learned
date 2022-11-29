# CRLF Injection

When an attacker can input special carriage return line ending delimiters to possibly cause HTTP Request Smuggling and HTTP Response Splitting.

HTTP Request Smuggling occurs when an HTTP request is passed through a server which processes it and passes it to another server, like a proxy or firewall.

HTTP Response Splitting allows an attacker to insert HTTP response headers and split the response entirely, creating two separate responses. This is effective because modifying HTTP headers can result in unintended behavior, such as redirecting a user to an malicious website or serving content controlled by attackers.

%0D%0A are particularly significant characters as they can lead to CRLF Injection issues. Sometimes, when an out of date browser is used that does not properly handle special characters, what gets returned as valid may be interpreted as an line delimiter.