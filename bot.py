import os
from highrise import BaseBot, Position
from highrise.__main__ import BotDefinition, main as client_main
import asyncio
from highrise import *
from highrise.models import *
from highrise.models import (
    AnchorPosition,
    ChannelEvent,
    ChannelRequest,
    ChatEvent,
    ChatRequest,
    CurrencyItem,
    EmoteEvent,
    EmoteRequest,
    Error,
    FloorHitRequest,
    GetRoomUsersRequest,
    GetWalletRequest,
    IndicatorRequest,
    Item,
    Position,
    Reaction,
    ReactionEvent,
    ReactionRequest,
    SessionMetadata,
    TeleportRequest,
    TipReactionEvent,
    User,
    UserJoinedEvent,
    UserLeftEvent,
)
import random
import time
from aiohttp import web
import threading
import json

dancs = [
    # 1
    "emote-lust",
    # 2
    "emote-superpose",
    # 3
    "dance-tiktok10",
    # 4
    "dance-weird",
    # 5
    "emote-charging",
    # 6
    "emote-snowball",
    # 7
    "emote-hot",
    # 8
    "emote-snowangel",
    # 9
    "dance-russian",
    # 10
    "emote-curtsy",
    # 11
    "emote-bow",
    # 12
    "dance-pennywise",
    # 13
    "dance-blackpink",
    # 14
    "emote-model",
    # 15
    "dance-tiktok8",
    # 16
    "dance-tiktok2",
    # 17
    "dance-macarena",
    # 18
    "emoji-gagging",
    # 19
    "emoji-flex",
    # 20
    "emoji-celebrate",
    # 21
    "emoji-cursing",
    # 22
    "idle-loop-sitfloor",
    # 23
    "emote-yes",
    # 24
    "emote-sad",
    # 25
    "emote-no",
    # 26
    "emote-laughing",
    # 27
    "emote-kiss",
    # 28
    "emote-hello",
    # 29
    "emote-zombierun",
    # 30
    "emote-pose8",
    # 31
    "emote-pose7",
    # 32
    "emote-pose5",
    # 33
    "emote-pose3",
    # 34
    "emote-pose1",
    # 35
    "idle-dance-casual",
    # 36
    "emote-cutey",
    # 37
    "emote-astronaut",
    # 38
    "idle-dance-tiktok4",
    # 39
    "emote-punkguitar",
    # 40
    "dance-icecream",
    # 41
    "emote-gravity",
    # 42
    "emote-fashionista",
    # 43
    "idle-uwu",
    # 44
    "dance-wrong",
    # 45
    "emote-dab",
    # 46
    "emote-robot",
    # 47
    "emote-rainbow",
    # 48
    "emote-nightfever",
    # 49
    "emote-harlemshake",
    # 50
    "emote-gangnam2",
    # 51
    "emote-tapdance",
    # 52
    "emote-peace",
    # 53
    "emote-panic",
    # 54
    "emote-clap",
    # 55
    "emote-thumbsup",
    # 56
    "emote-happy",
    # 57
    "emote-mad",
    # 58
    "emote-sleepy",
    # 59
    "emote-thewave",
    # 60
    "emote-think",
    # 61
    "emote-judochop",
    # 62
    "dance-breakdance",
    # 63
    "dance-handsup",
    # 64
    "dance-aerobics",
    # 65
    "dance-metal",
    # 66
    "dance-robotic",
    # 67
    "dance-smoothwalk",
    # 68
    "dance-spiritual",
    # 69
    "dance-singleladies",
    # 70
    "dance-voguehands",
    # 71
    "dance-duckwalk",
    # 72
    "emoji-angry",
    # 73
    "emoji-thumbsup",
    # 74
    "emoji-tired",
    # 75
    "emoji-pray",
    # 76
    "emoji-halo",
    # 77
    "emoji-sneeze",
    # 78
    "emoji-sick",
    # 79
    "emoji-naughty",
    # 80
    "emoji-scared",
    # 81
    "emoji-crying",
    # 82
    "emoji-dizzy",
    # 83
    "emoji-hadoken",
    # 84
    "emoji-arrogance",
    # 85
    "emoji-smirking",
    # 86
    "emoji-lying",
    # 87
    "emoji-give-up",
    # 88
    "emoji-punch",
    # 89
    "emoji-poop",
    # 90
    "emoji-there",
    # 91
    "idle-loop-annoyed",
    # 92
    "idle-loop-sad",
    # 93
    "idle-loop-happy",
    # 94
    "idle-loop-aerobics",
    # 95
    "idle-loop-tired",
    # 96
    "idle-loop-shy",
    # 97
    "idle-loop-tapdance",
    # 98
    "idle-dance-swinging",
    # 99
    "dance-tiktok1",
    # 100
    "dance-tiktok3",
    # 101
    "dance-tiktok4",
    # 102
    "dance-tiktok5",
    # 103
    "dance-tiktok6",
    # 104
    "dance-tiktok7",
    # 105
    "dance-tiktok9",
    # 106
    "dance-tiktok11",
    # 107
    "emote-pose2",
    # 108
    "emote-pose4",
    # 109
    "emote-pose6",
    # 110
    "emote-wave",
    # 111
    "emote-shrug",
    # 112
    "emote-facepalm",
    # 113
    "emote-confused",
    # 114
    "emote-victory",
    # 115
    "emote-point",
    # 116
    "emote-cry",
    # 117
    "emote-shy",
    # 118
    "emote-flex",
    # 119
    "emote-excited",
    # 120
    "emote-salute",
    # 121
    "dance-hype",
    # 122
    "dance-disco",
    # 123
    "dance-shuffle",
    # 124
    "dance-charleston",
    # 125
    "idle-dance-hiphop",
    # 126
    "idle-dance-kawaii",
    # 127
    "idle-loop-dance",
    # 128
    "emote-wink",
    # 129
    "dance-kpop",
    # 130
    "emote-heart",
    # 131 - Ghost Float
    "emote-ghost-idle",
    # 132 - Rest
    "sit-idle-cute",
]

