from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json

from task4.settings import BASE_DIR

filePath = str(BASE_DIR) + '/users/data.json'

## Open File for reading
d = open(filePath)
data = (d.read())

fullData = json.loads(data);  ## The full contents of the file
data = json.loads(data)["userData"];  ##The Desired List of userData we need to Alter


def writeInFile(updated_data):
    ## Function for Writing the updated data in the File

    fullData["userData"] = updated_data
    with open(filePath, 'w') as w:
        w.write(json.dumps(fullData))


def POST_GET(request):
    '''
        Function that Deals with POST and GET Requests
    :param request: Takes the sent Request
    :return: Returns a Json Response
    '''

    ## For Get Requests, Simply Return the data as a Json Response
    if request.method == 'GET':
        return JsonResponse(data, safe=False)


    ## For Post Requests,
    elif request.method == 'POST':

        post = json.loads(request.body)  ## Take the new Data from the request body

        if isinstance(post, list):  ## if the input data is a list of multiple users,
            for key in post:
                data.append(key)
        else:  ## if its a single user
            data.append(post)

        writeInFile(data)  ##Save in data.json

        return JsonResponse(json.loads(request.body), safe=False)  ## Return the added data

    return JsonResponse({"code": 300, "message": "Invalid Request."},
                        safe=False)  ## If it's not a POST or a GET Request, Return an Error Message


def Update_Delete(request, id):
    '''
        Function to deal with PUT and DELETE Requests
    :param request: Takes the sent Request
    :param id: Takes the id from the URL
    :return: Returns a JsonResponse
    '''

    index = -1;  ## Index for the element to be deleted or updated

    ## For PUT Requests,
    if request.method == 'PUT':
        put = json.loads(request.body)  ## Take the new data

        for i in range(len(data)):  ##Search for an element with the same ID

            if (data[i]["id"] == id):  ##IF FOUND, UPDATE IT
                data[i] = put
                index = i
                writeInFile(data) ## Update data.json
                break

        ## If the operation was done, Return the Updated data else return an Error Message
        if index != -1:
            return JsonResponse(data[index], safe=False)
        else:
            return JsonResponse({"code": 404, "message": "User Not Found"},
                                safe=False)  ## If it's not a POST or a GET Request, Return an Error Message


    ## For Delete Requests,
    elif request.method == 'DELETE':

        for i in range(len(data)): ## Search for the first element with the same ID

            if (data[i]["id"] == id):
                index = i
                del data[i] ## Delete it
                writeInFile(data) ## Update data.json
                break


        if index != -1:
            return JsonResponse({"code": 200, "message": "Deleted."},
                                safe=False)
        else:
            return JsonResponse({"code": 404, "message": "User Not Found."},
                                safe=False)

    return JsonResponse({"code": 300, "message": "Invalid Request."},
                                safe=False)
