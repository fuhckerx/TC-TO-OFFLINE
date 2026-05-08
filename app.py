import asyncio, os, sys, ssl, time, re, traceback
from datetime import datetime
from aiohttp import web, ClientSession
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# xxx.com খুব ভালো ওয়েবসাইট
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Pb2'))
import MajoRLoGinrEq_pb2, MajoRLoGinrEs_pb2, PorTs_pb2


KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

BASE_HEADERS = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB53"
}


def pad_pkcs7(data: bytes) -> bytes:
    padding_len = 16 - (len(data) % 16)
    return data + bytes([padding_len] * padding_len)

async def Ua():
    return "GarenaMSDK/4.0.18P6(SM-A125F;Android 11;en-US;USA;)"

def EnC_Vr(n: int) -> bytes:
    r = []
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            b |= 0x80
        r.append(b)
        if not n:
            break
    return bytes(r)

async def CrEaTe_VarianT(field_number, value):
    return EnC_Vr(field_number << 3 | 0) + EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    field_header = EnC_Vr(field_number << 3 | 2)
    data = value.encode() if isinstance(value, str) else value
    return field_header + EnC_Vr(len(data)) + data

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested = await CrEaTe_ProTo(value)
            packet.extend(await CrEaTe_LenGTh(field, nested))
        elif isinstance(value, int):
            packet.extend(await CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await CrEaTe_LenGTh(field, value))
    return packet

def DecodE_HeX(n):
    h = hex(n)[2:]
    if len(h) == 1:
        h = "0" + h
    return h

async def EnC_PacKeT(hex_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad_pkcs7(bytes.fromhex(hex_data))).hex()

async def GeneRaTePk(packet_hex, packet_prefix, key, iv):
    encrypted = await EnC_PacKeT(packet_hex, key, iv)
    length = len(encrypted) // 2
    hex_len = DecodE_HeX(length)
    if len(hex_len) == 2:   header = packet_prefix + "000000"
    elif len(hex_len) == 3: header = packet_prefix + "00000"
    elif len(hex_len) == 4: header = packet_prefix + "0000"
    else:                   header = packet_prefix + "000000"
    return bytes.fromhex(header + hex_len + encrypted)

async def encrypted_proto(plain: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.encrypt(pad_pkcs7(plain))


async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": await Ua(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid, "password": password,
        "response_type": "token", "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as resp:
            if resp.status != 200: return None, None
            j = await resp.json()
            return j.get("access_token"), j.get("open_id")

async def EncRypTMajoRLoGin(open_id, access_token):
    req = MajoRLoGinrEq_pb2.MajorLogin()
    req.event_time = str(datetime.now())[:-7]
    req.game_name = "free fire"
    req.platform_id = 1
    req.client_version = "1.123.1"
    req.system_software = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
    req.system_hardware = "Handheld"
    req.telecom_operator = "Verizon"
    req.network_type = "WIFI"
    req.screen_width = 1920
    req.screen_height = 1080
    req.screen_dpi = "280"
    req.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    req.memory = 3003
    req.gpu_renderer = "Adreno (TM) 640"
    req.gpu_version = "OpenGL ES 3.1 v1.46"
    req.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    req.client_ip = "223.191.51.89"
    req.language = "en"
    req.open_id = open_id
    req.open_id_type = "4"
    req.device_type = "Handheld"
    req.memory_available.version = 55
    req.memory_available.hidden_value = 81
    req.access_token = access_token
    req.platform_sdk_id = 1
    req.network_operator_a = "Verizon"
    req.network_type_a = "WIFI"
    req.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    req.external_storage_total = 36235
    req.external_storage_available = 31335
    req.internal_storage_total = 2519
    req.internal_storage_available = 703
    req.game_disk_storage_available = 25010
    req.game_disk_storage_total = 26628
    req.external_sdcard_avail_storage = 32992
    req.external_sdcard_total_storage = 36235
    req.login_by = 3
    req.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    req.reg_avatar = 1
    req.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    req.channel_type = 3
    req.cpu_type = 2
    req.cpu_architecture = "64"
    req.client_version_code = "2019118695"
    req.graphics_api = "OpenGLES2"
    req.supported_astc_bitset = 16383
    req.login_open_id_type = 4
    req.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    req.loading_time = 13564
    req.release_channel = "android"
    req.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    req.android_engine_init_flag = 110009
    req.if_push = 1
    req.is_vpn = 1
    req.origin_platform_type = "4"
    req.primary_platform_type = "4"
    return await encrypted_proto(req.SerializeToString())

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    async with ClientSession() as session:
        async with session.post(url, headers=BASE_HEADERS, data=payload, ssl=ssl_ctx) as resp:
            if resp.status == 200: return await resp.read()
            else:
                text = await resp.text()
                print(f"MajorLogin failed: {resp.status} {text[:200]}")
                return None

async def DecRypTMajoRLoGin(data):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(data)
    return proto

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    headers = BASE_HEADERS.copy()
    headers['Authorization'] = f"Bearer {token}"
    print(f"GetLoginData URL: {url}")
    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=payload, ssl=ssl_ctx) as resp:
            if resp.status == 200: return await resp.read()
            else:
                text = await resp.text()
                print(f"GetLoginData failed: {resp.status} {text[:200]}")
                return None

