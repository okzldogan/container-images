#!/bin/bash

curl -f -X POST -H "Accept: application/vnd.github+json" -H "Authorization: Bearer ${PAT}" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/my-org/${REPO}/actions/runners/registration-token -o /token/tokenfile

echo token response: $?

ACTIONS_RUNNER_INPUT_NAME=$HOSTNAME ; ACTIONS_RUNNER_INPUT_TOKEN=`cat /token/tokenfile | jq -r '.token'` ; /runner/config.sh --url https://github.com/my-org/${REPO} --token $ACTIONS_RUNNER_INPUT_TOKEN --labels $CLUSTER_LABEL --disableupdate --replace --unattended
