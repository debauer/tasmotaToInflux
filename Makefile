init:
	pip3 install -r requirements.txt
run:
	python3 -m tasmotatoinflux
test:
	python3 -m unittest discover -v
build:
	python3 setup.py sdist

init-docker:
	sudo mkdir -p /srv/docker/grafana/data
	sudo chown 472:472 /srv/docker/grafana/data
	sudo mkdir -p /srv/docker/influxdb/data
	sudo systemctl start docker
	sudo docker pull grafana/grafana
	sudo docker pull influxdb
run-docker:
	sudo systemctl start docker
	sudo docker-compose up -d
stop-docker:
	sudo docker-compose stop
cleanup-docker:
	sudo docker-compose rm

cleanup-influx:
	curl -i -XPOST http://localhost:8086/query --data-urlencode "q=DROP database tasmotaToInflux"
	curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE database tasmotaToInflux"