valuesss = "ghjk"
user_ad = ["9.__"]

# Global stats
bot_stats = {
    "total_joins": 0,
    "total_dances": 0,
    "total_commands": 0,
    "start_time": time.time(),
    "online": False,
    "user_count": 0,
    "positions": {},  # username -> {x, y, z, facing, ts}
}

ROOM_ID = "696db8cb135ecd6d9ecf77e6"
BOT_NAME = "9.__"


class MyBot(BaseBot):

    def __init__(self):
        self.dances = {e: 5.0 for e in dancs}
        self.in_area_users = set()
        self.dance_event = asyncio.Event()
        self.ord = None
        self.ter = []
        self.run = False
        self.d = []
        self.current_dance = None

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        try:
            print("on")
            bot_stats["online"] = True
            asyncio.create_task(self.update_user_count())
        except Exception as e:
            print(f"error : {e}")

    async def update_user_count(self):
        while True:
            try:
                room_users = await self.highrise.get_room_users()
                bot_stats["user_count"] = len(room_users.content)
                # Update positions for all users in room
                for u, pos in room_users.content:
                    if hasattr(pos, 'x'):
                        bot_stats["positions"][u.username] = {
                            "x": round(pos.x, 2),
                            "y": round(pos.y, 2),
                            "z": round(pos.z, 2),
                            "facing": getattr(pos, 'facing', ''),
                            "ts": time.time(),
                        }
            except Exception as e:
                print(f"user count error: {e}")
            await asyncio.sleep(10)

    async def send_continuous_dances(self):
        while True:
            valid_users = []
            users_positions = await self.highrise.get_room_users()
            if isinstance(users_positions, Error) or not hasattr(users_positions, 'content'):
                await asyncio.sleep(5)
                continue
            for user, position in users_positions.content:
                if isinstance(position, Position):
                    x_range = (1, 1)
                    y_range = (0, 1.5)
                    z_range = (1, 1)
                    if (
                        x_range[0] <= position.x <= x_range[1]
                        and y_range[0] <= position.y <= y_range[1]
                        and z_range[0] <= position.z <= z_range[1]
                    ):
                        valid_users.append(user)

            random_dance, duration = random.choice(list(self.dances.items()))
            duration = float(duration)

            async def send_emote_safely(user):
                try:
                    await self.highrise.send_emote(random_dance, user.id)
                    bot_stats["total_dances"] += 1
                except Exception as e:
                    print(f"Error sending dance to {user.id}: {e}")

            tasks = [asyncio.create_task(send_emote_safely(user)) for user in valid_users]
            await asyncio.gather(*tasks)
            await asyncio.sleep(duration - 0.5)
            valid_users = []

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        bot_stats["total_joins"] += 1
        try:
            room_users = await self.highrise.get_room_users()
            bot_stats["user_count"] = len(room_users.content)
            if len(room_users.content) >= 125:
                await self.highrise.moderate_room(user.id, "kick")
                return
        except Exception as e:
            print(f"capacity check error: {e}")

        if user.username == "9.__":
            await self.highrise.chat("نورت الروم سيدي،تحت امرك يامولاي👑")
        else:
            welcomes = [
                f" أهلاً وسهلاً {user.username} نورت الروم ",
                f" حياك الله {user.username} يسعدنا وجودك ",
                f" ولكم بيك {user.username} وسط أهلك وناسك ",
                f" دخل {user.username} الروم اتنور ",
                f" أهلين {user.username} زين جيتك ",
                f" مرحبا {user.username} حللت وأهلت ",
                f" يا مرحبا {user.username} سعدنا بيك ",
                f" أهلاً بضيفنا العزيز {user.username} ",
                f" دخل {user.username} يسلم علينا ويسعد أوقاته ",
                f" ألف أهلين {user.username} ربي يسعدك ",
                f" نورت يا {user.username} وين الغيبة ",
                f" أهلاً بـ {user.username} يا زين الحضور ",
                f" حياك ربي {user.username} في ديرتك ",
                f" أهلاً {user.username} الروم ما يكتمل إلا بك ",
                f" ولكم بيك {user.username} طالت الغيبة ",
            ]
            await self.highrise.chat(random.choice(welcomes))
        await asyncio.sleep(1)
        await self.highrise.react("wave", user.id)
        await self.highrise.send_emote("emote-hello", user.id)

    async def on_user_move(self, user: User, position) -> None:
        try:
            if hasattr(position, 'x'):
                bot_stats["positions"][user.username] = {
                    "x": round(position.x, 2),
                    "y": round(position.y, 2),
                    "z": round(position.z, 2),
                    "facing": getattr(position, 'facing', ''),
                    "ts": time.time(),
                }
        except Exception as e:
            print(f"on_user_move error: {e}")

    async def print_message(self, message: str, user: User) -> None:
        try:
            dance_number = int(message.split()[0])
            if 1 <= dance_number <= len(dancs):
                current_dance = dancs[dance_number - 1]
                while True:
                    try:
                        await self.highrise.send_emote(current_dance, user.id)
                        bot_stats["total_dances"] += 1
                        await asyncio.sleep(6.5)
                    except Exception as e:
                        print(f"Chat Error: {e}")
                        break
        except ValueError:
            print("Invalid dance number format")

    async def on_chat(self, user: User, message: str) -> None:
        global valuesss
        bot_stats["total_commands"] += 1
        if message.startswith("الحق") and user.username in user_ad:
            values = message.split()
            valuesss = values[1].replace("@", "")
        elif message.startswith("توقف") and user.username in user_ad:
            await self.highrise.chat("حسنا")
            valuesss = "#####"
            self.stopped = True
            return
        if message.startswith("هزو") and user.username in user_ad:
            random_dans = random.sample(dancs, 1)[0]
            room_list = await self.highrise.get_room_users()
            for u, position in room_list.content:
                try:
                    await self.highrise.send_emote(random_dans, u.id)
                    bot_stats["total_dances"] += 1
                except:
                    print("error")

        if message.isdigit() and len(message.split()) > 0:
            if not hasattr(self, 'print_tasks'):
                self.print_tasks = {}

            if hasattr(self, 'print_tasks') and user.id in self.print_tasks and not self.print_tasks[user.id].done():
                self.print_tasks[user.id].cancel()
                await asyncio.sleep(0.1)

            self.print_tasks[user.id] = asyncio.create_task(self.print_message(message, user))

        if message.startswith(("توقف", "stop", "ايقاف", "0")):
            try:
                if hasattr(self, 'print_tasks') and user.id in self.print_tasks and not self.print_tasks[user.id].done():
                    self.print_tasks[user.id].cancel()
                    await asyncio.sleep(1)
            except ValueError:
                print("Invalid dance number format")

        if message.strip() == "جوست":
            if not hasattr(self, 'print_tasks'):
                self.print_tasks = {}
            if user.id in self.print_tasks and not self.print_tasks[user.id].done():
                self.print_tasks[user.id].cancel()
                await asyncio.sleep(0.1)
            async def loop_ghost(uid=user.id):
                while True:
                    try:
                        await self.highrise.send_emote("emote-ghost-idle", uid)
                        await asyncio.sleep(6.5)
                    except Exception:
                        break
            self.print_tasks[user.id] = asyncio.create_task(loop_ghost())

        if message.strip() == "ريست":
            if not hasattr(self, 'print_tasks'):
                self.print_tasks = {}
            if user.id in self.print_tasks and not self.print_tasks[user.id].done():
                self.print_tasks[user.id].cancel()
                await asyncio.sleep(0.1)
            async def loop_rest(uid=user.id):
                while True:
                    try:
                        await self.highrise.send_emote("sit-idle-cute", uid)
                        await asyncio.sleep(6.5)
                    except Exception:
                        break
            self.print_tasks[user.id] = asyncio.create_task(loop_rest())

        if message.startswith("نزلني"):
            await self.highrise.teleport(user.id, Position(x='16.01', y='0', z='8.01'))
        if message.startswith("فوق"):
            await self.highrise.teleport(user.id, Position(x='15.5', y='12.0', z='25.0'))
        if message == "فوك":
            await self.highrise.teleport(user.id, Position(x='14.0', y='19.25', z='26.0'))
        if message.startswith("انتقال") and user.username in user_ad:
            if user.username not in self.ter:
                self.ter.append(user.username)
            else:
                print("u r in")
        if message == "vip" and user.username in user_ad:
            await self.highrise.teleport(user.id, Position(x='15.5', y='12.0', z='25.0'))
        if message.startswith("vip @") and user.username in user_ad:
            try:
                target_name = message.split('@', 1)[1].strip()
                room_users = await self.highrise.get_room_users()
                for u, pos in room_users.content:
                    if u.username == target_name:
                        await self.highrise.teleport(u.id, Position(x='15.5', y='12.0', z='25.0'))
                        break
            except Exception as e:
                print(f"vip @ error: {e}")
        if message == "vvip" and user.username in user_ad:
            await self.highrise.teleport(user.id, Position(x='14.5', y='0.25', z='3.5'))
        if message.startswith("vvip @") and user.username in user_ad:
            try:
                target_name = message.split('@', 1)[1].strip()
                room_users = await self.highrise.get_room_users()
                for u, pos in room_users.content:
                    if u.username == target_name:
                        await self.highrise.teleport(u.id, Position(x='14.5', y='0.25', z='3.5'))
                        break
            except Exception as e:
                print(f"vvip @ error: {e}")
        if message.startswith("جيب") and user.username in user_ad:
            if '@' not in message:
                await self.highrise.send_whisper(user.id, "اكتب: جيب @اسم_المستخدم")
            else:
                try:
                    target_name = message.split('@', 1)[1].strip()
                    room_users = await self.highrise.get_room_users()
                    admin_pos = None
                    target_id = None
                    for u, pos in room_users.content:
                        if u.id == user.id and isinstance(pos, Position):
                            admin_pos = pos
                        if u.username == target_name:
                            target_id = u.id
                    if target_id is None:
                        await self.highrise.send_whisper(user.id, f"المستخدم {target_name} مو موجود في الغرفة")
                    elif admin_pos is None:
                        await self.highrise.send_whisper(user.id, "ما قدرت أحدد موقعك")
                    else:
                        await self.highrise.teleport(target_id, Position(x=admin_pos.x, y=admin_pos.y, z=admin_pos.z))
                except Exception as e:
                    print(f"جيب error: {e}")
        if message.startswith("صعدني"):
            await self.highrise.teleport(user.id, Position(x='15.0', y='7.0', z='20.0'))
        if message.startswith("927363829") and user.username == "9.__":
            room_list = await self.highrise.get_room_users()
            for u, position in room_list.content:
                try:
                    await self.highrise.move_user_to_room(u.id, '655a7f15c9ad99cfd71031c0')
                except Exception as e:
                    print(f"حدث خطأ: {e}")
        if user.username in user_ad:
            if message.startswith("اطرد"):
                try:
                    target_name = message.split('@', 1)[1].strip()
                    room_users = await self.highrise.get_room_users()
                    for u, pos in room_users.content:
                        if u.username == target_name:
                            await self.highrise.moderate_room(u.id, "kick")
                            break
                except Exception as e:
                    print(f"اطرد error: {e}")
            if message.startswith("حظر"):
                try:
                    target_name = message.split('@', 1)[1].strip()
                    room_users = await self.highrise.get_room_users()
                    for u, pos in room_users.content:
                        if u.username == target_name:
                            await self.highrise.moderate_room(u.id, "ban", action_length=1440)
                            break
                except Exception as e:
                    print(f"حظر error: {e}")
            if message.startswith("بلوك"):
                try:
                    target_name = message.split('@', 1)[1].strip()
                    room_users = await self.highrise.get_room_users()
                    for u, pos in room_users.content:
                        if u.username == target_name:
                            await self.highrise.moderate_room(u.id, "ban")
                            break
                except Exception as e:
                    print(f"بلوك error: {e}")
            if message.startswith("ميوت"):
                try:
                    target_name = message.split('@', 1)[1].strip()
                    room_users = await self.highrise.get_room_users()
                    for u, pos in room_users.content:
                        if u.username == target_name:
                            await self.highrise.moderate_room(u.id, "mute", action_length=60)
                            break
                except Exception as e:
                    print(f"ميوت error: {e}")

    async def on_user_move(self, user: User, destination: Position | AnchorPosition) -> None:
        if user.username == "9.__":
            print(destination)
        try:
            if user.username == valuesss:
                self.x = destination.x
                self.y = destination.y
                self.z = destination.z
                await self.highrise.walk_to(Position(self.x, self.y, self.z - 1))
            if user.username in self.ter:
                if isinstance(destination, AnchorPosition):
                    print(f"AnchorPosition(entity_id={destination.entity_id}, anchor_ix={destination.anchor_ix}")
                else:
                    await self.highrise.teleport(user.id, Position(x=destination.x, y=destination.y, z=destination.z))
        except Exception as e:
            print(f"Error : {e}")

    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
        if user.username == "9.__":
            if reaction == "thumbs":
                try:
                    await self.highrise.move_user_to_room(receiver.id, '')
                    await self.highrise.chat(f"لم نتشرف بك ضيفا فلا تكرر زيارتنا ، لقد تم طرد المستخدم  {user.username}")
                except Exception as e:
                    print(f"حدث خطأ: {e}")
        if user.username in user_ad:
            if reaction == "wave":
                try:
                    r_username = receiver.username
                    print(f"receiver: {r_username}")
                    room_list = await self.highrise.get_room_users()
                    username_targ = user.username
                    for u, position in room_list.content:
                        if u.username == username_targ:
                            print(f"User: {u.username}")
                            print(f"id: {u.id}")
                            await self.highrise.teleport(receiver.id, Position(x=position.x, y=position.y, z=position.z - 1))
                except Exception as e:
                    print(f"حدث خطأ: {e}")


