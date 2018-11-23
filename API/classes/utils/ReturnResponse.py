import time
from rest_framework import serializers


class Response(object):

    def __init__(self, status, module, result, message):
        #  instance variable unique to each instance
        self.pk = 1
        self.status = status
        self.module = module
        self.result = result
        self.message = message
        self.created = time.time()

    def return_json(self):
        res = ReturnResponseSerializer(self).data
        return res


class ReturnResponseSerializer(serializers.Serializer):
    pk = serializers.IntegerField(default=1, required=False)
    status = serializers.CharField(max_length=50)
    module = serializers.CharField(max_length=50)
    result = serializers.CharField(max_length=50)
    message = serializers.CharField(max_length=200)
    created = serializers.CharField()

    class Meta:
        model = Response
        fields = ('status', 'module', 'result', 'message', 'created')
