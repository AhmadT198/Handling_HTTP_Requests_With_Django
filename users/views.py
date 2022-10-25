from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json
from .forms import *
from .models import Student
from django.core import serializers
from django.views import View


class SingleStudent(View):
    '''
    Class for handling HTTP Requests for the endpoint 'localhost:8000/api/<int:id>
    '''

    def get(self, request, *args, **kwargs):
        '''
        Handling GET Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns the data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['id']  ## ID from URL

        try:
            data = Student.objects.filter(studentID=id)  ## Reading Student DATA
            ## Making the output in the form of a JSON object
            data = serializers.serialize('json', data)
            data = json.loads(data)
            data[0]['fields']['studentID'] = data[0]['pk']
            data[0] = data[0]['fields']
        except Exception as e:
            data = {"message": "Not Found"}

        return JsonResponse(data, safe=False);

    def put(elf, request, *args, **kwargs):
        '''
                Handling PUT Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns the Updated data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['id']

        try:
            data = json.loads(request.body)
            form = StudentForm(data=data, instance=Student.objects.get(studentID=id))
            if form.is_valid():
                form.save()
                return JsonResponse(form.data);
            return JsonResponse(form.errors, status=422)

        except Exception as e:
            print(type(e))
            if str(e.__class__.__name__) == "JSONDecodeError":
                data = {"message": "Invalid Input.", 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=422);

            elif str(e.__class__.__name__) == "DoesNotExist":
                data = {"message": "Not Found.", 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=404);
            else:
                data = {"message": str(e), 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=500);

    def delete(elf, request, *args, **kwargs):
        '''
                Handling DELETE Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns Message in the form of a JSON Object {"message" : Msg} , Msg contains the string "Deleted" if it succeeded or contains the Error body.
        '''
        id = kwargs['id']
        Msg = ""

        try:
            Student.objects.get(studentID=id).delete()
        except Exception as e:
            Msg = str(e)
        else:
            Msg = "Deleted"

        return JsonResponse({"message": Msg});


class MultipleStudents(View):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/'
    '''

    def get(self, request):
        '''
            Handling GET Requests for the endpoint 'localhost:8000/api/' to Read Data from the database 'student'
        :param request:
        :return: Returns The Required Data in the form of a JSON Object
        '''

        ## Read and Put data in the form of a JSON Object
        data = Student.objects.all()
        data = serializers.serialize('json', data)
        data = json.loads(str(data));

        for student in range(len(data)):
            data[student]['fields']['studentID'] = data[student]['pk']
            data[student] = data[student]['fields']

        return JsonResponse(data, safe=False);

    def post(self, request):
        '''
                    Handling POST Requests for the endpoint 'localhost:8000/api/' and Adding sent data to the database 'student'
        :param request:
        :return: Returns the newly added Data in the form of a JSON Object
        '''

        try:
            data = json.loads(request.body)
            output = []
            if isinstance(data, list):  ## if the sent data is a list :
                for singleStudent in data:
                    form = StudentForm(singleStudent)
                    if form.is_valid():
                        form.save()
                        output.append(form.data)
                    else:
                        output.append(form.errors)
            else:  ##if it is a single JSON Object
                form = StudentForm(data)
                if form.is_valid():
                    form.save()
                    output = data
                else:
                    output = form.errors

            return JsonResponse(json.loads(json.dumps(output)), safe=False)
        except Exception as e:
            return JsonResponse({"message": "Invalid Error."}, status=500)


class SingleParent(View):
    '''
    Class for handling HTTP Requests for the endpoint 'localhost:8000/api/<int:id>
    '''

    def get(self, request, *args, **kwargs):
        '''
        Handling GET Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns the data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['id']  ## ID from URL

        try:
            data = Parent.objects.filter(parentID=id)  ## Reading Student DATA
            ## Making the output in the form of a JSON object
            data = serializers.serialize('json', data)
            data = json.loads(data)
            data[0]['fields']['parentID'] = data[0]['pk']
            data[0] = data[0]['fields']
        except Exception as e:
            data = {"message": "Not Found"}

        return JsonResponse(data, safe=False);

    def put(self, request, *args, **kwargs):
        '''
                Handling PUT Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns the Updated data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['id']

        try:
            data = json.loads(request.body)

            form = ParentForm(data=data, instance=Parent.objects.get(parentID=id))
            if form.is_valid():
                form.save()
                return JsonResponse(form.data);
            return JsonResponse(form.errors, status=422)

        except Exception as e:
            if str(e.__class__.__name__) == "JSONDecodeError":
                data = {"message": "Invalid Input.", 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=422);
            elif str(e.__class__.__name__) == "DoesNotExist":
                data = {"message": "Not Found.", 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=404);
            else:
                data = {"message": str(e), 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=500);

    def delete(elf, request, *args, **kwargs):
        '''
                Handling DELETE Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns Message in the form of a JSON Object {"message" : Msg} , Msg contains the string "Deleted" if it succeeded or contains the Error body.
        '''

        id = kwargs['id']
        Msg = ""

        try:
            Parent.objects.get(parentID=id).delete()
        except Exception as e:
            Msg = str(e)
        else:
            Msg = "Deleted"

        return JsonResponse({"message": Msg});


class MultipleParents(View):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/'
    '''

    def get(self, request):
        '''
            Handling GET Requests for the endpoint 'localhost:8000/api/' to Read Data from the database 'student'
        :param request:
        :return: Returns The Required Data in the form of a JSON Object
        '''

        ## Read and Put data in the form of a JSON Object
        data = Parent.objects.all()
        data = serializers.serialize('json', data)
        data = json.loads(str(data));

        for parent in range(len(data)):
            data[parent]['fields']['parentID'] = data[parent]['pk']
            data[parent] = data[parent]['fields']

        return JsonResponse(data, safe=False);

    def post(self, request):
        '''
                    Handling POST Requests for the endpoint 'localhost:8000/api/' and Adding sent data to the database 'student'
        :param request:
        :return: Returns the newly added Data in the form of a JSON Object
        '''

        try:
            data = json.loads(request.body)
            output = []
            if isinstance(data, list):  ## if the sent data is a list :
                for singleParent in data:
                    form = ParentForm(singleParent)
                    if form.is_valid():
                        form.save()
                        output.append(form.data)
                    else:
                        output.append(form.errors)
            else:  ##if it is a single JSON Object
                form = ParentForm(data)
                if form.is_valid():
                    form.save()
                    output = data
                else:
                    output = form.errors

            return JsonResponse(json.loads(json.dumps(output)), safe=False)
        except Exception as e:
            return JsonResponse({"message": "Invalid Error."}, status=500)


