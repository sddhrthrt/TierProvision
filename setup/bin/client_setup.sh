#!/bin/bash
set -e # we dont want the script to continue running if some command fails. 

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -S|--setup)
    SETUP="true"
    shift # past argument
    ;;
    -c|--as-client)
    NOMAD_ROLE="client"
    shift
    ;;
    -s|--as-server)
    NOMAD_ROLE="server"
    shift
    ;;
    -r|--role)
    NOMAD_ROLE="$2"
    shift
    shift
    ;;
    -h|--help)
    HELP="true"
    shift
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo "Try $0 --help for help."
if [ "$HELP" == "true" ]
then
  cat <<EOL

Usage:
$0 -S                 - runs setup script to set up an empty Ubuntu 16.04 with docker and nomad.
$0 [-r client | -c]   - starts a nomad client
$0 [-r server | -s]   - starts a nomad server
EOL
exit 2
fi

if [ "$SETUP" == "true" ]
then
  # From https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#os-requirements
  # Uninstalling old docker versions if any
  sudo apt-get remove docker docker-engine docker.io
  sudo apt-get -y install \
      apt-transport-https \
      ca-certificates \
      curl \
      software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo apt-key fingerprint 0EBFCD88
  sudo add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
  sudo apt-get update
  sudo apt-get install -y docker-ce
  sudo service docker start
  # so user can run docker commands withouts sudo
  sudo usermod -a -G docker thota

  # install nomad
  sudo apt install -y unzip
  curl -fsSL https://releases.hashicorp.com/nomad/0.7.0/nomad_0.7.0_linux_amd64.zip > nomad.zip
  unzip -e nomad.zip
  sudo mv nomad /usr/bin/
fi

# setup as server/client
if [ -z $NOMAD_ROLE ]
then
  echo "Please set \$NOMAD_ROLE to either client or server (or use -c, -s or -r options)"
  exit 1
elif [ "$NOMAD_ROLE" == "client" ]
then
  nomad agent -config client.hcl
elif [ "$NOMAD_ROLE" == "server" ]
then
  nomad agent -config server.hcl
fi
