const express = require("express");
const app = express();
const PORT = 5000;

// URL del servidor de Grafana en local o en la nube
const GRAFANA_URL = "http://localhost:3000"; // Cambia esto si Grafana está en otro servidor

// ID del dashboard que quieres mostrar
const DASHBOARD_ID = "eebda0sp3tgjkb"; // Sustituye con el UID real del dashboar

// Genera la URL embebida del dashboard
const grafanaDashboardURL = `${GRAFANA_URL}/d/${DASHBOARD_ID}?kiosk`;

app.get("/", (req, res) => {
    res.send(`
        <html>
        <head>
            <title>Grafana Dashboard</title>
        </head>
        <body style="text-align:center;">
            <h1>Dashboard de Grafana</h1>
            <iframe src="${grafanaDashboardURL}" width="100%" height="800px" frameborder="0"></iframe>
        </body>
        </html>
    `);
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