async def DecRypTLoGinDaTa(data):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(data)
    return proto

async def xAuThSTarTuP(target_uid, token, timestamp, key, iv):
    uid_hex = hex(target_uid)[2:]
    enc_timestamp = DecodE_HeX(timestamp)
    enc_token = token.encode().hex()
    enc_packet = await EnC_PacKeT(enc_token, key, iv)
    enc_packet_len = hex(len(enc_packet) // 2)[2:]
    uid_len = len(uid_hex)
    if uid_len == 9:   header = '0000000'
    elif uid_len == 8: header = '00000000'
    elif uid_len == 10:header = '000000'
    elif uid_len == 7: header = '000000000'
    else:              header = '0000000'
    return f"0115{header}{uid_hex}{enc_timestamp}00000{enc_packet_len}{enc_packet}"

# miakhalifa.com best website
online_writer = None
bot_info = None
spam_running = False


async def send_required_packets(bot_uid, key, iv):
    """Send packets 100 & 101 so the bot appears fully loaded."""
    fields1 = {
        1: 100,
        2: {
            1: bot_uid,
            2: "1.22.1",   
            3: "Android",
            4: "en",
        }
    }
    fields2 = {
        1: 101,
        2: {
            1: "[FF9000]RIZER",
            2: "1901",
            3: "arm64-v8a",
            4: str(int(time.time())),
        }
    }
    for fields in [fields1, fields2]:
        pkt = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', key, iv)
        online_writer.write(pkt)
        await online_writer.drain()
        await asyncio.sleep(0.2)
    print("✅ Required client info packets sent")


async def GenJoinSquadsPacket(code, K, V):
    fields = {
        1: 4,
        2: {
            4: bytes.fromhex("01090a0b121920"),
            5: str(code), 6: 6, 8: 1,
            9: {2: 800, 6: 11, 8: "1.111.1", 9: 5, 10: 1}
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)

async def ready_packet(bot_uid, K, V):
    """Toggle ready/unready – field 2.2 is omitted to just toggle."""
    fields = {1: 15, 2: {1: int(bot_uid)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)

async def ready_unready_spam(bot_uid, key, iv, duration=40):
    global spam_running, online_writer
    spam_running = True
    count = 0
    start = time.time()
    print(f"⚡ Starting ready/unready spam for {duration}s")
    while spam_running and (time.time() - start) < duration:
        try:
            if online_writer:
                pkt = await ready_packet(bot_uid, key, iv)
                online_writer.write(pkt)
                await online_writer.drain()
                count += 1
                if count % 2000 == 0:
                    print(f"   📤 Sent {count} packets")
                await asyncio.sleep(0.00)  
            else:
                await asyncio.sleep(0.0)
        except Exception as e:
            print(f"Spam error: {e}")
            await asyncio.sleep(0.0)
    spam_running = False
    print(f"✅ Spam finished. Total packets: {count}")


async def tcp_online_handler(ip, port, auth_token, bot_uid, key, iv):
    global online_writer
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            online_writer = writer
            writer.write(bytes.fromhex(auth_token))
            await writer.drain()
            print(f"Online TCP connected to {ip}:{port}")


            await send_required_packets(bot_uid, key, iv)

            while True:
                data = await reader.read(9999)
                if not data: break
        except Exception as e:
            print(f"TCP connection lost ({e}), reconnecting in 5s...")
            online_writer = None
            await asyncio.sleep(5)


async def http_join(request: web.Request):
    global bot_info, online_writer, spam_running
    teamcode = request.query.get('teamcode')
    if not teamcode:
        return web.Response(text="Missing teamcode", status=400)
    if not bot_info:
        return web.Response(text="Bot not initialized", status=503)
    if online_writer is None:
        return web.Response(text="TCP not connected", status=503)
    if spam_running:
        return web.Response(text="Spam already running", status=429)


    join_pkt = await GenJoinSquadsPacket(teamcode, bot_info['key'], bot_info['iv'])
    online_writer.write(join_pkt)
    await online_writer.drain()
    print(f"🚪 Joined squad: {teamcode}")


    await asyncio.sleep(1)


    asyncio.create_task(
        ready_unready_spam(bot_info['uid'], bot_info['key'], bot_info['iv'], 40)
    )
    return web.Response(text=f"Joining {teamcode} and starting ready/unready spam for 40s")

async def http_status(request):
    return web.json_response({
        "bot_uid": str(bot_info['uid']) if bot_info else None,
        "tcp_connected": online_writer is not None,
        "spam_running": spam_running
    })


def load_first_account():
    if not os.path.exists("accounts.txt"):
        return None, None
    with open("accounts.txt") as f:
        for line in f:
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                uid, pwd = line.split(':', 1)
                return uid.strip(), pwd.strip()
    return None, None


async def main():
    global bot_info
    uid, pwd = load_first_account()
    if not uid:
        print("No accounts found in accounts.txt")
        return

    print(f"Logging in with UID {uid}...")
    access_token, open_id = await GeNeRaTeAccEss(uid, pwd)
    if not access_token:
        print("Failed to get access token")
        return

    ml_payload = await EncRypTMajoRLoGin(open_id, access_token)
    ml_resp = await MajorLogin(ml_payload)
    if not ml_resp:
        print("MajorLogin failed")
        return

    ml_data = await DecRypTMajoRLoGin(ml_resp)
    key = ml_data.key
    iv = ml_data.iv
    token = ml_data.token
    bot_uid = ml_data.account_uid
    base_url = ml_data.url
    timestamp = ml_data.timestamp

    if not token:
        jwt_regex = r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
        matches = re.findall(jwt_regex, ml_resp.decode('latin-1', errors='ignore'))
        if matches:
            token = matches[0]
            print("JWT extracted via regex")
        else:
            print("No JWT found")
            return

    if not base_url:
        base_url = "https://clientbp.ggblueshark.com"

    print(f"Token: {token[:30]}... Bot UID: {bot_uid}")

    login_data_raw = await GetLoginData(base_url, ml_payload, token)
    if not login_data_raw:
        print("GetLoginData failed")
        return

    login_data = await DecRypTLoGinDaTa(login_data_raw)
    online_ip_port = login_data.Online_IP_Port
    if not online_ip_port:
        print("No server IP in login data")
        return
    online_ip, online_port = online_ip_port.split(':')
    print(f"Connecting to Online server: {online_ip}:{online_port}")

    bot_info = {
        'uid': bot_uid,
        'key': key,
        'iv': iv,
        'token': token,
        'region': login_data.Region,
    }

    auth_hex = await xAuThSTarTuP(int(bot_uid), token, int(timestamp), key, iv)


    asyncio.create_task(tcp_online_handler(online_ip, int(online_port), auth_hex, bot_uid, key, iv))

    
    app = web.Application()
    app.router.add_get('/join', http_join)
    app.router.add_get('/status', http_status)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()
    print("HTTP API running on port 5000")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())