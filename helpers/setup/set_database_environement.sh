echo "usage: url username password"

url=$1
username=$2
password=$3
contacts=$4
export WEPITOPES_ARANGODB_URL=$url
export WEPITOPES_ARANGODB_USERNAME=$username
export WEPITOPES_ARANGODB_PASSWORD=$password
export WEPITOPES_CONTACTS_DATABASE=$contacts
