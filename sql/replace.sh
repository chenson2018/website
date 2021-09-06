filename=""
title=""
published=0
date="CURRENT_DATE()"

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -f|--filename)
      filename="'$2'"
      article_file="$(git rev-parse --show-toplevel)/articles/$2.html"
      shift # past argument
      shift # past value
      ;;
    -t|--title)
      title="'$2'"
      shift # past argument
      shift # past value
      ;;
    -d|--date)
      date="'$2'"
      shift # past argument
      shift # past value
      ;;
    -p|--publish)
      published=1
      shift # past argument
      ;;
    --default)
      DEFAULT=YES
      shift # past argument
      ;;
    *)    # unknown option
      echo "Unknown option '$1'"
      exit 1
      ;;
  esac
done


if [ ! -f "$article_file" ]
then
  echo "$article_file not found, exiting..."
  exit 1
fi

if [ -z "$title" ]
then
  echo "Argument title is missing, exiting..."
  exit 1
fi

if [ $published -eq 0 ]
then
    sql="REPLACE INTO website.articles (filename, title) values ($filename, $title);"
else
    sql="REPLACE INTO website.articles (filename, title, published, publish_date) values ($filename, $title,  1, $date);"
fi

echo $sql | mysql --user=$website_mysql_username --password=$website_mysql_password

