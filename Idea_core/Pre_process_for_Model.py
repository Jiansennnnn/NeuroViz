from util import *
import numpy as np
import pandas as pd
import openpyxl 
import os
import dashscope

from util.constant import *
from util.models import Response_Excel_Range
import time
import json
from json import JSONDecodeError
from pydantic import ValidationError
import logging
import random

logging.basicConfig(filename="main.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def remove_backticks(s):
    return s.replace('```', '')

def _get_response(attempt: int, user_prompt: str):
    temperature = min(Model_PARAMS_Compute['temperature'] + 0.2 * attempt, 1.0)
    sys_prompt = LLM_PARAMS_Idea['system_prompt']
    messages = [
        {'role': 'system', 'content': [{'text': sys_prompt}]},
        {'role': 'user', 'content': user_prompt}
        ]
    response = dashscope.MultiModalConversation.call(
        api_key=Model_PARAMS_Compute['API_KEY'],
        model=Model_PARAMS_Compute['model_name'],
        temperature=temperature,
        top_p=Model_PARAMS_Compute['top_p'],
        messages=messages,
        result_format='message'
        )

    return response

def _get_response_comment(attempt: int, user_prompt: str):
    temperature = min(Model_PARAMS_Comment['temperature'] + 0.2 * attempt, 1.0)
    sys_prompt = LLM_PARAMS_Corr_Comment['system_prompt']
    messages = [
        {'role': 'system', 'content': [{'text': sys_prompt}]},
        {'role': 'user', 'content': str(user_prompt)}
        ]
    response = dashscope.Generation.call(
        api_key=Model_PARAMS_Comment['API_KEY'],
        model=Model_PARAMS_Comment['model_name'],
        temperature=temperature,
        top_p=Model_PARAMS_Comment['top_p'],
        messages=messages,
        result_format='message'
        )

    return response

#async def get_response(img_path: dict, report: dict):
def get_response_Idea(img_path: dict, report: str):
    #selected_keys = ['corr_matrix', 'report']
    #report_msg = {key: report[key] for key in selected_keys if key in report}
    combined_text = report
    user_msg = [
            {"image": img_path['histogram_img_path']},
            {"image": img_path['scatter_img_path']},
            {"text": combined_text}
        ]

    max_retries = Model_PARAMS_Compute['max_retries']
    initial_delay = 1
    start_time = time.time()
    
    logger.info("get_response_Idea---->Start")
    for attempt in range(max_retries):
        try:
            response = _get_response(attempt, user_msg)
            try:
                if Model_PARAMS_Compute['model_name'] == "alibaba-intl":
                    message_content = json.loads(response.output.choices[0].message.content)
                    input_tokens = response.usage.input_tokens
                    output_tokens = response.usage.output_tokens
                else:
                    #message_content = json.loads(response.choices[0].message.content)
                    message_content = response['output']['choices'][0]['message']['content'][0]['text']
                    input_tokens = response['usage']['input_tokens']
                    output_tokens = response['usage']['output_tokens']
                    #input_tokens = response.usage.prompt_tokens
                    #output_tokens = response.usage.completion_tokens
                #llm_response = Response_Excel_Range(**message_content)
                llm_response = message_content
            except (JSONDecodeError, ValidationError) as e:
                logger.error(f"Malformed response received at attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                    continue
                else:
                    pass
                    #raise HTTPException(status_code=500, detail=f"Malformed response received, retries exhausted: {e}")
                    logger.info(f"retries exhausted: {e}")
            break
        except Exception as e:
            pass
            logger.info(f"Error in sending request: {e}")
            #raise HTTPException(status_code=500, detail=f"Error in sending request: {e}")
    # usage of tokens
    time_elapsed = time.time() - start_time
    logger.info("get_response_Idea---->End")
    logger.info(f"Total attempts {attempt + 1}/{max_retries}; Request elapsed: {time_elapsed}")
    logger.info(f"Total tokens: {input_tokens + output_tokens}; Input tokens: {input_tokens}; Output tokens: {output_tokens}")
    return llm_response

async def Get_comment(corr_matrix, xy_fields, descriptive_statistics):
    combined_text = descriptive_statistics
    user_msg = [
            {"text": corr_matrix},
            {"text": str(xy_fields)},
            {"text": combined_text}
        ]
    max_retries = Model_PARAMS_Compute['max_retries']
    initial_delay = 1
    start_time = time.time()
    
    logger.info("Get_comment---->Start")
    for attempt in range(max_retries):
        try:
            response = _get_response_comment(attempt, user_msg)
            try:
                if Model_PARAMS_Compute['model_name'] == "alibaba-intl":
                    message_content = json.loads(response.output.choices[0].message.content)
                    input_tokens = response.usage.input_tokens
                    output_tokens = response.usage.output_tokens
                else:
                    #message_content = json.loads(response.choices[0].message.content)
                    message_content = response['output']['choices'][0]['message']['content']
                    input_tokens = response['usage']['input_tokens']
                    output_tokens = response['usage']['output_tokens']
                    #input_tokens = response.usage.prompt_tokens
                    #output_tokens = response.usage.completion_tokens
                #llm_response = Response_Excel_Range(**message_content)
                llm_response = remove_backticks(message_content)
                llm_response = llm_response.replace('```json\n', '').replace('\n```', '').replace('json\n', '')
            except (JSONDecodeError, ValidationError) as e:
                logger.error(f"Malformed response received at attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                    continue
                else:
                    pass
                    #raise HTTPException(status_code=500, detail=f"Malformed response received, retries exhausted: {e}")
                    logger.info(f"retries exhausted: {e}")
            break
        except Exception as e:
            pass
            logger.info(f"Error in sending request: {e}")
            #raise HTTPException(status_code=500, detail=f"Error in sending request: {e}")
    # usage of tokens
    time_elapsed = time.time() - start_time
    logger.info("Get_comment---->End")
    logger.info(f"Total attempts {attempt + 1}/{max_retries}; Request elapsed: {time_elapsed}")
    logger.info(f"Total tokens: {input_tokens + output_tokens}; Input tokens: {input_tokens}; Output tokens: {output_tokens}")
    return llm_response