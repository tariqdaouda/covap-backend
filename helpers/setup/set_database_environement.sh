echo "usage: url username password"

url=$1
username=$2
password=$3
export WEPITOPES_ARANGODB_URL=$url
export WEPITOPES_ARANGODB_USERNAME=$username
export WEPITOPES_ARANGODB_PASSWORD=$password
