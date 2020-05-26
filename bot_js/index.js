
const express     = require('express')
const app         = express()
const port        = process.env.PORT || 80;
//const port      = 3000;
require('dotenv').config();

app.set("view engine", "ejs");
//app.use(express.static(__dirname + "/public"));



app.listen(port, () => {
    console.log(`Josh_Bot_9000 listening on port: ${port}`);
});