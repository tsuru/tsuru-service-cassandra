 # tsuru-service-cassandra

Cassandra service API for tsuru PaaS.

## HOW TO

### Install Cassandra Server


Install Java 1.6

```bash
sudo apt-get install python-software-properties -qqy --force-yes
sudo echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
sudo echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update -qqy --force-yes
sudo apt-get install -qqy oracle-java6-installer --force-yes
sudo apt-get install -qqy oracle-java6-set-default --force-yes
```

install Cassandra

```bash
echo "deb http://debian.datastax.com/community stable main" | sudo tee /etc/apt/sources.list.d/cassandra.sources.list > /dev/null
echo "deb http://some.debian.mirror/debian/ precise main contrib non-free" | sudo tee /etc/apt/source.list > /dev/null

sudo apt-get install curl --force-yes -qqy
curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -
sudo apt-get update --force-yes
sudo apt-get install python-cql --force-yes -qqy
sudo apt-get install dsc1.1 cassandra=1.1.9 --force-yes -qqy
```

### Running this API

Before running the API you must export ther enviroment variables:

 - `TSURU_CASSANDRA_SERVER`
 - `TSURU_CASSANDRA_PORT`





