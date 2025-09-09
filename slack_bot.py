#!/usr/bin/env python3
import asyncio
import json
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError

class WeatherSlackBot:
    def __init__(self, token):
        self.client = AsyncWebClient(token=token)
    
    async def send_weather_report(self, channel, weather_analysis):
        try:
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🌤️ {weather_analysis['location']} 날씨 분석 보고서"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*🌡️ 평균 온도*\n{weather_analysis['temperature']['avg']}°C"
                        },
                        {
                            "type": "mrkdwn", 
                            "text": f"*💧 평균 습도*\n{weather_analysis['humidity']['avg']}%"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*📈 온도 트렌드*\n{weather_analysis['temperature']['trend']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⏰ 분석 시간*\n{weather_analysis['analysis_time'][:16]}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"📊 *요약*: {weather_analysis['summary']}"
                    }
                }
            ]
            
            response = await self.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                username="날씨봇",
                icon_emoji=":sunny:"
            )
            
            return {"success": True, "ts": response["ts"]}
            
        except SlackApiError as e:
            return {"success": False, "error": str(e)}

async def send_to_slack_formatted(token, channel, analysis_data):
    bot = WeatherSlackBot(token)
    result = await bot.send_weather_report(channel, analysis_data)
    return result