class MultipleSubjects(View):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/school/subjects'
    '''

    def get(self, request):
        '''
            Handling GET Requests for the endpoint ''localhost:8000/school/subjects' to Read Multiple Records from the database 'subject'
        :param request:
        :return: Returns The Required Data in the form of a JSON Object
        '''

        ## Read and Put data in the form of a JSON Object
        data = Subject.objects.all()
        data = serializers.serialize('json', data)
        data = json.loads(str(data));


        ## Prepare the form of the output
        output = []
        for subject in data:
            subject['fields']['subjectID'] = subject['pk']
            output.append(subject['fields'])

        return JsonResponse(json.loads(json.dumps(output)), safe=False);

    def post(self, request):
        '''
                    Handling POST Requests for the endpoint 'localhost:8000/school/subjects' and Adding sent data to the database 'subjects'
        :param request:
        :return: Returns the newly added Data in the form of a JSON Object
        '''

        try:
            data = json.loads(request.body)

            output = []
            if isinstance(data, list):  ## if the sent data is a list :
                for singleSubject in data: ## For each subject append its corresponding data or Error if any.
                    form = SubjectForm(singleSubject)
                    if form.is_valid():
                        form.save()
                        output.append(form.data)
                    else:
                        output.append(form.errors)
            else:  ##if it is a single JSON Object
                form = SubjectForm(data)
                if form.is_valid():
                    form.save()
                    output = data
                else:
                    output = form.errors

            return JsonResponse(json.loads(json.dumps(output)), safe=False)
        except Exception as e:
            return JsonResponse({"message": "Invalid Input."}, status=422)


class SingleSubject(View):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/school/subjects/<int:id>'
    '''

    def get(self, request, *args, **kwargs):
        '''
            Gets the Data of a specified subject, or says it doesnt exist.
        :param request:
        :param args:
        :param kwargs:
        :return: Returns a JSON object with the Required Data.
        '''
        id = kwargs['id']  ## ID from URL

        try:
            data = Subject.objects.filter(subjectID=id)  ## Reading subject DATA

            ## Making the output in the form of a JSON object
            data = serializers.serialize('json', data)
            data = json.loads(data)
            data[0]['fields']['subjectID'] = data[0]['pk']
            data[0] = data[0]['fields']

        except Exception as e: ## Return "Not Found"
            data = {"message": "Not Found"}

        return JsonResponse(data, safe=False);

    def put(self, request, *args, **kwargs):
        '''
                    Handling POST Requests for the endpoint 'localhost:8000/school/subjects/<int:id>' and Adding sent data to the database 'subject'
        :param request:
        :return: Returns the newly added Data in the form of a JSON Object
        '''

        id = kwargs['id']

        try:
            data = json.loads(request.body)
            output = []
            if isinstance(data, dict):  ## if the sent data is a single element (dict) :

                form = SubjectForm(data, instance=Subject.objects.get(subjectID=id)) ## Update
                if form.is_valid():
                    form.save()
                    output = data
                else:
                    output = form.errors
            else:  ## Return an Error message.
                return JsonResponse({"message": "Invalid Input."}, status=422)

            return JsonResponse(json.loads(json.dumps(output)), safe=False)
        except Exception as e: ## Handling Various Errors
            if str(e.__class__.__name__) == "JSONDecodeError":
                data = {"message": "Invalid Input.", 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=422);
            elif str(e.__class__.__name__) == "DoesNotExist":
                data = {"message": "Not Found.", 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=404);
            else:
                data = {"message": str(e), 'type': str(e.__class__.__name__)}
                return JsonResponse(data, status=500);

    def delete(elf, request, *args, **kwargs):
        '''
                Handling DELETE Requests for the endpoint 'localhost:8000/school/subjects/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns Message in the form of a JSON Object {"message" : Msg} , Msg contains the string "Deleted" if it succeeded or contains the Error body.
        '''

        id = kwargs['id']
        Msg = ""

        try: ## Try to delete, and update the message accordingly
            Subject.objects.get(subjectID=id).delete()
        except Exception as e:
            Msg = str(e)
        else:
            Msg = "Deleted"

        return JsonResponse({"message": Msg});


