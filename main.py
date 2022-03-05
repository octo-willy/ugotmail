from mail.client import Mail
from threading import Thread
from queue import Queue
import keyring

def main():

    #instantiate a FIFO queue with maxsize=10 (will block if queue.Full)
    SHARED_QUEUE = Queue(maxsize=10)
    
    #instantiate two client sessions
    producer_client = Mail("outlook.office365.com",993,
                            keyring.get_credential("HOTMAIL",None).username,
                            keyring.get_credential("HOTMAIL",None).password
                            )
    consumer_client = Mail("outlook.office365.com",993,
                            keyring.get_credential("HOTMAIL",None).username,
                            keyring.get_credential("HOTMAIL",None).password
                            )

    #spawning a background task which monitors new mail and put it into queue as task
    Thread(target=producer_client.run_idle,args=(SHARED_QUEUE,),daemon=True).start()
    
    #spawning a consumer that processes any new task in queue
    Thread(target=consumer_client.handle_tasks,args=(SHARED_QUEUE,)).start()
    

if __name__ == '__main__':
    main()