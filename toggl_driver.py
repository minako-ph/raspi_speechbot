# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import json

class TogglDriver:

    def __init__(self, _token):
        self._token = _token # api_token
        self._workspace_id = self.get_workspace_id(self._token)
        self._headers = {'Content-Type': 'application/json'}

    @staticmethod
    def get_workspace_id(api_token):
        # get workspace id from api/v8/workspaces
        r = requests.get('https://www.toggl.com/api/v8/workspaces',
                         auth=(api_token, 'api_token'))
        if r.status_code != 200:
            print("Error: cannot get workspace id. please check the token.")
            return ""

        # JSON形式でデータのエクスポート
        data = r.json()
        Data = data[0]
        return Data['id']

    def get_running_time_entry(self):
        # return time entry id of current entry
        r = requests.get('https://www.toggl.com/api/v8/time_entries/current',
                         auth=HTTPBasicAuth(self._token, 'api_token'))
        if r.status_code != 200:
            print("Error: cannot get running time entry. please check the token.")
            return ""
        data = r.json()['data']
        if data is None:
            return None
        return data['id']

    def start(self, description, pid):
        params = {"time_entry": {"description": description, "pid": pid, "created_with": "python"}}
        r = requests.post('https://www.toggl.com/api/v8/time_entries/start',
                          auth=HTTPBasicAuth(self._token, 'api_token'),
                          headers=self._headers,
                          data=json.dumps(params))
        print('time entry start. HTTP status :', r.status_code)

    def stop(self, running_time_entry_id):
        url = 'https://www.toggl.com/api/v8/time_entries/' + str(running_time_entry_id) + '/stop'
        r = requests.put(url, auth=HTTPBasicAuth(self._token, 'api_token'), headers=self._headers)

        print('time entry stop. HTTP status :', r.status_code)
        return r
