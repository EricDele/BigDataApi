#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Imports for general purpose
from collections import defaultdict
import json
import pkg_resources
from packaging import version
from getpass import getpass

# Imports for http requests and Authent
import requests
from requests.auth import HTTPBasicAuth
from requests_kerberos import HTTPKerberosAuth, REQUIRED


class ApiError(Exception):
    """
    Exception for API call.
    """
    def __init__(self, value, cause=None):
        if(cause is None):
            cause = "An error occured in Api class with {}".format(value)
        super(ApiError, self).__init__(cause)
        self.value = value

    def __str__(self):
        return self.value


class Api(object):
    """
    Api Class to be used by other class for calling API
    """

    def __init__(self):
        self._url = ""
        # should be one of GET, PUT, POST, DELETE
        self._methode = ""
        # should be basic or kerberos
        self._authenticationMethode = ""
        self._headers = ""
        self._data = ""

    def setCredentialsBasic(self, user, password):
        self._user = user
        self._password = password
        self._authentication = HTTPBasicAuth(self._user, self._password)

    def setCredentialsKerberos(self, principal):
        if(version.parse(pkg_resources.get_distribution("requests_kerberos").version) >= version.parse("0.9.0")):
            self._authentication = HTTPKerberosAuth(mutual_authentication=REQUIRED, principal=self._principal)
        else:
            self._authentication = HTTPKerberosAuth(mutual_authentication=REQUIRED)
        self._principal = principal

    def setCompleteUrl(self, url, methode, authenticationMethode, headers, data):
        self._url = url
        # should be one of GET, PUT, POST, DELETE
        self._methode = methode.lower()
        # should be basic or kerberos
        self._authenticationMethode = authenticationMethode.upper()
        self._headers = headers
        self._data = data

    def setUrl(self, url):
        self._url = url

    def setMethode(self, methode):
        # should be one of GET, PUT, POST, DELETE
        self._methode = methode.lower()

    def setAuthenticationMethode(self, authenticationMethode):
        # should be basic or kerberos
        self._authenticationMethode = authenticationMethode.upper()

    def setHeaders(self, headers):
        self._headers = headers

    def setData(self, data):
        self._data = data

    def checkReturnCode(self):
        if(self._r.status_code != 200):
            raise ApiError("\nHTTP Error code {}\nReturned after calling {} {} \nAuthentification : {}\nData : \n{}\n".format(self._r.status_code, self._methode, self._url, self._authenticationMethode, json.dumps(self._r.json(), indent=2)))

    def callApi(self):
        if(self._methode not in ["get", "put", "post", "delete"]):
            raise ApiError("Methode for calling API should be one of : GET, PUT, POST or DELETE")
        self._r = getattr(requests, self._methode)(self._url, auth=self._authentication, headers=self._headers, data=self._data, verify=False)
        self.checkReturnCode()

    def __str__(self):
        return "Url : {} {} \nAuthentification : {}\nData in : {}\nResult : \n{}\n".format(self._methode, self._url, self._authenticationMethode, self._data, json.dumps(self._r.json(), indent=2))
