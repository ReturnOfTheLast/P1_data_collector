if ! command -v docker 2>/dev/null; then
	echo "docker not found, please install"
	exit 1
fi

if ! command -v docker-compose 2>/dev/null; then
	echo "docker-compose not found, please install"
	exit 1
fi

docker build -t data_collector .

docker-compose up -d mongo mongo-express

echo "Setup complete, run 'docker-compose up data_collector' to start the collector"
