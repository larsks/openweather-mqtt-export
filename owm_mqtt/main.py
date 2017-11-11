#!/usr/bin/env python

import argparse
import json
import logging
import os
import requests
import sys
import time

import paho.mqtt.client as mqtt

LOG = logging.getLogger(__name__)

current_weather_url = ('http://api.openweathermap.org/data/2.5/weather?'
                       'id={city_id}&appid={api_key}&units=metric')


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--api-key',
                   default=os.environ.get('OPENWEATHERMAP_API_KEY'))
    p.add_argument('--city-id',
                   default=os.environ.get('OPENWEATHERMAP_CITY_ID'))
    p.add_argument('--interval', '-i',
                   default=os.environ.get('OPENWEATHERMAP_POLL_INTERVAL', 60),
                   type=int)
    p.add_argument('--topic',
                   default=os.environ.get('OPENWEATHERMAP_TOPIC_PREFIX', 'sensor'))
    p.add_argument('--mqtt-server', '-s',
                   default=os.environ.get('OPENWEATHERMAP_MQTT_SERVER'))

    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level='INFO')

    LOG.info('connecting to mqtt broker')
    mq = mqtt.Client()
    mq.loop_start()
    mq.connect(args.mqtt_server)

    url = current_weather_url.format(
        city_id=args.city_id,
        api_key=args.api_key)
    while True:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        topic = '{}/openweathermap/{}'.format(
            args.topic, data['id'])
        sample = data['main']
        sample['temperature'] = sample['temp']
        del sample['temp']
        sample['clouds'] = data['clouds']['all']
        sample['wind_speed'] = data['wind']['speed']
        sample['wind_direction'] = data['wind']['deg']
        sample['sensor_type'] = 'openweathermap'

        LOG.info('sending on %s sample %s', topic, sample)
        mq.publish(topic, json.dumps(sample))

        time.sleep(args.interval)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
