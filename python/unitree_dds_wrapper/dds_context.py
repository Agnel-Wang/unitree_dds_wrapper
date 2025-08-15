from cyclonedds.domain import DomainParticipant

# default DDS participant for publishers and subscribers
global_participant = DomainParticipant(domain_id=0)