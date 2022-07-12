#!/bin/sh
## Requires openssl, nodejs, jq
###

https://docs.mia-platform.eu/docs/runtime_suite/client-credentials/jwt_keys

ssh-keygen -f private.key -e -m PKCS8 > public.key

####
header='
{
  "kid": "12345",
  "alg": "RS256"
}'
payload='
{
  "iss": "https://example.com",
  "sub": "user-id-123",
  "aud": "client-app-id-123",
  "exp": 1735689600,
  "iat": 1563980400
}'

function pack() {
  # Remove line breaks and spaces
  echo $1 | sed -e "s/[\r\n]\+//g" | sed -e "s/ //g"
}

if [ ! -f private-key.pem ]; then
  # Private and Public keys
  openssl genrsa 2048 > private-key.pem
  openssl rsa -in private-key.pem -pubout -out public-key.pem
fi

# Base64 Encoding
b64_header=$(pack "$header" | openssl enc -e -A -base64)
b64_payload=$(pack "$payload" | openssl enc -e -A -base64)
signature=$(echo -n $b64_header.$b64_payload | openssl dgst -sha256 -sign private-key.pem | openssl enc -e -A -base64)
# Export JWT 
echo $b64_header.$b64_payload.$signature > jwt.txt
# Create JWK from public key
if [ ! -d ./node_modules/pem-jwk ]; then
  # A tool to convert PEM to JWK
  npm install pem-jwk
fi
jwk=$(./node_modules/.bin/pem-jwk public-key.pem)
# Add additional fields
jwk=$(echo '{"use":"sig"}' $jwk $header | jq -cs add)
# Export JWK
echo '{"keys":['$jwk']}'| jq . > jwks.json

echo "--- JWT ---"
cat jwt.txt
echo -e "\n--- JWK ---"
jq . jwks.json
