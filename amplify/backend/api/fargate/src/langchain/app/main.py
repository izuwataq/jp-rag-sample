# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/
"""FastAPI で用意する各種 API を定義するモジュール
"""
import os
from typing import Dict, Literal

import boto3
from amplify.backend.api.fargate.src.langchain.app.logics.convert_s3url import convert_presigned_url
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logics import llm_with_doc
from schemas import LLMWithDocReqBody

app = FastAPI()

origins = os.environ["ALLOW_ORIGINS"].split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
REGION = os.environ["AWS_REGION"]
KENDRA_INDEX_ID: str = os.environ["KENDRA_INDEX_ID"]
SAGEMAKER_ENDPOINT_NAME: str = os.environ.get("SAGEMAKER_ENDPOINT_NAME", None)
LLM: Literal["rinna", "claude"] = os.environ.get("LLM", "rinna")
kendra_client = boto3.client("kendra", region_name=REGION)


@app.post("/v2/llm-with-doc")
async def llm_with_doc_handler(
    body: LLMWithDocReqBody
):
    """LLM に対してドキュメントとチャット履歴を直接渡す"""
    return llm_with_doc(
        body, endpoint_name=SAGEMAKER_ENDPOINT_NAME, aws_region=REGION, llm_type=LLM
    )


@app.post("/v2/kendra/query")
async def kendra_query(body: Dict):
    """Kendra の Query API をキックする"""
    request_body = body["input"]
    response = kendra_client.query(**request_body)
    return convert_presigned_url(response)


@app.post("/v2/kendra/send")
async def kendra_send(body: Dict):
    """Kendra の SubmitFeedback API をキックする"""
    kendra_request_body = body["input"]
    response = kendra_client.submit_feedback(**kendra_request_body)
    return response


@app.post("/v2/kendra/describeIndex")
async def kendra_describe(
    body: Dict
):
    """Kendra の DesribeIndex API をキックする"""
    kendra_request_body = body["input"]
    response = kendra_client.describe_index(**kendra_request_body)
    return response
