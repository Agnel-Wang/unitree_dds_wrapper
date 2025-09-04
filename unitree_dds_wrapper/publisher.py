from cyclonedds.topic import Topic
from cyclonedds.pub import DataWriter
from .dds_context import global_participant
import threading
from cyclonedds.qos import Qos, Policy
from cyclonedds.core import Listener
from cyclonedds.util import duration
from cyclonedds.core import DDSStatus
import time

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
    msg_ = self.msg if msg is None else msg

    with self.lock:
      self.pre_communication()
      self._writer.write(msg_)
      self.post_communication()

  def post_communication(self):
    pass

  def pre_communication(self):
    pass


class RequestPublisher(Publisher):
  """ 专为请求响应设计"""
  __publication_matched_count = 0

  def __init__(self, message, topic, participant = None):
    self._participant = participant if participant else global_participant
    self._topic = Topic(self._participant, topic, message)
    qos= Qos(
      Policy.Reliability.Reliable(max_blocking_time=duration(seconds=1.0)),
      Policy.Durability.TransientLocal,
    )
    self._writer = DataWriter(self._participant, self._topic, qos=qos,
      listener=Listener(on_publication_matched=self._on_publication_matched)
    )
    self.msg = message()

  def write(self, msg=None):
    # 发送前需确认连接 以保证每条都会被处理
    while self.__publication_matched_count == 0:
      time.sleep(0.01)

    msg_ = self.msg if msg is None else msg
    self._writer.write(msg_)

  def _on_publication_matched(self, writer, status):
    self.__publication_matched_count = status.current_count