const express = require('express');
const port = process.env.PORT || 8080;
const app = express();
const cors = require("cors");
const corsOptions ={
   origin:'http://127.0.0.1:3000/', 
               
   optionSuccessStatus:200,
}

app.use(cors(corsOptions))


app.use(express.static(__dirname + '/dist/'));


app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "http://127.0.0.1:3000/");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept",
    "GET,PUT,POST,DELETE,PATCH,OPTIONS"
  );
  next();
});  
app.get(/.*/, function (req, res) {
  res.sendFile(__dirname + '/dist/index.html');
  res.setHeader("Access-Control-Allow-Origin", "http://127.0.0.1:3000/");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
})
app.listen(port);
console.log("server started");