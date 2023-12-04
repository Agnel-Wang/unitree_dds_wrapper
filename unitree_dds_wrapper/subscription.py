from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import DataReader
from cyclonedds.util import duration
import threading

class Subscription:
  """
  message: 消息类型
  topic: 话题名称
  """
  def __init__(self, message, topic):
    self._participant = DomainParticipant()
    self._topic = Topic(self._participant, topic, message)
    self._reader = DataReader(self._participant, self._topic)
    
    self.msg = None

    self.lock = threading.Lock()
    self._read_cmd_thread = threading.Thread(target=self._listen_cmd)
    self._read_cmd_thread.setDaemon(True)
    self._read_cmd_thread.start()
    
  def _listen_cmd(self):
    for msg in self._reader.take_iter(timeout=duration(seconds=1)):
      with self.lock:
        self.msg = msg
