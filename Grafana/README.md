# Grafana Local Setup

## 1. Installing Grafana

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install grafana -y
```

### Windows
1. Download the installer from: [https://grafana.com/grafana/download](https://grafana.com/grafana/download)
2. Run the installer and follow the instructions.

## 2. Start and Enable the Grafana Service

```bash
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

Check the service status:
```bash
sudo systemctl status grafana-server
```

## 3. Accessing Grafana

Open your browser and go to:  
[http://localhost:3000](http://localhost:3000)

Default credentials:
- Username: `admin`
- Password: `admin` (you will be prompted to change it).

## 4. Configuring the Grafana Enterprise License (Optional)

If you are using Grafana Enterprise, place your `license.jwt` file in:
```bash
sudo cp /path/to/license.jwt /var/lib/grafana/license.jwt
sudo chown grafana:grafana /var/lib/grafana/license.jwt
sudo chmod 600 /var/lib/grafana/license.jwt
```

Restart Grafana to apply the changes:
```bash
sudo systemctl restart grafana-server
```

Check the license status:
```bash
sudo journalctl -u grafana-server --no-pager | grep "Enterprise license"
```

## 5. Running Grafana with Docker

To run Grafana using Docker, follow these steps:

1. Ensure your Grafana configuration files are in the correct local directories:
   - `./etc/grafana` (configuration files)
   - `./var/lib/grafana` (data storage)

2. Build the Docker image:
   ```bash
   sudo docker build -t my-grafana .
   ```

3. Run the Grafana container:
   ```bash
   sudo docker run -d -p 3000:3000 my-grafana
   ```

4. Access Grafana at [http://localhost:3000](http://localhost:3000)

## 6. (Optional) Installing Plugins or Data Sources

If you need additional plugins:
```bash
sudo grafana-cli plugins install grafana-mongodb-datasource
```

Then, restart Grafana:
```bash
sudo systemctl restart grafana-server
```

## 7. Troubleshooting

### "license token file not found"
Ensure that `license.jwt` is correctly located in `/var/lib/grafana/` with the correct permissions.

### Cannot access Grafana in the browser
1. Check if Grafana is running:
   ```bash
   sudo systemctl status grafana-server
   ```
2. Make sure port 3000 is open:
   ```bash
   sudo netstat -tulnp | grep 3000
   ```

## Configuring grafana.ini

It is usually located at:
```
/etc/grafana/grafana.ini
```

1. Edit the configuration file:
```bash
sudo nano /etc/grafana/grafana.ini
```
2. Find these lines under the `[security]` section:
```
;allow_embedding = true
```
3. Remove the `;` at the beginning to enable them:
```
[security]
allow_embedding = true
```

Save the changes and restart Grafana:
```bash
sudo systemctl restart grafana-server
```

## Additional Scripts and Their Functions

### `tesgrafanadashboards.js`
This script sets up an Express server that embeds a specific Grafana dashboard in a web page.
- Runs a web server on port `5000`.
- Generates an embedded Grafana dashboard URL.
- Displays the dashboard inside an `<iframe>`.

### `testMongo.js`
This script interacts with MongoDB to update documents using a machine learning model.
- Connects to a MongoDB database.
- Fetches and updates documents with inferred values.
- Runs a Python script (`tokenizer.py`) for text embedding.
- Adds new participants from a JSON file if they don’t exist in the database.

### `tokenizer.py`
This script uses the `sentence-transformers` model to generate embeddings for text inputs.
- Loads a pre-trained model.
- Tokenizes input text and extracts embeddings.
- Outputs results as JSON for further processing.

## Dependency Files

### `requirements.txt`
This file lists the Python dependencies required to run `tokenizer.py`.
- `torch`: Required for running the deep learning model.
- `transformers`: Provides the pre-trained `sentence-transformers` model.

To install dependencies, run:
```bash
pip install -r requirements.txt
```

### `dependencies.txt`
This file lists the Node.js dependencies needed for `tesgrafanadashboards.js` and `testMongo.js`.
- `express`: Used to create the web server for embedding Grafana dashboards.
- `mongodb`: Required to connect and interact with the MongoDB database.

To install dependencies, run:
```bash
npm install express mongodb
```

## Grafana is now running locally

For more configurations, check the [official documentation](https://grafana.com/docs/).