# ─── HTTP status server (for deployment health checks) ─────────────────────
async def handle_status(request):
    uptime_secs = int(time.time() - bot_stats["start_time"])
    h = uptime_secs // 3600
    m = (uptime_secs % 3600) // 60
    s = uptime_secs % 60
    data = {
        "online": bot_stats["online"],
        "roomId": ROOM_ID,
        "botName": BOT_NAME,
        "uptime": f"{h:02d}:{m:02d}:{s:02d}",
        "userCount": bot_stats["user_count"],
    }
    return web.Response(
        text=json.dumps(data),
        content_type="application/json",
        headers={"Access-Control-Allow-Origin": "*"},
    )

async def handle_stats(request):
    data = {
        "totalJoins": bot_stats["total_joins"],
        "totalDancesSent": bot_stats["total_dances"],
        "totalCommands": bot_stats["total_commands"],
        "startTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(bot_stats["start_time"])),
    }
    return web.Response(
        text=json.dumps(data),
        content_type="application/json",
        headers={"Access-Control-Allow-Origin": "*"},
    )

async def handle_health(request):
    return web.Response(
        text=json.dumps({"status": "ok"}),
        content_type="application/json",
        headers={"Access-Control-Allow-Origin": "*"},
    )

async def handle_positions(request):
    now = time.time()
    # Only return positions updated in the last 5 minutes
    active = {
        username: pos
        for username, pos in bot_stats["positions"].items()
        if now - pos["ts"] < 300
    }
    return web.Response(
        text=json.dumps({"positions": active}),
        content_type="application/json",
        headers={"Access-Control-Allow-Origin": "*"},
    )

