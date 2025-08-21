from .dds_context import global_participant
from cyclonedds.topic import Topic
from cyclonedds.sub import DataReader
from cyclonedds.util import duration
import threading
import time
from cyclonedds.qos import Qos, Policy
from abc import ABC
from cyclonedds.internal import InvalidSample
from cyclonedds.util import duration
from cyclonedds.core import Listener

class Subscription(ABC):
  """
  message: 消息类型
  topic: 话题名称
  autospin:
    默认是直接读取消息至self.msg; 但这样(在pub高频且msg复杂时)对CPU占用较高
    如果设置为False，则需要手动读取消息
  """
  def __init__(self, message, topic, participant = None, autospin=True):
    self._topic_name = topic
    self._participant = participant if participant else global_participant
    self._topic = Topic(self._participant, topic, message)
    qos = Qos(
      Policy.History.KeepLast(1),
      Policy.Reliability.BestEffort,
    )
    self._reader = DataReader(self._participant, self._topic, qos=qos)
    
    # 不初始化message() 可用于判断初次接受消息
    self.msg = None

    self.lock = threading.Lock()
    
    self._last_recv_time = 0.
    self.timeout_ms = 1000.

    self._autospin = autospin
    if autospin:
      self._read_thread = threading.Thread(target=self._listen_cmd)
      self._read_thread.daemon = True
      self._read_thread.start()

  def take_one(self):
    try:
      samples = self._reader.take(N=1)
    except Exception as e:
      return
    if samples and not isinstance(samples[0], InvalidSample):
      self._last_recv_time = time.time()
      with self.lock:
        self.msg = samples[0]

  def _listen_cmd(self):
    for msg in self._reader.take_iter():
      self._last_recv_time = time.time()
      with self.lock:
        self.pre_communication()
        self.msg = msg
        self.post_communication()
  
  def isTimeout(self) -> bool:
    if not self._autospin:
      self.take_one()
    return time.time() - self._last_recv_time > self.timeout_ms / 1000.
  
  def post_communication(self):
    pass

  def pre_communication(self):
    pass

  def wait_for_connection(self):
    t0 = time.time()
    warn_info = False
    while self.msg is None:
      time.sleep(0.1)
      if not self._autospin:
        self.take_one()
      if not warn_info:
        if time.time() - t0 > 2.:
          print(f"Waiting for connection {self._topic_name} ...")
          warn_info = True
    if warn_info:
      print(f"Connected {self._topic_name}.")
    time.sleep(0.1)
    
class RequestSubscription(ABC):
  """为请求响应模式设计的订阅类"""
  def __init__(self, message, topic, participant = None, depth=10, handler=None):
    assert depth > 1, "Depth must be greater than 1"

    self._topic_name = topic
    self._participant = participant if participant else global_participant
    self._topic = Topic(self._participant, topic, message)

    qos = Qos(
      Policy.History.KeepLast(depth),
      Policy.Reliability.Reliable(max_blocking_time=duration(seconds=1)),
    )
    self._reader = DataReader(self._participant, self._topic, qos=qos, 
      listener=(Listener(on_data_available=handler) if handler else None)
    )

  def take_one(self):
    try:
      samples = self._reader.take(N=1)
    except Exception as e:
      return None
    if not samples:
      return None
    sample = samples[0]
    if isinstance(sample, InvalidSample):
      return None
    return sample