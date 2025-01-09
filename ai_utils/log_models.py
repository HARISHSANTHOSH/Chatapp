from datetime import datetime

from pydantic import BaseModel


class OpenAINodeRunLog(BaseModel):
    """Represents the log object for an OpenAI API call.
    Attributes:
        node_name: indicates the identifier for the purpose of API call.
        model: model used in the API call.
        llm_prompt: input messages or text (for embeddings) given.
        llm_response: Completions text output from OpenAI API.
        prompt_tokens: Input tokens used.
        completion_tokens: Output tokens used.
        total_tokens: total tokens used.
        is_sucess: Indicates whether API call purpose succeeded.
        attempt: Attempt no for the API call on this particular node.
        llm_functions: functions output for function calling.
        failure_reason: error message incase attempt failed.
        start_time: start time to calculate time duration of API call.
        end_time. end time to calculate time duration of API call.
    """

    node_name: str
    model: str
    llm_prompt: str
    llm_response: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    is_success: bool
    attempt: int
    llm_functions: str = ""
    failure_reason: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
