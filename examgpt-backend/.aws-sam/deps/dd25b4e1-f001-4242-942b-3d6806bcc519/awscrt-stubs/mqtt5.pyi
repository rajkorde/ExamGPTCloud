from concurrent.futures import Future
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Callable, Optional, Sequence, Union

from awscrt import NativeResource as NativeResource
from awscrt import exceptions as exceptions
from awscrt.exceptions import AwsCrtError
from awscrt.http import HttpProxyOptions as HttpProxyOptions
from awscrt.http import HttpRequest as HttpRequest
from awscrt.io import ClientBootstrap as ClientBootstrap
from awscrt.io import ClientTlsContext as ClientTlsContext
from awscrt.io import SocketOptions as SocketOptions
from awscrt.mqtt import (
    Connection,
    ConnectReturnCode,
    OnConnectionClosedData,
    OnConnectionFailureData,
    OnConnectionSuccessData,
)
from awscrt.mqtt import QoS as Mqtt3QoS

class QoS(IntEnum):
    AT_MOST_ONCE: int
    AT_LEAST_ONCE: int
    EXACTLY_ONCE: int

    def to_mqtt3(self) -> Mqtt3QoS: ...

class ConnectReasonCode(IntEnum):
    SUCCESS: int
    UNSPECIFIED_ERROR: int
    MALFORMED_PACKET: int
    PROTOCOL_ERROR: int
    IMPLEMENTATION_SPECIFIC_ERROR: int
    UNSUPPORTED_PROTOCOL_VERSION: int
    CLIENT_IDENTIFIER_NOT_VALID: int
    BAD_USERNAME_OR_PASSWORD: int
    NOT_AUTHORIZED: int
    SERVER_UNAVAILABLE: int
    SERVER_BUSY: int
    BANNED: int
    BAD_AUTHENTICATION_METHOD: int
    TOPIC_NAME_INVALID: int
    PACKET_TOO_LARGE: int
    QUOTA_EXCEEDED: int
    PAYLOAD_FORMAT_INVALID: int
    RETAIN_NOT_SUPPORTED: int
    QOS_NOT_SUPPORTED: int
    USE_ANOTHER_SERVER: int
    SERVER_MOVED: int
    CONNECTION_RATE_EXCEEDED: int

class DisconnectReasonCode(IntEnum):
    NORMAL_DISCONNECTION: int
    DISCONNECT_WITH_WILL_MESSAGE: int
    UNSPECIFIED_ERROR: int
    MALFORMED_PACKET: int
    PROTOCOL_ERROR: int
    IMPLEMENTATION_SPECIFIC_ERROR: int
    NOT_AUTHORIZED: int
    SERVER_BUSY: int
    SERVER_SHUTTING_DOWN: int
    KEEP_ALIVE_TIMEOUT: int
    SESSION_TAKEN_OVER: int
    TOPIC_FILTER_INVALID: int
    TOPIC_NAME_INVALID: int
    RECEIVE_MAXIMUM_EXCEEDED: int
    TOPIC_ALIAS_INVALID: int
    PACKET_TOO_LARGE: int
    MESSAGE_RATE_TOO_HIGH: int
    QUOTA_EXCEEDED: int
    ADMINISTRATIVE_ACTION: int
    PAYLOAD_FORMAT_INVALID: int
    RETAIN_NOT_SUPPORTED: int
    QOS_NOT_SUPPORTED: int
    USE_ANOTHER_SERVER: int
    SERVER_MOVED: int
    SHARED_SUBSCRIPTIONS_NOT_SUPPORTED: int
    CONNECTION_RATE_EXCEEDED: int
    MAXIMUM_CONNECT_TIME: int
    SUBSCRIPTION_IDENTIFIERS_NOT_SUPPORTED: int
    WILDCARD_SUBSCRIPTIONS_NOT_SUPPORTED: int

class PubackReasonCode(IntEnum):
    SUCCESS: int
    NO_MATCHING_SUBSCRIBERS: int
    UNSPECIFIED_ERROR: int
    IMPLEMENTATION_SPECIFIC_ERROR: int
    NOT_AUTHORIZED: int
    TOPIC_NAME_INVALID: int
    PACKET_IDENTIFIER_IN_USE: int
    QUOTA_EXCEEDED: int
    PAYLOAD_FORMAT_INVALID: int

