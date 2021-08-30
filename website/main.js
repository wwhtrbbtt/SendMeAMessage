const fastify = require('fastify')({ logger: true })
const path = require('path')

let connections = []
fastify.register(require('fastify-websocket'))
fastify.register(require('fastify-static'), {
    root: path.join(__dirname, 'public'),
    prefix: '/public/', // optional: default '/'
  })

// Declare a route
fastify.get('/', async (request, reply) => {
  return reply.sendFile('index.html')
})
fastify.post('/send', async(request, reply) => {
    const body = request.body 

    console.log(`New message!\n Text: ${body.text}\n Mood: ${body.mood}`)
    // console.log(connections)
    connections.forEach(conn => {
        conn.socket.send(JSON.stringify(body))
    })
    return {"success": true}
})
fastify.get('/socket', { websocket: true }, (connection /* SocketStream */, req /* FastifyRequest */) => {
    connections.push(connection)
  })
// Run the server!
const start = async () => {
  try {
    await fastify.listen(1000)
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()