class ModifySubjects(View):
    '''
        A Class to Check, Add, or Delete the relationship between a specific Subject and a specific Student
    '''

    def get(self, request, *args, **kwargs):
        '''
            Returns whether the student has this subject or not.
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ## Extracting IDs
        studID = kwargs['studentID']
        subID = kwargs['subjectID']


        Msg = {}
        try:
            ## Get the desired Records from the tables
            stud = Student.objects.get(studentID=studID)
            sub = Subject.objects.get(subjectID=subID)

            ## If the student has the subject, Return a Message. Else, Return another message
            if sub in stud.subjects.all():
                Msg = {"message": f"Student {stud} has the subject {sub}", "code": 200}
            else:
                Msg = {"message": f"Student {stud} doesnt have the subject {sub}", "code": 204}


        except Exception as e: ## Return the error message and type, incase an error occurs
            Msg = {"type": str(e.__class__.__name__), "message": str(e), 'code': 500}

        return JsonResponse(Msg, status=Msg['code']);

    def post(self, request, *args, **kwargs):
        '''
            Creates a Relationship between the given Student and the given Subject.

        :param request:
        :param args:
        :param kwargs:
        :return: Returns a JSON Objecst with a message that indicates whether the subject already exists, was added successfully or an Error occured.
        '''

        ## Extracting IDs
        studID = kwargs['studentID'];
        subID = kwargs['subjectID']

        Msg = {}
        try:

            ## GEtting the desired records
            stud = Student.objects.get(studentID=studID)
            sub = Subject.objects.get(subjectID=subID)

            ## If the subject already exists, return a message indicating that.
            if sub in stud.subjects.all():
                Msg = {"message": f"Student {stud} already has the subject {sub}", "code": 200}
            else: ## Else, Add the subject and return a suitable message
                stud.subjects.add(sub)
                Msg = {"message": f"the subject {sub} has been add successfully to the Student {stud}.", "code": 204}

        except Exception as e: ## Return the error message and exception type, incase an error occurs
            Msg = {"type": str(e.__class__.__name__), "message": str(e), 'code': 500}

        return JsonResponse(Msg, status=Msg['code']);

    def delete(self, request, *args, **kwargs):
        '''
            Deletes the Relationship between the given Student and the given Subject if it exists.
        :param request:
        :param args:
        :param kwargs:
        :return: Returns a JSON object with a message that indicate whether the subject was deleted or if there is no such relationship.
        '''


        ## Extracting IDs
        studID = kwargs['studentID'];
        subID = kwargs['subjectID']


        Msg = {}
        try:

            ## Getting desired records
            stud = Student.objects.get(studentID=studID)
            sub = Subject.objects.get(subjectID=subID)

            ## If the subject exists, Delete it and return a suitable message.
            if sub in stud.subjects.all():
                stud.subjects.remove(sub)
                Msg = {"message": f"Deleted Successfully !", "code": 200}
            else: ## If the relationship does not exist, Return a suitable message.
                Msg = {"message": f"the Student {stud} does not have the subject {sub}.", "code": 204}

        except Exception as e: ## Return the error message and exception type, incase an error occurs
            Msg = {"type": str(e.__class__.__name__), "message": str(e), 'code': 500}

        return JsonResponse(Msg, status=Msg['code']);