class SubackReasonCode(IntEnum):
    GRANTED_QOS_0: int
    GRANTED_QOS_1: int
    GRANTED_QOS_2: int
    UNSPECIFIED_ERROR: int
    IMPLEMENTATION_SPECIFIC_ERROR: int
    NOT_AUTHORIZED: int
    TOPIC_FILTER_INVALID: int
    PACKET_IDENTIFIER_IN_USE: int
    QUOTA_EXCEEDED: int
    SHARED_SUBSCRIPTIONS_NOT_SUPPORTED: int
    SUBSCRIPTION_IDENTIFIERS_NOT_SUPPORTED: int
    WILDCARD_SUBSCRIPTIONS_NOT_SUPPORTED: int

class UnsubackReasonCode(IntEnum):
    SUCCESS: int
    NO_SUBSCRIPTION_EXISTED: int
    UNSPECIFIED_ERROR: int
    IMPLEMENTATION_SPECIFIC_ERROR: int
    NOT_AUTHORIZED: int
    TOPIC_FILTER_INVALID: int
    PACKET_IDENTIFIER_IN_USE: int

class ClientSessionBehaviorType(IntEnum):
    DEFAULT: int
    CLEAN: int
    REJOIN_POST_SUCCESS: int
    REJOIN_ALWAYS: int

class PayloadFormatIndicator(IntEnum):
    AWS_MQTT5_PFI_BYTES: int
    AWS_MQTT5_PFI_UTF8: int

class RetainHandlingType(IntEnum):
    SEND_ON_SUBSCRIBE: int
    SEND_ON_SUBSCRIBE_IF_NEW: int
    DONT_SEND: int

class RetainAndHandlingType(IntEnum):
    SEND_ON_SUBSCRIBE: int
    SEND_ON_SUBSCRIBE_IF_NEW: int
    DONT_SEND: int

class ExtendedValidationAndFlowControlOptions(IntEnum):
    NONE: int
    AWS_IOT_CORE_DEFAULTS: int

class ClientOperationQueueBehaviorType(IntEnum):
    DEFAULT: int
    FAIL_NON_QOS1_PUBLISH_ON_DISCONNECT: int
    FAIL_QOS0_PUBLISH_ON_DISCONNECT: int
    FAIL_ALL_ON_DISCONNECT: int

class ExponentialBackoffJitterMode(IntEnum):
    DEFAULT: int
    NONE: int
    FULL: int
    DECORRELATED: int

@dataclass
class UserProperty:
    name: Optional[str] = ...
    value: Optional[str] = ...

class OutboundTopicAliasBehaviorType(IntEnum):
    DEFAULT: int
    MANUAL: int
    LRU: int
    DISABLED: int

class InboundTopicAliasBehaviorType(IntEnum):
    DEFAULT: int
    ENABLED: int
    DISABLED: int

@dataclass
class TopicAliasingOptions:
    outbound_behavior: Optional[OutboundTopicAliasBehaviorType] = ...
    outbound_cache_max_size: Optional[int] = ...
    inbound_behavior: Optional[InboundTopicAliasBehaviorType] = ...
    inbound_cache_max_size: Optional[int] = ...

@dataclass
class NegotiatedSettings:
    maximum_qos: Optional[QoS] = ...
    session_expiry_interval_sec: Optional[int] = ...
    receive_maximum_from_server: Optional[int] = ...
    maximum_packet_size_to_server: Optional[int] = ...
    topic_alias_maximum_to_server: Optional[int] = ...
    topic_alias_maximum_to_client: Optional[int] = ...
    server_keep_alive_sec: Optional[int] = ...
    retain_available: Optional[bool] = ...
    wildcard_subscriptions_available: Optional[bool] = ...
    subscription_identifiers_available: Optional[bool] = ...
    shared_subscriptions_available: Optional[bool] = ...
    rejoined_session: Optional[bool] = ...
    client_id: Optional[str] = ...

