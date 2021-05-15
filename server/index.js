// server/index.js

const express = require("express");
const path = require('path');

const PORT = process.env.PORT || 3001;
const amqp = require("amqplib/callback_api");


const app = express();

// Have Node serve the files for our built React app
app.use(express.static(path.resolve(__dirname, '../client/build')));

// Handle GET requests to /api route
app.get("/api", (req, res) => {
    res.json({ message: "Hello from server!" });
});


app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});

app.get("/tpa", callPythonApi);
function callPythonApi(req, res) {
    const input = [];

    amqp.connect("amqp://localhost", function (error0, conn) {
        if (error0) {
            throw error0;
        }

        conn.createChannel(function (error1, ch) {
            if (error1) {
                throw error1;
            }

            const simulations = "simulations";
            ch.assertQueue(simulations, { durable: false });

            ch.sendToQueue(simulations, Buffer.from(JSON.stringify(input)));

            const results = "results";
            ch.assertQueue(results, { durable: false });
            ch.consume(results, function (msg) {
                res.send(msg.content.toString())
            }, { noAck: true });
        });

        setTimeout(function () { conn.close(); }, 500);
    });
}

// All other GET requests not handled before will return our React app
app.get('*', (req, res) => {
    res.sendFile(path.resolve(__dirname, '../client/build', 'index.html'));
});