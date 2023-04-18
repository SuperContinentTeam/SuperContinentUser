import datetime
import hashlib
import json
import time
import hmac

import httpx

from utils.environments import Env

HOST = "ses.tencentcloudapi.com"
CT = "application/json; charset=utf-8"
ALGORITHM = "TC3-HMAC-SHA256"
REGION = "ap-hongkong"
SERVICE = "ses"


def sign(key, msg: str, digest=True):
    result = hmac.new(key, msg.encode(), hashlib.sha256)
    return result.digest() if digest else result.hexdigest()


def canonical_request(req_action: str, req_payload: dict):
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_query_string = ""
    canonical_headers = f"content-type:{CT}\nhost:{HOST}\nx-tc-action:{req_action.lower()}\n"
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(json.dumps(req_payload).encode()).hexdigest()

    return "\n".join((
        http_request_method,
        canonical_uri,
        canonical_query_string,
        canonical_headers,
        signed_headers,
        hashed_request_payload
    )), signed_headers


def signature(request_timestamp, _canonical_request):
    str_date = datetime.datetime.utcfromtimestamp(request_timestamp).strftime("%Y-%m-%d")
    credential_scope = f"{str_date}/{SERVICE}/tc3_request"

    string_to_sign = "\n".join((
        ALGORITHM,
        str(request_timestamp),
        credential_scope,
        hashlib.sha256(_canonical_request.encode()).hexdigest()
    ))

    secret_date = sign(f"TC3{Env.TENCENT_SECRET_KEY}".encode(), str_date)
    secret_service = sign(secret_date, SERVICE)
    secret_signing = sign(secret_service, "tc3_request")
    return sign(secret_signing, string_to_sign, digest=False), credential_scope


def authorization(scope, signed_header, signature_result):
    _scope = f"Credential={Env.TENCENT_SECRET_ID}/{scope}"
    _signed_header = f"SignedHeaders={signed_header}"
    _signature = f"Signature={signature_result}"
    return f"{ALGORITHM} {', '.join((_scope, _signed_header, _signature))}"


class TencentSmsAdapter:
    def __init__(self):
        self.client = httpx.AsyncClient()

    def clean_header(self):
        self.client.headers = {}

    def build_header(self, request_version, request_action, request_payload):
        self.clean_header()

        int_timestamp = int(time.time())

        _canonical_request, _sign_header = canonical_request(request_action, request_payload)
        _signature, _scope = signature(int_timestamp, _canonical_request)
        _authorization = authorization(_scope, _sign_header, _signature)

        self.client.headers.update({
            "Authorization": _authorization,
            "Content-Type": CT,
            "Host": HOST,
            "X-TC-Action": request_action,
            "X-TC-Timestamp": str(int_timestamp),
            "X-TC-Version": request_version,
            "X-TC-Region": REGION
        })

    async def send_email(self, to_addresses: list, subject, template_id, message: dict | str):
        payload = {
            "FromEmailAddress": Env.FROM_ADDRESS,
            "Destination": to_addresses,
            "Subject": subject
        }

        if isinstance(message, dict):
            payload["Template"] = {"TemplateID": template_id, "TemplateData": json.dumps(message)}
        else:
            payload["Simple"] = {"Text": message}

        self.build_header("2020-10-02", "SendEmail", payload)
        return await self.client.post(f"https://{HOST}/", json=payload)

    async def send_code(self, recipient, subject, code):
        return await self.send_email(
            [recipient],
            subject,
            Env.TEMPLATE_ID,
            {Env.TEMPLATE_ARG: code}
        )


SmsAdapter = TencentSmsAdapter()

if __name__ == "__main__":
    from pprint import pprint
    import asyncio


    async def main():
        response = await SmsAdapter.send_code(
            "soleperson@126.com",
            "验证码",
            "123456"
        )
        pprint(response.json())


    asyncio.run(main())
