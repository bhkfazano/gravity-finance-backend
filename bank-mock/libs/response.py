import json

def success(body):
    return buildResponse(200, body)

  
def failure(body):
	return buildResponse(500, body)


def unauthorized(body):
	return buildResponse(403, body)

def alreadyExists(body):
	return buildResponse(409, body)

def notfound(body):
	return buildResponse(404, body)

def missingData(body):
	return buildResponse(422, body)


def buildResponse(statusCode, body):
	"""
	Builds a response object
	Receive the status code and the body of the response and returns a response object
	"""

	return {
		"statusCode": statusCode,
		"headers": {
			"Access-Control-Allow-Origin": "*",
			"Access-Control-Allow-Credentials": True
		},
		"body": json.dumps(body)
	};
