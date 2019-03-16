# Copyright (c) 2019, MD2K Center of Excellence
# - Nasir Ali <nasir.ali08@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import requests
import json

def login_user(url:str, username:str, password:str):
    """
    Send credentials to CC-ApiServer and Authenticate a user

    Args:
        url (str): url of login route of CC-ApiServer
        username (str): username
        password (str): password of the user

    Returns:
        dict: HTTP response.content

    Raises:
        Exception: if authentication fails

    """
    try:
        data = {"username": str(username),"password": str(password)}
        headers = {"Accept": "application/json"}
        response = requests.post(url, json=data, headers=headers)

        return json.loads(response.content)
    except Exception as e:
        raise Exception("Login failed. "+str(e))

def register_stream(url:str, auth_token:str, stream_metadata:str):
    """
    Send stream metadata to CC-ApiServer for registration

    Args:
        url (str): url of stream-registration route of CC-ApiServer
        auth_token (str): auth token of a user
        stream_metadata (dict): metadata of the stream

    Returns:
        dict: HTTP response.content

    Raises:
        Exception: if stream registration fails


    """
    try:
        headers = {"Accept": "application/json", "Authorization": auth_token}
        response = requests.post(url, json=stream_metadata, headers=headers)
        return json.loads(response.content)
    except Exception as e:
        raise Exception("Stream registration failed. "+str(e))

def upload_stream_data(base_url:str, username:str, password:str, stream_metadata:dict, data_file_path:str):
    """
    Upload stream data to cerebralcortex storage using CC-ApiServer

    Args:
        base_url (str): base url of CerebralCortex-APIServer. For example, http://localhost/
        username (str): username
        password (str): password of the user
        stream_metadata (dict): metadata of the stream
        data_file_path (str): stream data file path that needs to be uploaded

    Returns:
        dict: HTTP response.content

    Raises:
        Exception: if stream data upload fails

    """
    login_url = base_url+"api/v3/user/login"
    register_stream_url = base_url+"api/v3/stream/register"

    auth = login_user(login_url, username, password)
    status = register_stream(register_stream_url, auth.get("auth_token"), stream_metadata)

    stream_upload_url = base_url+"api/v3/stream/"+status.get("hash_id")

    try:
        f = open(data_file_path, "rb")
        files = {"file": (data_file_path, f)}

        headers = {"Accept": "application/json", "Authorization": auth.get("auth_token")}
        response = requests.put(stream_upload_url, files=files, headers=headers)

        return json.loads(response.content)
    except Exception as e:
        raise Exception("Stream data upload failed. "+str(e))