@dataclass
class ConnackPacket:
    session_present: Optional[bool] = ...
    reason_code: Optional[ConnectReasonCode] = ...
    session_expiry_interval_sec: Optional[int] = ...
    receive_maximum: Optional[int] = ...
    maximum_qos: Optional[QoS] = ...
    retain_available: Optional[bool] = ...
    maximum_packet_size: Optional[int] = ...
    assigned_client_identifier: Optional[str] = ...
    topic_alias_maximum: Optional[int] = ...
    reason_string: Optional[str] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...
    wildcard_subscriptions_available: Optional[bool] = ...
    subscription_identifiers_available: Optional[bool] = ...
    shared_subscription_available: Optional[bool] = ...
    server_keep_alive_sec: Optional[int] = ...
    response_information: Optional[str] = ...
    server_reference: Optional[str] = ...

    @property
    def server_keep_alive(self) -> Optional[int]: ...
    @server_keep_alive.setter
    def server_keep_alive(self, value: Optional[int]) -> None: ...

@dataclass
class DisconnectPacket:
    reason_code: Optional[DisconnectReasonCode] = ...
    session_expiry_interval_sec: Optional[int] = ...
    reason_string: Optional[str] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...
    server_reference: Optional[str] = ...

@dataclass
class Subscription:
    topic_filter: str
    qos: Optional[QoS] = ...
    no_local: Optional[bool] = ...
    retain_as_published: Optional[bool] = ...
    retain_handling_type: Optional[Union[RetainAndHandlingType, RetainHandlingType]] = ...

@dataclass
class SubscribePacket:
    subscriptions: Sequence[Subscription]
    subscription_identifier: Optional[int] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...

@dataclass
class SubackPacket:
    reason_string: Optional[str] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...
    reason_codes: Optional[Sequence[SubackReasonCode]] = ...

@dataclass
class UnsubscribePacket:
    topic_filters: Sequence[str]
    user_properties: Optional[Sequence[UserProperty]] = ...

@dataclass
class UnsubackPacket:
    reason_string: Optional[str] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...
    reason_codes: Optional[Sequence[DisconnectReasonCode]] = ...

@dataclass
class PublishPacket:
    payload: Optional[Any] = ...
    qos: Optional[QoS] = ...
    retain: Optional[bool] = ...
    topic: Optional[str] = ...
    payload_format_indicator: Optional[PayloadFormatIndicator] = ...
    message_expiry_interval_sec: Optional[int] = ...
    topic_alias: Optional[int] = ...
    response_topic: Optional[str] = ...
    correlation_data_bytes: Optional[Union[bytes, str]] = ...
    correlation_data: Optional[Any] = ...
    subscription_identifiers: Optional[Sequence[int]] = ...
    content_type: Optional[str] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...

@dataclass
class PubackPacket:
    reason_code: Optional[PubackReasonCode] = ...
    reason_string: Optional[str] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...

@dataclass
class ConnectPacket:
    keep_alive_interval_sec: Optional[int] = ...
    client_id: Optional[str] = ...
    username: Optional[str] = ...
    password: Optional[str] = ...
    session_expiry_interval_sec: Optional[int] = ...
    request_response_information: Optional[bool] = ...
    request_problem_information: Optional[bool] = ...
    receive_maximum: Optional[int] = ...
    maximum_packet_size: Optional[int] = ...
    will_delay_interval_sec: Optional[int] = ...
    will: Optional[PublishPacket] = ...
    user_properties: Optional[Sequence[UserProperty]] = ...

class WebsocketHandshakeTransformArgs:
    def __init__(self, client: Client, http_request: HttpRequest, done_future: Future[Any]) -> None:
        self.client: Client
        self.http_request: HttpRequest

    def set_done(self, exception: Optional[Exception] = ...) -> None: ...

@dataclass
class PublishReceivedData:
    publish_packet: Optional[PublishPacket] = ...

@dataclass
class OperationStatisticsData:
    incomplete_operation_count: int = ...
    incomplete_operation_size: int = ...
    unacked_operation_count: int = ...
    unacked_operation_size: int = ...

