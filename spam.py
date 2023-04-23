import aiohttp
import getpass
import asyncio

async def convert_gamertag_to_xuid(gamertag: str):
    async with aiohttp.ClientSession() as session:    
        resp = await session.get("https://xbl.io/api/v2/search/{}".format(gamertag), headers={"accept": "*/*", "x-authorization": auth_key, "Content-Type": "application/json"})
        data = await resp.json()

        xuid = data["people"][0]["xuid"]
        return xuid

auth_key = getpass.getpass("Enter auth key: ")

async def main():
    gamertag = input("Gamertag to spam: ")
    message = input("Message to spam: ")
    amount = int(input("Amount of times to spam: "))

    xuid = await convert_gamertag_to_xuid(gamertag)

    for i in range(amount):
        async with aiohttp.ClientSession() as session:
            r = await session.post("https://xbl.io/api/v2/conversations", json={"message": message, "xuid": xuid}, headers={"accept": "*/*", "x-authorization": auth_key, "Content-Type": "application/json"})

            print("[SUCCESS] Sent {} message(s)".format(i + 1))

            if "limitType" in (await r.json()).keys():
                print("[ERROR] Rate Limited")

asyncio.run(main())