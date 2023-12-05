from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.pub import DataWriter

class Publisher:
  """
  message: 消息类型
  topic: 话题名称
  """
  def __init__(self, message, topic, participant = None):
    self._participant = participant if participant else DomainParticipant()
    self._topic = Topic(self._participant, topic, message)
    self._writer = DataWriter(self._participant, self._topic)
    self.msg = None

  def write(self):
    if self.msg:
      self._writer.write(self.msg)