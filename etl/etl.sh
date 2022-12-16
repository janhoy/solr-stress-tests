#!/usr/bin/env bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

function usage() {
  cat << EOF
Usage: etl.sh [<options>]
 -f    File to index
 -u    URL of Solr, without /solr suffix, e.g. http://localhost:8983
 -h    This help
EOF
}

COLLECTION=stackexchange
CONFIGSET=stackexchange-config

while getopts "hf:u:" opt; do
  case ${opt} in
    f)
      FILE="$OPTARG"
      ;;
    u)
      SOLR_URL="$OPTARG"
      ;;
    h)
      usage
      exit 0
      ;;
   \?)
      echo "Unknown option $OPTARG"
      usage
      exit 1
   esac
done
shift $((OPTIND -1))

if [[ -z "$FILE" ]]; then
  echo "Lacking -f option, must specify file name."
  usage
  exit 1
fi

if [[ -z "$SOLR_URL" ]]; then
  echo "Lacking -u option, must specify Solr url."
  usage
  exit 1
fi



echo "Solr ETL"

#printf "\n\n"
#echo "Upload config set"
#rm -f configset.zip >/dev/null
#pushd configset
#zip ../configset.zip *
#popd
#curl -X DELETE "$SOLR_URL/api/cluster/configs/${CONFIGSET}?omitHeader=true" >/dev/null
#curl -X PUT --header "Content-Type:application/octet-stream" --data-binary @configset.zip \
#    "$SOLR_URL/api/cluster/configs/${CONFIGSET}?overwrite=true"

printf "\n\n"
echo "Delete old collection"
curl "$SOLR_URL/solr/admin/collections?action=DELETE&name=${COLLECTION}" >/dev/null

printf "\n\n"
echo "Create collection"
curl -X POST "$SOLR_URL/api/collections" -H 'Content-Type: application/json' -d "
{
  \"create\": {
    \"name\": \"$COLLECTION\",
    \"config\": \"$CONFIGSET\",
    \"numShards\": 1,
    \"replicationFactor\": 2
  }
}
"

printf "\n\n"
echo "Index content"
curl -XPOST --header "Content-Type:application/json" "$SOLR_URL/solr/$COLLECTION/update?commit=true&update.chain=script" --data-binary @"$FILE"
