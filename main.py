#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE =re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return USER_RE.match(username) and username
def valid_password(password):
    return PASSWORD_RE.match(password) and password
def valid_email(email):
    return not email or EMAIL_RE.match(r"^[\S]+@[\S]+.[\S]+$")
errorMessages={'emailError':"",'verifyError':"",'usernameError':"",'passwordError':""}



header = """<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        Signup
    </h1>
"""
def buildForm(usernameError="",passwordError="",verifyError ="",emailError="",user=" ",email=" "):
    form = """  <form method="post">
    <table><tr><td><label for="username">Username</label></td>
    <td>
    <input name="username" type="text" required value="""+user+""">
    <span class="error">""" + usernameError +"""</span>
    </td>
    </tr>
    <tr>
    <td><label for="password">Password</label></td>
    <td>
    <input name="password" type="password" value = ""required>
    <span class="error">"""+passwordError+"""</span>
    </td>
    </tr>
    <tr>
    <td><label for="verify">Verify Password</label></td>
    <td>
    <input name="verify" type="password" vale = ""required>
    <span class="error">""" +verifyError+"""</span>
    </td>
    </tr>
    <tr>
    <td><label for="email">Email (optional)</label></td>
    <td>
    <input name="email" type="email" value="""+email+""">
    <span class="error">"""+emailError+"""</span>
    </td>
    </tr>
    </table>
    <input type="submit">
    </form>"""
    return form


class MainHandler(webapp2.RequestHandler):
    def get(self):
        verifyError =self.request.get("verifyError")
        emailError = self.request.get("emailError")
        passwordError = self.request.get("passwordError")
        usernameError = self.request.get("usernameError")
        user = self.request.get("user")
        email = self.request.get("email")
        self.response.write(header+buildForm(usernameError,passwordError,verifyError,emailError,user,email))

    def post(self):
        errors = False
        email = cgi.escape(self.request.get("email"), quote =True)
        verify = cgi.escape(self.request.get("verify"), quote=True)
        password = cgi.escape(self.request.get("password"),quote=True)
        username = cgi.escape(self.request.get("username"), quote=True)
        verifyError=""
        passwordError=""
        usernameError=""
        emailError=""


        params = dict(username = username,email = email)

        if not valid_username(username):
            usernameError ="Please enter a valid username"
            errors =True
        if not valid_password(password):
            passwordError ="Enter a valid password"
            errors =True
        if not valid_email(email):
            emailError="Email is not valid."
            errors=True
        if not password == verify:
            verifyError="The passwords do not match."
            errors=True
        if errors:
            self.redirect("/?verifyError="+verifyError +"&emailError="+emailError+"&passwordError="+passwordError + "&usernameError="+usernameError
            + "&user="+username+"&email="+email)
        else:
            self.redirect("/Welcome?user="+username)

class Success(webapp2.RequestHandler):
    def get(self):
        if not valid_username(self.request.get("user")):
            self.redirect("/")
        self.response.write("<h1>Welcome, " +self.request.get("user")+"</h1>")



app = webapp2.WSGIApplication([
    ('/', MainHandler),('/Welcome',Success)
], debug=True)
