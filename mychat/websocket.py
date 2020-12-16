async def websocket_application(scope, recieve, send):
  while True:
    event = await recieve()

    if event['type'] == 'websocket.connect':
      await send({
        'type': 'websocket.accept'
      })

    if event['type'] == 'websocket.disconnect':
      break

    if event['type'] == 'websocket.recieve':
      message = event['message']
      await send({
        'type': 'websocket.send',
        'text': message
      })