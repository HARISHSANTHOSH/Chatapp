from enum import Enum


class OpenAIConstants:
    ENCODING_NAME = "cl100k_base"
    TIMEOUT_LIMIT = 60.0
    JSON_MODE_CONFIG = {"type": "json_object"}
    STREAM_OPTIONS_CONFIG = {"include_usage": True}
    MEMORY_TOKEN_LIMIT = 8192
    TEMPERATURE = 0
    MAX_ATTEMPTS = 3
    EMBEDDINGS_NODE_NAME = "embeddings-node"
    EMBEDDINGS_ENCODING_FORMAT = "float"
    MAX_ATTEMPTS_ERROR_MSG = "Max attempts reached due to {error_message}"


class OpenAIModels(Enum):
    MINI_MODEL = "gpt-4o-mini"
    DEFAULT_MODEL = "gpt-4o"
    LEGACY_MODEL = "gpt-4-turbo"
    SMALL_EMBEDDINGS_MODEL = "text-embedding-3-small"
    LARGE_EMBEDDINGS_MODEL = "text-embedding-3-large"


class OpenaiMessageRole(Enum):
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
    USER = "user"
