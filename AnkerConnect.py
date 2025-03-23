#!/usr/bin/env python3
import paho.mqtt.publish
import json
import click
import concurrent.futures
import configparser
import logging as log

import cli.logfmt

from cli.config import configmgr
from cli.mqtt import mqtt_open


from libflagship.mqtt import MqttMsgType

config = configparser.ConfigParser()
config.read('config.ini')

# Local MQTT config
username = config['MQTT']['username']
password = config['MQTT']['password']
mqttIp = config['MQTT']['ip']
mqttPort = int(config['MQTT']['port'])
auth = {'username': username, 'password': password}

class Environment:

    def load_config(self, required=True):
        with self.config.open() as config:
            if not getattr(config, 'printers', False):
                msg = "No printers found in default.json!"


pass_env = click.make_pass_decorator(Environment)


# Setup all internal settings
@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.pass_context
def main(ctx):
    ctx.ensure_object(Environment)
    env = ctx.obj
    levels = {
        -3: log.CRITICAL,
        -2: log.ERROR,
        -1: log.WARNING,
        0: log.INFO,
        1: log.DEBUG,
    }
    env.level = 0
    cli.logfmt.setup_logging(levels[env.level])
    env.config = configmgr()


# Load Config
@main.group("mqtt", help="Low-level mqtt api access")
@pass_env
def mqtt(env):
    env.load_config()


# Loop function for ankermake mqtt server
def process_client(client):
    for msg, body in client.fetchloop():
        try:
            serial_number = msg.topic.split('/')[3]
            log.info(f"New cloud data from printer {serial_number}")
            new_topic = f"ankermake2mqtt/printers/{serial_number}/data"
            raw_data = json.dumps(body)
            log.info(raw_data)
            paho.mqtt.publish.single(new_topic, raw_data, hostname=mqttIp, port=mqttPort, auth=auth)
            log.info("")
        except Exception as e:
            log.error(f"Error processing message: {e}")


# Start mqtt loop function for every printer in config
@mqtt.command("mirror", help="Starting mirror to local mqtt server")
@pass_env
def mqtt_monitor(env):
    log.info("Starting mqtt ankermake cloud spoofing for printers in default.json")
    with env.config.modify() as cfg:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(0, len(cfg.printers)):
                executor.submit(process_client, mqtt_open(env.config, i, False))


if __name__ == "__main__":
    main()
