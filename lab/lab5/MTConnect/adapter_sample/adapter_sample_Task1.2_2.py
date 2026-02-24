# MTConnet adapter sample for ME597 Lab5

import random
import sys
import time
import datetime
from data_item import Event, Sample  # load data_item package
from mtconnect_adapter import Adapter  # load mtconnect_adapter package


class MTConnectAdapter(object):

    def __init__(self, host, port):
        # MTConnect adapter connection info
        self.host = host
        self.port = port
        self.adapter = Adapter((host, port))

        # For samples
        self.t1 = Sample("t1")  # self.t1 takes 't1' data item id.
        self.adapter.add_data_item(self.t1)  # adding self.t1 as a data item
        self.h1 = Sample("h1")  # self.h1 takes 'h1' data item id.
        self.adapter.add_data_item(self.h1)  # adding self.h1 as a data item
        ## Add more samples below

        # For events
        self.event = Event("event")  # self.event takes 'event' data item name.
        self.adapter.add_data_item(
            self.event
        )  # adding self.event as a data item
        ## Add more events below

        # MTConnnect adapter availability
        self.avail = Event("avail")
        self.adapter.add_data_item(self.avail)

        # Start MTConnect
        self.adapter.start()
        self.adapter.begin_gather()
        self.avail.set_value("AVAILABLE")
        self.adapter.complete_gather()
        self.adapter_stream()

    def adapter_stream(self):
        while True:
            try:
                # Do something here.
                t1 = random.uniform(
                    20, 25
                )  # this example is to take a random float between 15 and 25.
                h1 = random.uniform(
                    40, 60
                )  # this example is to take a random float between 40 and 60.

                self.adapter.begin_gather()
                self.t1.set_value(
                    str(t1)
                )  # set value of t1 data item, format: str(float)
                self.h1.set_value(
                    str(h1)
                )  # set value of h1 data item, format: str(float)
                self.adapter.complete_gather()

                print(
                    "{} RANDOM VALUE t1={} °C".format(
                        datetime.datetime.now(), t1
                    )
                )  # printing out datetime now and t1
                print(
                    "{} RANDOM VALUE h1={} %".format(
                        datetime.datetime.now(), h1
                    )
                )  # printing out datetime now and h1
                print(
                    datetime.datetime.now(),
                    "MTConnect data items gathering completed...\n",
                )  # printing out MTConnect data collection is done.

                time.sleep(3)  # wait for 2 seconds

            except KeyboardInterrupt:
                print("Stopping MTConnect...")
                self.adapter.stop()  # Stop adapter thread
                sys.exit()  # Terminate Python


## ====================== MAIN ======================
if __name__ == "__main__":
    print("Starting up!")
    MTConnectAdapter("127.0.0.1", 7879)  # Args: host ip, port number
