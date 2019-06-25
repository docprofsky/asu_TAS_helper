#! /usr/bin/env python3
# coding: utf-8

from pycookiecheat import chrome_cookies
import requests
from datetime import date, datetime, time, timedelta as td


def make_request_data(start_datetime, end_datetime):
    # captured from the form on tas.asu.edu
    data = {
        'bConfirm': '0',
        'mode': 'new',
        'cbotype': 'Hours Worked',
        'txtfrom': '05/10/2019',
        'txthourfrom': '8:00 AM',
        'txtto': '05/10/2019',
        'txthourto': '5:00 PM',
        'txthours': '8',
        'txtdest': '',
        'txtreason': '',
        'txtemail': '',
        'txtphone': '',
        'txtsub': ''
    }

    data['txtfrom'] = start_datetime.strftime('%m/%d/%Y')
    data['txthourfrom'] = start_datetime.strftime('%I:%M %p').strip('0')
    data['txtto'] = end_datetime.strftime('%m/%d/%Y')
    data['txthourto'] = end_datetime.strftime('%I:%M %p').strip('0')
    data['txthours'] = '{:.2f}'.format((end_datetime - start_datetime) / td(hours=1))

    return data

def submit_request(data, cookies={}):
    form_url = 'https://tas.asu.edu/request_save.cfm'
    cookies = chrome_cookies(form_url)
    cookies.update({})
    return requests.post(form_url, data=data, cookies=cookies)


def round_timedelta(td_to_round):
    rounded_td = round(td_to_round / td(minutes=15)) * td(minutes=15)
    residual = td_to_round - rounded_td
    return (rounded_td, residual)

def round_datetime(datetime_to_round):
    td_from_midnight = datetime.combine(date.min, datetime_to_round.time()) - datetime.min
    rounded_td_from_midnight, _ = round_timedelta(td_from_midnight)
    rounded_datetime = datetime.combine(datetime_to_round.date(), time.min) + rounded_td_from_midnight
    return rounded_datetime


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Submit hours worked to TAS')
    parser.add_argument('start_time', type=time.fromisoformat,
                        help='time work started at, ISO 8601 format')
    parser.add_argument('end_time', type=time.fromisoformat,
                        help='time work finished at, ISO 8601 format')
    parser.add_argument('-d', '--date', type=date.fromisoformat, default=date.today(),
                        help='date that work occured on, ISO 8601 format. Default is today')

    args = parser.parse_args()


    start_time = datetime.combine(args.date, args.start_time)
    end_time = datetime.combine(args.date, args.end_time)

    hours_worked = end_time - start_time
    hours_worked_rounded, residual = round_timedelta(hours_worked)

    residual_str = '{}{}'.format('-' if residual / td(seconds=1) < 0 else '', abs(residual))
    print('time worked: {}, rounded time worked: {}, residual: {}'.format(
            hours_worked, hours_worked_rounded, residual_str))

    start_time_rounded = round_datetime(start_time)
    end_time_rounded = start_time_rounded + hours_worked_rounded

    print("Submitting start time: {} end time: {}".format(start_time_rounded, end_time_rounded))

    r = submit_request(make_request_data(start_time_rounded, end_time_rounded))
    print(r, r.content)
