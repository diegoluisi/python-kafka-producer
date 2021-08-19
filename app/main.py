#!/usr/bin/env python
import threading, time

#print(int(t))

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='lab-python-kafka-brokers.kafka.svc.cluster.local:9092')

        while not self.stop_event.is_set():
            #producer.send('input', b"test")
            #producer.send('input', b"\xc2Hola, mundo!")
            t = time.time()
            date = b(int(t))
            producer.send('input', date)
            time.sleep(1)

        producer.close()




def main():
    # Create 'input' Kafka topic
    try:
        admin = KafkaAdminClient(bootstrap_servers='lab-python-kafka-brokers.kafka.svc.cluster.local:9092')

        topic = NewTopic(name='input',
                         num_partitions=1,
                         replication_factor=1)
        admin.create_topics([topic])
    except Exception:
        pass

    tasks = [
        Producer(),
    ]

    # Start threads of a publisher/producer and a subscriber/consumer to 'input' Kafka topic
    for t in tasks:
        t.start()

    time.sleep(10)

    # Stop threads
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    main()
