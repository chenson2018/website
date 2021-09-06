echo "SELECT * FROM website.emails" | 
	mysql --user=$website_mysql_username --password=$website_mysql_password | 
	tail -n +2 | 
	sed 's/\t/,/g'
