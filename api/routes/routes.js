const batchClient = require('azure-batch')


let appRouter = function (app) {
    app.get("/", function(req, res) {
      res.status(200).send("Status ok!");
    });

    app.post('/batch', (req, res) => {
        console.log(req.body)
        res.status(200).json({status: 'ok', data:'Batch job added!'})
    })
}

  
  module.exports = appRouter;