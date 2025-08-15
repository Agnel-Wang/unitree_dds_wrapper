from cyclonedds.topic import Topic
from cyclonedds.pub import DataWriter
from .dds_context import global_participant
import threading

class Publisher:
  """
  message: 消息类型
  topic: 话题名称
  """
  def __init__(self, message, topic, participant = None):
    self._participant = participant if participant else global_participant
    self._topic = Topic(self._participant, topic, message)
    self._writer = DataWriter(self._participant, self._topic)
    self.msg = message()
    self.lock = threading.Lock()

  def write(self, msg = None):
    if msg is None:
      with self.lock:
        self.pre_communication()
        self._writer.write(self.msg)
        self.post_communication()
    else:
      self._writer.write(msg)

  def post_communication(self):
    pass

  def pre_communication(self):
    pass