@dataclass
class LifecycleStoppedData: ...

@dataclass
class LifecycleAttemptingConnectData: ...

@dataclass
class LifecycleConnectSuccessData:
    connack_packet: Optional[ConnackPacket] = ...
    negotiated_settings: Optional[NegotiatedSettings] = ...

@dataclass
class LifecycleConnectFailureData:
    connack_packet: Optional[ConnackPacket] = ...
    exception: Optional[Exception] = ...

@dataclass
class LifecycleDisconnectData:
    disconnect_packet: Optional[DisconnectPacket] = ...
    exception: Optional[Exception] = ...

@dataclass
class PublishCompletionData:
    puback: Optional[PubackPacket] = ...

@dataclass
class ClientOptions:
    host_name: str
    port: Optional[int] = ...
    bootstrap: Optional[ClientBootstrap] = ...
    socket_options: Optional[SocketOptions] = ...
    tls_ctx: Optional[ClientTlsContext] = ...
    http_proxy_options: Optional[HttpProxyOptions] = ...
    websocket_handshake_transform: Optional[Callable[[WebsocketHandshakeTransformArgs], None]] = ...
    connect_options: Optional[ConnectPacket] = ...
    session_behavior: Optional[ClientSessionBehaviorType] = ...
    extended_validation_and_flow_control_options: Optional[
        ExtendedValidationAndFlowControlOptions
    ] = ...
    offline_queue_behavior: Optional[ClientOperationQueueBehaviorType] = ...
    retry_jitter_mode: Optional[ExponentialBackoffJitterMode] = ...
    min_reconnect_delay_ms: Optional[int] = ...
    max_reconnect_delay_ms: Optional[int] = ...
    min_connected_time_to_reset_reconnect_delay_ms: Optional[int] = ...
    ping_timeout_ms: Optional[int] = ...
    connack_timeout_ms: Optional[int] = ...
    ack_timeout_sec: Optional[int] = ...
    topic_aliasing_options: Optional[TopicAliasingOptions] = ...
    on_publish_callback_fn: Optional[Callable[[PublishReceivedData], None]] = ...
    on_lifecycle_event_stopped_fn: Optional[Callable[[LifecycleStoppedData], None]] = ...
    on_lifecycle_event_attempting_connect_fn: Optional[
        Callable[[LifecycleAttemptingConnectData], None]
    ] = ...
    on_lifecycle_event_connection_success_fn: Optional[
        Callable[[LifecycleConnectSuccessData], None]
    ] = ...
    on_lifecycle_event_connection_failure_fn: Optional[
        Callable[[LifecycleConnectFailureData], None]
    ] = ...
    on_lifecycle_event_disconnection_fn: Optional[Callable[[LifecycleDisconnectData], None]] = ...

class _ClientCore:
    def __init__(self, client_options: ClientOptions) -> None: ...

class Client(NativeResource):
    def __init__(self, client_options: ClientOptions) -> None: ...
    def start(self) -> None: ...
    def stop(self, disconnect_packet: Optional[DisconnectPacket] = ...) -> None: ...
    def publish(self, publish_packet: PublishPacket) -> Future[PublishCompletionData]: ...
    def subscribe(self, subscribe_packet: SubscribePacket) -> Future[SubackPacket]: ...
    def unsubscribe(self, unsubscribe_packet: UnsubscribePacket) -> Future[UnsubackPacket]: ...
    def get_stats(self) -> Future[OperationStatisticsData]: ...
    def new_connection(
        self,
        on_connection_interrupted: Optional[Callable[[Connection, AwsCrtError], None]] = ...,
        on_connection_resumed: Optional[
            Callable[[Connection, ConnectReturnCode, bool], None]
        ] = ...,
        on_connection_success: Optional[
            Callable[[Connection, OnConnectionSuccessData], None]
        ] = ...,
        on_connection_failure: Optional[
            Callable[[Connection, OnConnectionFailureData], None]
        ] = ...,
        on_connection_closed: Optional[Callable[[Connection, OnConnectionClosedData], None]] = ...,
    ) -> Connection: ...
