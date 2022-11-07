docker build -t data_collector .
docker-compose up -d mongo mongo-express

echo "Setup complete, run 'docker-compose up data_collector' to start the collector"
