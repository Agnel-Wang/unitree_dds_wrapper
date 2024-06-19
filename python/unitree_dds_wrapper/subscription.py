from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import DataReader
from cyclonedds.util import duration
import threading
import time

from abc import ABC, abstractmethod

class Subscription(ABC):
  """
  message: 消息类型
  topic: 话题名称
  """
  def __init__(self, message, topic, participant = None):
    self._participant = participant if participant else DomainParticipant()
    self._topic = Topic(self._participant, topic, message)
    self._reader = DataReader(self._participant, self._topic)
    
    # 不初始化message() 可用于判断初次接受消息
    self.msg = None

    self.lock = threading.Lock()
    self._read_cmd_thread = threading.Thread(target=self._listen_cmd)
    self._read_cmd_thread.setDaemon(True)
    self._read_cmd_thread.start()
    
    self._last_recv_time = 0.
    self.timeout_ms = 1000.

  def _listen_cmd(self):
    for msg in self._reader.take_iter():
      self._last_recv_time = time.time()
      with self.lock:
        self.pre_communication()
        self.msg = msg
        self.post_communication()
  
  def isTimeout(self) -> bool:
    return time.time() - self._last_recv_time > self.timeout_ms / 1000.
  
  def post_communication(self):
    pass

  def pre_communication(self):
    pass

  def wait_for_connection(self):
    while self.msg is None:
      time.sleep(0.1)