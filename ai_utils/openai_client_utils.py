import json
from typing import Callable, Type, TypeVar

import httpx
import openai
import tiktoken
from openai.types import CreateEmbeddingResponse
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.embedding import Embedding
from pydantic import BaseModel, ValidationError

from .constants import OpenAIConstants, OpenAIModels
from .log_models import OpenAINodeRunLog
from .retry import retry_with_exponential_backoff

T = TypeVar("T", bound=BaseModel)
class OpenAINode:
    """Represents the Node run for an OpenAI API call with given input prompt and associated requirements.

    Attributes:
           node_name: A string identifier for the purpose of the API.
           api_key: OpenAI API Key as string.
           messages: list of dictionaries of messages in expected OpenAI input format.
           log_hook: A callable which will pass the log object to be processed by the user.
           model: A string model name for the API call.
           temperature: Integer indicating the level of determinism in output response.
           stream: Provides a generator object which could used for SSE implementation.
           output_params: A pydantic model for JSON validation incase of using JSON mode.
           attempt: recursive attempt counter for OpenAI API call.
           prev_error: Error message from previous attempt to be passed as context for next attempt.
           max_attempts: Integer for attempt limit. 
    """

    def __init__(
                    self,
                    node_name:str,
                    api_key:str,
                    messages: list[dict],
                    log_hook: Callable,
                    model : str =OpenAIModels.DEFAULT_MODEL.value,
                    temperature: int = OpenAIConstants.TEMPERATURE,
                    stream: bool =False,
                    output_params: Type[T] | None = None,
                attempt: int = 0,
                prev_error: str | None = None,
                max_attempts: int = OpenAIConstants.MAX_ATTEMPTS,


                        )-> None:
                self.client = openai.OpenAI(
                    api_key=api_key,
                    timeout=httpx.Timeout(OpenAIConstants.TIMEOUT_LIMIT),
                )
                self.nod_name = node_name
                self.messages = messages
                self.log_hook = log_hook
                self.model = model
                self.temperature = temperature
                self.stream = stream
                self.output_params = output_params
                self.attempt = attempt
                self.prev_error = prev_error
                self.max_attempts = max_attempts

    @staticmethod
    def count_tokens_from_str(
                       
                        text:str , encoding_model: str = OpenAIConstants.ENCODING_NAME
                    )->int:
                        """
                        Count the number of tokens in a string of text.

                        Args:
                            text: input text string.
                            encoding_model: tokenizer encoding model for GPT

                        Returns:
                            num_tokens: Number of tokens for the given string.    
                        
                        
                        """
                        encoding  = tiktoken.get_encoding(encoding_model)
                        num_tokens = len(encoding.encode(text))
                        return num_tokens
        

        @retry_with_exponential_backoff
        def api_call(
            self,
            **kwargs,         
        )-> tuple[bool, str | ChatCompletion, openai.Stream[ChatCompletionChunk]]:
         """Performs the API call with the OpenAI SDK.

         Retruns: 
         A tuple consisting of :
         A bool from indicate the success or failure
         A Chatcompletion object
         
         
         """

         response_format = (
             OpenAIConstants.JSON_MODE_CONFIG if self.output_params else None
          )
        
         stream_options = (
            OpenAIConstants.STREAM_OPTIONS_CONFIG if self.stream else None
         )
    
         return self.client.chat.completions(
            model= self.model,
            temperature=self.temperature,
            response_format=response_format,
            stream= self.stream,
            stream_options=stream_options,
            **kwargs

         )

        def get_completion(
            self,
            **kwargs
        )->tuple[bool,str]:
         """
        OpenAI API call wrapped with functionalities for recursive attempts incase of failure in output validation.

        Returns:
            bool: to indicate success or failure of the operation.
            T: A pydantic object of class specified output_params attr incase of JSON mode, a string with completion response incase of successful run or a string with error message incase of failure.
        
         """
         self.attempt +=1
         log_data={
                "node_name":self.nod_name,
                "model":self.model

         }
         if self.attempt > self.max_attempts:
            return False, OpenAIConstants.MAX_ATTEMPTS_ERROR_MSG(
                error_msg =  self.prev_error
            )
         if self.attempt >1 and self.prev_error:
            if self.attempt ==2:
                self.messages.append(
                    {
                        "role":"system",
                        "content": f"Your last attempt result in error {self.prev_error}"
                    }
                )
            else:
                self.messages[-1] = {
                    "role": f"Your last attempt result in error : {self.prev_error}"
                }
         log_data["llm_prompts"] =  json.dumps(self.messages)

         result,response = self.api_call()

         if not result:
            log_data.update({
                "llm_response":"",
                "prompt_tokens":0,
                "completion_tokens":0,
                "total_tokens":0,
                "attempt": self.attempt,
                "is_sucess":False,
                "failure_reason":response




            })
            log_object = OpenAINodeRunLog(**log_data)
            self.log_hook(log=log_object)
            return False,response
          
         response_str = response.choices[0].message.content.strip()
         log_data.update(
            {
                "llm_response":response_str,
                "prompt_tokens":response.usage.prompt_tokens,
                "completion_tokens":response.usage.completion_tokens,
                "total_tokens":response.usage.total_tokens
            }
         )
         if self.output_params:
            try:
                response_object =  self.output_params.model_validate_json(
                    response_str
                )
            except ValidationError as e:
                self.prev_error = (
                    f"Error in JSON parsing for the text response: {e}"
                )

                log_data.update(
                    {
                        "attempt":self.attempt,
                        "is_sucess":False,
                        "failure_reason":self.prev_error
                    }
                )
                log_object= OpenAINodeRunLog(**log_data)
                self.log_hook(log=log_data)
         else:
             log_data["attempt"]=self.attempt
             log_data["is_sucess"]=True
             log_object =  OpenAINodeRunLog(**log_data)
             self.log_hook(log=log_object)
             return True, response_object
         
         log_data["attempt"]=self.attempt
         log_data["is_sucess"]=True
         log_object =  OpenAINodeRunLog(**log_data)
         self.log_hook(log=log_data)
         return True, response_str

