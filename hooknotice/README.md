# This is a simple example of how to use loguru in your flask application

Just create a new InterceptHandler and add it to your app. 
Different settings should be configured in your config file, so that it is easy to change settings.

Logging is then as easy as:

`from loguru import logger`

`logger.info("I am logging from loguru!")`

