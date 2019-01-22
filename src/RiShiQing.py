import requests
import json
import time


class RiShiQing(object):
    _userMessage = {
        'j_username': 'your_userName',
        'j_password': 'your_password'
    }
    _day = '2019.01.09'
    _header ={
        'token': 'your_token_from_url',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def get_token(self):
        token = requests.post('https://www.rishiqing.com/task/j_spring_security_check',
                      data=self._userMessage).json()['token']
        self._header['token'] = token
        print('token is change : %s' % token)

    def get_timer(self, day):
        result = []
        if day is not None:
            self._day = day
        timer_msg = requests.get('https://www.rishiqing.com/task/v1/todo/list', params={
            'startDate': self._day,
            'endDate': self._day
        }, headers=self._header)
        timers = timer_msg.json()
        if timers is not None and len(timers) >= 0:
            for timer in timers:
                clock = timer['clock']
                if clock is not None and len(clock) > 0:
                    startTime = clock['startTime']
                    endTime = clock['endTime']
                else:
                    continue
                workMsg = timer['name']
                boxContent = '%s - %s    %s' %(startTime, endTime, workMsg)
                result.append({
                    'id': timer['id'],
                    'boxContent': boxContent,
                    'isDone': timer['isDone']
                })
        else:
            if timers is None:
                self.get_token()
                self.get_timer(day)
        return result

    def set_timer(self, message, start_time, end_time, refresh):
        clock = {
            'startTime': start_time,
            'endTime': end_time,
            'alert': [],
            'id': None
        }
        data = {
            'name': message,
            'isInbox': False,
            'priority': 1,
            'startDate': self._day,
            'endDate': self._day,
            'clock': clock,
            'memberIds': '4141904',
            'isOpenToMember': False,
            'todoLabelIds': '',
            'responsibilityId': '',
            'isDone': True
        }
        data = json.dumps(data)
        requests.post('https://www.rishiqing.com/task/v1/todo', data=data, headers=self._header)
        if refresh is not None:
            refresh()

    def setFreshTime(self):
        self._header['freshTime'] = '4141904' + str(int(time.time()))

    def isDone(self, box_id, is_done, fresh):
        if is_done:
            is_done = False
        else:
            is_done = True
        data = {
            'id': box_id,
            'isDone': is_done
        }
        data = json.dumps(data)
        url = 'https://www.rishiqing.com/task/v1/todo/%s' % box_id
        self.setFreshTime()
        result = requests.put(url , data=data, headers=self._header).json()
        if fresh is not None:
            fresh()
        if result['id'] is not None:
            return True
        else:
            return False

    def delete_msg(self, box_id, fresh):
        url = 'https://www.rishiqing.com/task/v1/todo/%s' % box_id
        result = requests.delete(url, headers=self._header).json()
        print(result)
        if fresh is not None:
            fresh()

    def set_day(self, day, refresh):
        self._day = day
        if refresh is not None:
            refresh()

# 以下为测试
# app = RiShiQing()
# app.set_timer('测试手机', '21:00','21:05')
# app.get_timer(None)