async def run_http_server():
    import os
    port = int(os.environ.get("PORT", 8000))
    app = web.Application()
    app.router.add_get("/api/healthz", handle_health)
    app.router.add_get("/api/bot/status", handle_status)
    app.router.add_get("/api/bot/stats", handle_stats)
    app.router.add_get("/api/bot/positions", handle_positions)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"HTTP server running on port {port}")


API_TOKEN = os.environ["HIGHRISE_API_TOKEN"]


async def run_bot_with_retry():
    # Wait for any old deployment session to expire before connecting
    startup_delay = 45
    print(f"Waiting {startup_delay}s for old sessions to expire...")
    await asyncio.sleep(startup_delay)

    attempt = 0
    while True:
        attempt += 1
        print(f"Bot connection attempt #{attempt}...")
        bot_stats["online"] = False
        try:
            bot_definition = BotDefinition(
                bot=MyBot(),
                api_token=API_TOKEN,
                room_id=ROOM_ID,
            )
            await client_main([bot_definition])
        except Exception as e:
            wait = 30
            print(f"Bot disconnected: {e} — retrying in {wait}s...")
            await asyncio.sleep(wait)


async def self_ping():
    import os
    await asyncio.sleep(30)
    domains = os.environ.get("REPLIT_DOMAINS", "")
    domain = domains.split(",")[0].strip() if domains else ""
    if not domain:
        print("self_ping: no REPLIT_DOMAINS, skipping")
        return
    url = f"https://{domain}/api/healthz"
    print(f"self_ping: will ping {url} every 4 min")
    while True:
        try:
            import aiohttp as _aiohttp
            async with _aiohttp.ClientSession() as session:
                async with session.get(url, timeout=_aiohttp.ClientTimeout(total=10)) as r:
                    print(f"self_ping: {r.status}")
        except Exception as e:
            print(f"self_ping error: {e}")
        await asyncio.sleep(240)


async def main():
    await asyncio.gather(
        run_http_server(),
        run_bot_with_retry(),
        self_ping(),
    )


if __name__ == "__main__":
    asyncio.run(main())
